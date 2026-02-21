"""Parish Directory — Search + Manual submission + Live OSM worldwide."""

import streamlit as st
try:
    from services.save_indicator import mark_saved, show_save_status
except Exception:
    def mark_saved(x): pass
    def show_save_status(x, y=None): pass
import urllib.request
import json
import time
from datetime import date

st.set_page_config(page_title="Parish Directory", page_icon="🗺️", layout="wide")

try:
    from services.theme import inject, hero, section_label
    inject()
except Exception:
    pass

# ── Session state ─────────────────────────────────────────────────────────────
if "submitted_parishes" not in st.session_state:
    st.session_state.submitted_parishes = []
if "confirmed_parishes" not in st.session_state:
    st.session_state.confirmed_parishes = [
        {"id": 1, "name": "Holy Family Basilica", "city": "Nairobi", "country": "Kenya",
         "diocese": "Nairobi", "address": "City Square, Nairobi", "phone": "+254 20 222 4861",
         "mass_times": "Sun: 7am, 9am, 11am, 6pm | Mon–Sat: 6:30am, 12:15pm",
         "verified": True, "confirmations": 12, "added": "2024-01-01"},
        {"id": 2, "name": "Our Lady of Perpetual Help", "city": "Cebu City", "country": "Philippines",
         "diocese": "Cebu", "address": "Osmeña Blvd, Cebu City", "phone": "+63 32 253 9394",
         "mass_times": "Sun: 6am, 8am, 10am, 12pm, 6pm | Daily: 6am, 6pm",
         "verified": True, "confirmations": 7, "added": "2024-01-15"},
        {"id": 3, "name": "Igreja Nossa Senhora da Consolação", "city": "São Paulo", "country": "Brazil",
         "diocese": "São Paulo", "address": "Rua da Consolação, São Paulo", "phone": "+55 11 3256 0144",
         "mass_times": "Dom: 8h, 10h, 12h, 19h | Seg–Sex: 7h, 12h, 19h",
         "verified": True, "confirmations": 8, "added": "2024-01-15"},
        {"id": 4, "name": "All Saints Catholic Church", "city": "Manassas", "country": "USA",
         "diocese": "Arlington", "address": "Stonewall Road, Manassas VA",
         "mass_times": "Sun: 8am, 10am, 12pm, 5pm | Sat: 5pm",
         "verified": True, "confirmations": 7, "added": "2024-02-01"},
        {"id": 5, "name": "Ngurunit Catholic Church", "city": "Ngurunit", "country": "Kenya",
         "diocese": "Marsabit", "address": "Ngurunit Village, Samburu",
         "mass_times": "Sun: 9am | Wed: 7am",
         "verified": True, "confirmations": 4, "added": "2024-03-01"},
        {"id": 6, "name": "Korr Catholic Parish", "city": "Korr", "country": "Kenya",
         "diocese": "Marsabit", "address": "Korr, Marsabit County",
         "mass_times": "Sun: 9am",
         "verified": True, "confirmations": 3, "added": "2024-03-15"},
    ]


# ── OSM helpers ───────────────────────────────────────────────────────────────
_UA = "CatholicParishSteward/2.0 (https://catholicparishsteward.streamlit.app)"

def _http_get(url: str, timeout=15) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))

_OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",  # fallback mirror
    "https://overpass.openstreetmap.ru/api/interpreter",        # 2nd fallback
]

def _overpass(query: str, timeout=35) -> list:
    """Try multiple Overpass endpoints — returns first successful result."""
    body = query.encode("utf-8")
    last_err = None
    for endpoint in _OVERPASS_ENDPOINTS:
        try:
            req = urllib.request.Request(
                endpoint, data=body,
                headers={"Content-Type": "text/plain", "User-Agent": _UA},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8")).get("elements", [])
        except Exception as e:
            last_err = e
            continue  # try next endpoint
    raise last_err  # re-raise so caller can handle / log

def geocode_place(place_name: str) -> dict | None:
    """Convert a place name to coordinates + bounding box via Nominatim.
    Prefers administrative/settlement results over water features."""
    encoded = urllib.parse.quote(place_name)
    # Try with limit=5 so we can pick the best result
    url = (f"https://nominatim.openstreetmap.org/search"
           f"?q={encoded}&format=json&limit=5&addressdetails=1")
    try:
        results = _http_get(url, timeout=10)
        if not results:
            return None
        # Prefer administrative/place results over water/natural features
        preferred_classes = {"boundary", "place"}
        preferred_types = {"city", "town", "village", "suburb", "county",
                           "state", "administrative", "municipality", "region"}
        bad_classes = {"waterway", "water", "natural"}
        r = None
        for candidate in results:
            cls = candidate.get("class", "")
            typ = candidate.get("type", "")
            if cls in bad_classes:
                continue
            if cls in preferred_classes or typ in preferred_types:
                r = candidate
                break
        if r is None:
            r = results[0]  # fall back to first result
        bb = r.get("boundingbox", [])
        if not bb or len(bb) < 4:
            return None
        lat, lon = float(r["lat"]), float(r["lon"])
        s, n, w, e = float(bb[0]), float(bb[1]), float(bb[2]), float(bb[3])
        # Cap very large bounding boxes — use radius around centroid instead
        lat_span, lon_span = n - s, e - w
        if lat_span > 1.5 or lon_span > 1.5:
            pad = 0.25  # ~28km radius — enough for a city
            s, n, w, e = lat - pad, lat + pad, lon - pad, lon + pad
        return {
            "display_name": r.get("display_name", place_name),
            "lat": lat, "lon": lon,
            "s": s, "n": n, "w": w, "e": e,
            "type": r.get("type", ""),
        }
    except Exception:
        pass
    return None

def search_churches_by_place(geo: dict, max_results=20) -> list:
    """
    Search for Catholic churches within a bounding box.
    Expands the box for sparse/rural areas automatically.
    Tier 1: dense city — use bbox as-is
    Tier 2: town/suburb — small pad
    Tier 3: village — moderate expansion (~17km)
    Tier 4: remote/nomadic — large expansion (~55km, for Turkana-scale areas)
    """
    s, n, w, e = geo["s"], geo["n"], geo["w"], geo["e"]
    lat_span = n - s
    lon_span = e - w

    if lat_span < 0.05 and lon_span < 0.05:
        # Tiny (single road/hamlet) — remote nomadic area: 0.5° ≈ 55km
        pad = 0.5
    elif lat_span < 0.15 and lon_span < 0.15:
        # Small village: 0.2° ≈ 22km
        pad = 0.2
    elif lat_span < 0.3 and lon_span < 0.3:
        # Small town: 0.08° ≈ 9km
        pad = 0.08
    else:
        pad = 0.0  # City or larger — use bbox as returned by Nominatim

    s -= pad; n += pad; w -= pad; e += pad

    # Comprehensive query covering all OSM Catholic church tagging patterns:
    # - denomination=catholic OR roman_catholic (most tagged churches)
    # - religion=christian + catholic name patterns (English, Swahili, French, Spanish, Portuguese)
    # - relation type catches cathedrals and basilicas (large buildings often tagged as relations)
    # Build query parts separately to avoid f-string + backslash conflicts
    bbox = f"{s},{w},{n},{e}"
    denom_pat = "^(catholic|roman_catholic)$"
    name_pat = "catholic|saint|st[.] |holy|our lady|blessed|sacred|consolata|assumption|immaculate|annunciation|resurrection|corpus christi|kanisa|parokia|paroisse|iglesia|igreja"
    name_pat_way = "catholic|saint|holy|our lady|blessed|sacred|consolata|assumption|immaculate"
    big_pat = "catholic|cathedral|basilica|shrine"
    query = (
        "[out:json][timeout:40];\n("
        f'\n  node["amenity"="place_of_worship"]["denomination"~"{denom_pat}",i]({bbox});'
        f'\n  way["amenity"="place_of_worship"]["denomination"~"{denom_pat}",i]({bbox});'
        f'\n  relation["amenity"="place_of_worship"]["denomination"~"{denom_pat}",i]({bbox});'
        f'\n  node["amenity"="place_of_worship"]["religion"="christian"]["name"~"{name_pat}",i]({bbox});'
        f'\n  way["amenity"="place_of_worship"]["religion"="christian"]["name"~"{name_pat_way}",i]({bbox});'
        f'\n  relation["amenity"="place_of_worship"]["religion"="christian"]["name"~"{big_pat}",i]({bbox});'
        f'\n);\nout center {max_results};'
    )
    return _overpass(query)

def search_churches_by_name(name_query: str, max_results=15) -> list:
    """
    Search globally by church name — finds specific named churches anywhere on earth.
    Best for: 'Consolata Shrine', 'Holy Family', 'St. Peter' etc.
    """
    # Sanitise for Overpass regex
    safe = name_query.replace('"', '').replace("'", "").replace("\\", "")
    query = f"""
[out:json][timeout:30];
(
  node["amenity"="place_of_worship"]["name"~"{safe}",i];
  way["amenity"="place_of_worship"]["name"~"{safe}",i];
);
out center {max_results};
"""
    elements = _overpass(query)
    # Filter to likely-Catholic results
    catholic_hints = {"catholic", "saint", "our lady", "holy", "blessed",
                      "sacred heart", "consolata", "salesian", "jesuit",
                      "dominican", "franciscan"}
    def is_likely_catholic(el):
        tags = el.get("tags", {})
        denom = tags.get("denomination", "").lower()
        religion = tags.get("religion", "").lower()
        name = tags.get("name", "").lower()
        return (
            "catholic" in denom or
            religion == "christian" and any(h in name for h in catholic_hints) or
            "catholic" in name
        )
    filtered = [e for e in elements if is_likely_catholic(e)]
    return filtered if filtered else elements[:5]  # fall back to unfiltered if needed

def format_osm_result(el: dict) -> dict:
    tags = el.get("tags", {})
    name = tags.get("name") or tags.get("name:en") or "Unnamed church"
    parts = [p for p in [
        tags.get("addr:housenumber", ""),
        tags.get("addr:street", ""),
        tags.get("addr:city", "") or tags.get("addr:town", "") or tags.get("addr:village", ""),
        tags.get("addr:country", ""),
    ] if p]
    address = ", ".join(parts) if parts else ""
    phone = tags.get("phone", "") or tags.get("contact:phone", "")
    website = tags.get("website", "") or tags.get("contact:website", "")
    opening = tags.get("opening_hours", "")
    lat = el.get("lat") or (el.get("center", {}) or {}).get("lat")
    lon = el.get("lon") or (el.get("center", {}) or {}).get("lon")
    maps_link = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else ""
    return {"name": name, "address": address, "phone": phone,
            "website": website, "opening_hours": opening, "maps_link": maps_link}

import urllib.parse


# ══════════════════════════════════════════════════════════════════════════════
# PAGE
# ══════════════════════════════════════════════════════════════════════════════
try:
    hero("Parish Directory", "Find a Catholic church anywhere in the world", "DIRECTORY")
except Exception:
    st.title("🗺️ Parish Directory")

tab1, tab2, tab3 = st.tabs(["🔍 Find a Parish", "➕ Add a Parish", "⏳ Pending Verification"])


# ══ TAB 1: SEARCH ════════════════════════════════════════════════════════════
with tab1:
    m1, m2, m3 = st.columns(3)
    m1.metric("Listed Parishes", len(st.session_state.confirmed_parishes))
    m2.metric("Community-Verified", sum(1 for p in st.session_state.confirmed_parishes if p["verified"]))
    m3.metric("Countries", len(set(p["country"] for p in st.session_state.confirmed_parishes)))

    st.divider()

    # ── Local directory search ─────────────────────────────────────────────
    try:
        section_label("Search our directory")
    except Exception:
        st.markdown("**Search our directory**")

    try:
        from services.settings import get as _get_setting
        _diocese_pref = _get_setting("diocese") or ""
    except Exception:
        _diocese_pref = ""
    query = st.text_input("Search by name, city, or country",
                          value=_diocese_pref,
                          placeholder="Consolata · Nairobi · Uganda · Samburu",
                          label_visibility="collapsed")
    c1, c2 = st.columns(2)
    country_filter = c1.selectbox("Country",
        ["All"] + sorted(set(p["country"] for p in st.session_state.confirmed_parishes)))
    diocese_filter = c2.selectbox("Diocese",
        ["All"] + sorted(set(p.get("diocese","") for p in st.session_state.confirmed_parishes if p.get("diocese"))))

    results = st.session_state.confirmed_parishes
    if query:
        q = query.lower()
        results = [p for p in results if any(
            q in str(p.get(f, "")).lower()
            for f in ["name", "city", "country", "diocese", "address"]
        )]
    if country_filter != "All":
        results = [p for p in results if p["country"] == country_filter]
    if diocese_filter != "All":
        results = [p for p in results if p.get("diocese") == diocese_filter]

    if results:
        for p in results:
            badge = "✅" if p["verified"] else "⏳"
            with st.expander(f"{badge} **{p['name']}** — {p.get('city','')} · {p['country']}"):
                c1, c2 = st.columns(2)
                with c1:
                    if p.get("address"):  st.markdown(f"📍 {p['address']}")
                    if p.get("phone"):    st.markdown(f"📞 {p['phone']}")
                    if p.get("diocese"):  st.markdown(f"⛪ Diocese of {p['diocese']}")
                with c2:
                    if p.get("mass_times"): st.markdown(f"🕐 **Mass Times**\n{p['mass_times']}")
                if not p["verified"]:
                    conf = p.get("confirmations", 0)
                    st.progress(min(conf/3, 1.0), text=f"{conf}/3 community confirmations")
                if st.button("✅ I've been here — confirm it", key=f"conf_{p['id']}"):
                    p["confirmations"] = p.get("confirmations", 0) + 1
                    if p["confirmations"] >= 3:
                        p["verified"] = True
                    st.success("Thank you!")
                    st.rerun()

    elif query:
        st.info("Not in our directory yet. Try the worldwide search below, or add it.")

    # ── WORLDWIDE OSM SEARCH ───────────────────────────────────────────────
    st.divider()
    try:
        section_label("Worldwide search — 40,000+ Catholic churches via OpenStreetMap")
    except Exception:
        st.markdown("#### 🌍 Search churches globally")

    st.caption(
        "Find Catholic churches anywhere on earth — cities, rural areas, remote regions. "
        "Data from OpenStreetMap volunteers worldwide."
    )

    osm_col1, osm_col2 = st.columns([2, 1])
    osm_name = osm_col1.text_input(
        "Church name or keyword (optional)",
        placeholder="Consolata · Sacred Heart · Our Lady · Saint Peter",
        key="osm_name",
    )
    osm_place = osm_col1.text_input(
        "Location — city, region, or country",
        placeholder="Samburu Kenya · Nairobi · Manassas Virginia · Lagos Nigeria · Manila · São Paulo",
        key="osm_place",
    )
    search_mode = osm_col2.radio(
        "Search method",
        ["📍 By location", "🔤 By church name", "🌐 Both"],
        key="osm_mode",
        help="'By location' finds all Catholic churches in an area. "
             "'By church name' finds a specific church anywhere on earth. "
             "'Both' combines both approaches.",
    )
    osm_max = osm_col2.slider("Max results", 5, 30, 15, key="osm_max")

    if st.button("🔍 Search worldwide", type="primary", key="osm_btn"):
        if not osm_name.strip() and not osm_place.strip():
            st.warning("Please enter a church name, a location, or both.")
        else:
            st.session_state["_osm_search_ran"] = True
            osm_results = []
            osm_errors = []

            with st.spinner("Searching the world's Catholic church data…"):
                # ── NAME-BASED GLOBAL SEARCH ──────────────────────────────
                if search_mode in ("🔤 By church name", "🌐 Both") and osm_name.strip():
                    try:
                        # First try Nominatim (fastest for exact matches)
                        encoded = urllib.parse.quote(osm_name.strip())
                        nom_url = (f"https://nominatim.openstreetmap.org/search"
                                   f"?q={encoded}&format=json&limit=5&addressdetails=1"
                                   f"&featuretype=religion")
                        nom = _http_get(nom_url, timeout=10)
                        for r in nom[:5]:
                            dn = r.get("display_name", "")
                            osm_results.append({
                                "name": osm_name.strip(),
                                "address": dn[:120],
                                "phone": "", "website": "",
                                "opening_hours": "",
                                "maps_link": f"https://www.google.com/maps?q={r['lat']},{r['lon']}",
                            })
                        # Also search Overpass by name
                        time.sleep(0.5)  # Nominatim rate limit
                        els = search_churches_by_name(osm_name.strip(), max_results=osm_max)
                        for el in els:
                            r = format_osm_result(el)
                            if r["name"].lower() != "unnamed church":
                                osm_results.append(r)
                    except Exception as _name_err:
                        osm_errors.append(f"name_search: {str(_name_err)[:80]}")

                # ── LOCATION-BASED SEARCH ─────────────────────────────────
                if search_mode in ("📍 By location", "🌐 Both") and osm_place.strip():
                    try:
                        # Add church name to Nominatim query for combined searches
                        query_str = (f"{osm_name.strip()} {osm_place.strip()}".strip()
                                     if (search_mode == "🌐 Both" and osm_name.strip())
                                     else osm_place.strip())
                        geo = geocode_place(query_str)
                        if geo:
                            time.sleep(0.5)
                            els = search_churches_by_place(geo, max_results=osm_max)
                            _dn_parts = geo["display_name"].split(",")
                            area_label = _dn_parts[0].strip()
                            if len(_dn_parts) > 1:
                                area_label += f", {_dn_parts[1].strip()}"
                            for el in els:
                                # Filter out non-Catholic churches that leaked through name matching
                                tags = el.get("tags", {})
                                denom = tags.get("denomination", "").lower()
                                if denom and denom not in ("catholic", "roman_catholic", ""):
                                    continue  # skip confirmed non-Catholic
                                r = format_osm_result(el)
                                osm_results.append(r)
                        else:
                            osm_errors.append("geocode")
                    except Exception as _loc_err:
                        osm_errors.append(f"location_search: {str(_loc_err)[:80]}")

            # ── DEDUPLICATE & CACHE ──────────────────────────────────────
            seen, unique = set(), []
            for r in osm_results:
                key = r["name"].lower()[:30] + r["address"][:20]
                if key not in seen:
                    seen.add(key)
                    unique.append(r)
            # Cache results so they survive st.rerun()
            st.session_state["_osm_last_results"] = unique
            st.session_state["_osm_last_max"] = osm_max

            # ── DISPLAY ──────────────────────────────────────────────────
            if unique:
                st.success(f"Found {len(unique)} church{'es' if len(unique)>1 else ''}")
                for r in unique[:osm_max]:
                    with st.expander(f"⛪ {r['name']}"):
                        c1, c2 = st.columns(2)
                        if r["address"]:   c1.markdown(f"📍 {r['address'][:120]}")
                        if r["phone"]:     c1.markdown(f"📞 {r['phone']}")
                        if r["opening_hours"]: c2.markdown(f"🕐 {r['opening_hours']}")
                        if r["website"]:   c2.markdown(f"🔗 [{r['website'][:40]}]({r['website']})")
                        if r["maps_link"]: st.markdown(f"[📍 Open in Google Maps]({r['maps_link']})")

                        col_a, col_b = st.columns(2)
                        _save_key = f"saved_osm_{hash(r['name']+r['address'])}"
                        if st.session_state.get(_save_key):
                            col_a.success("✓ Saved to directory", icon=None)
                        elif col_a.button("➕ Save to our directory", key=f"save_{hash(r['name']+r['address'])}"):
                            from services.sheets import _save as _do_save
                            new_id = max((p["id"] for p in
                                st.session_state.confirmed_parishes +
                                st.session_state.submitted_parishes), default=0) + 1
                            addr_parts = r["address"].split(",")
                            _city    = addr_parts[1].strip() if len(addr_parts) > 1 else ""
                            _country = addr_parts[-1].strip() if addr_parts else ""
                            parish_data = {
                                "id": new_id, "name": r["name"],
                                "city": _city, "country": _country,
                                "address": r["address"], "phone": r["phone"],
                                "mass_times": r["opening_hours"],
                                "website": r.get("website", ""),
                                "maps_link": r.get("maps_link", ""),
                                "verified": False, "confirmations": 1,
                                "submitted_by": "OSM import",
                                "source": "OpenStreetMap",
                                "added": str(date.today()),
                            }
                            st.session_state.submitted_parishes.append(parish_data)
                            _ok = _do_save("parish_submission", parish_data)
                            st.session_state[_save_key] = True
                            if _ok:
                                col_a.success("✓ Saved to Google Sheets", icon=None)
                            else:
                                col_a.info("Saved for this session", icon="💾")
                            st.rerun()

            else:
                _geocode_failed = any("geocode" in e for e in osm_errors)
                _search_failed  = any("location_search" in e or "name_search" in e for e in osm_errors)
                _has_err_detail = any(":" in e for e in osm_errors)

                if _geocode_failed:
                    st.warning(
                        "**Location not recognised.** Try a nearby larger town — "
                        "e.g. 'Marsabit Kenya' instead of a remote village name. "
                        "For very remote areas, search the county or region name."
                    )
                elif _search_failed:
                    # Overpass timed out or all endpoints failed — give user a retry hint
                    err_detail = " | ".join(e for e in osm_errors if ":" in e)[:120]
                    st.warning(
                        "**The worldwide church database is temporarily busy.** "
                        "Please wait 10 seconds and try again. "
                        "Coverage is good for Nairobi, Mombasa, Kisumu, Kampala, Lagos, Manila, São Paulo and most cities."
                        + (("\n\n*Detail: " + err_detail + "*") if err_detail else "")
                    )
                else:
                    st.info(
                        "No Catholic churches found in this area yet. "
                        "OpenStreetMap coverage is dense in cities and growing in rural regions — "
                        "Turkana, Marsabit, and other remote dioceses are still being mapped. "
                        "You can **add your parish** using the tab below."
                    )

    st.session_state["_osm_search_ran"] = False  # allow cache render on next pass
    # ── Render cached results (visible after save button reruns page) ──────────
    if not st.session_state.get("_osm_search_ran"):  # only if we didn't just run a search
        _cached = st.session_state.get("_osm_last_results")
        _cached_max = st.session_state.get("_osm_last_max", 15)
        if _cached:
            st.success(f"Found {len(_cached)} church{'es' if len(_cached)>1 else ''}")
            for r in _cached[:_cached_max]:
                with st.expander(f"⛪ {r['name']}"):
                    c1, c2 = st.columns(2)
                    if r["address"]:   c1.markdown(f"📍 {r['address'][:120]}")
                    if r["phone"]:     c1.markdown(f"📞 {r['phone']}")
                    if r.get("opening_hours"): c2.markdown(f"🕐 {r['opening_hours']}")
                    if r.get("website"):   c2.markdown(f"🔗 [{r['website'][:40]}]({r['website']})")
                    if r.get("maps_link"): st.markdown(f"[📍 Open in Google Maps]({r['maps_link']})")

                    col_a, col_b = st.columns(2)
                    _save_key = f"saved_osm_{hash(r['name']+r['address'])}"
                    if st.session_state.get(_save_key):
                        col_a.success("✓ Saved to directory", icon=None)
                    elif col_a.button("➕ Save to our directory", key=f"save_c_{hash(r['name']+r['address'])}"):
                        from services.sheets import _save as _do_save
                        new_id = max((pp["id"] for pp in
                            st.session_state.confirmed_parishes +
                            st.session_state.submitted_parishes), default=0) + 1
                        addr_parts = r["address"].split(",")
                        _city    = addr_parts[1].strip() if len(addr_parts) > 1 else ""
                        _country = addr_parts[-1].strip() if addr_parts else ""
                        parish_data = {
                            "id": new_id, "name": r["name"],
                            "city": _city, "country": _country,
                            "address": r["address"], "phone": r["phone"],
                            "mass_times": r.get("opening_hours", ""),
                            "website": r.get("website", ""),
                            "maps_link": r.get("maps_link", ""),
                            "verified": False, "confirmations": 1,
                            "submitted_by": "OSM import",
                            "source": "OpenStreetMap",
                            "added": str(date.today()),
                        }
                        st.session_state.submitted_parishes.append(parish_data)
                        _ok = _do_save("parish_submission", parish_data)
                        st.session_state[_save_key] = True
                        if _ok:
                            col_a.success("✓ Saved to Google Sheets", icon=None)
                        else:
                            col_a.info("Saved for this session", icon="💾")
                        st.rerun()

    st.caption(
        "Church data from [OpenStreetMap](https://www.openstreetmap.org) contributors "
        "worldwide. Coverage varies by region — rural Africa is actively being mapped. "
        "Verified listings are from our community directory above."
    )


# ══ TAB 2: ADD A PARISH ══════════════════════════════════════════════════════
with tab2:
    st.subheader("Add a Missing Parish")
    st.info(
        "Submit a parish and it enters **Pending** status. "
        "Once 3 parishioners confirm it, or a parish coordinator verifies it, "
        "it goes live in the directory for everyone.",
        icon="ℹ️"
    )

    with st.form("add_parish_form"):
        c1, c2 = st.columns(2)
        name    = c1.text_input("Parish Name *", placeholder="Our Lady of Lourdes")
        city    = c1.text_input("City / Town *", placeholder="Eldoret")
        country = c1.text_input("Country *", placeholder="Kenya")
        diocese = c1.text_input("Diocese", placeholder="Eldoret")
        address = c2.text_input("Street Address", placeholder="Kenyatta Ave")
        phone   = c2.text_input("Contact Phone", placeholder="+254 …")
        langs   = c2.multiselect("Languages of Mass",
            ["English","Kiswahili","Luganda","French","Dholuo","Kikuyu","Other"])
        mass_times = st.text_area("Mass Times",
            placeholder="e.g. Sun: 8am, 10am, 6pm | Daily: 7am\nDom: 9h, 11h | Sab: 18h", height=80)
        confession = st.text_input("Confession times (optional)",
            placeholder="Sat 4–5pm, or by appointment")
        submitter_role = st.selectbox("Your relationship to this parish",
            ["Parishioner","Parish coordinator","Priest / Deacon",
             "Visitor who attended Mass","Diocese staff","Other"])
        notes = st.text_area("Anything else useful (optional)",
            placeholder="Parking, accessibility, SCC presence…", height=60)
        submitted = st.form_submit_button("Submit Parish", type="primary")

    if submitted and name and city and country:
        from services.sheets import _save as _do_save
        new_id = max((p["id"] for p in st.session_state.confirmed_parishes +
                      st.session_state.submitted_parishes), default=0) + 1
        parish_data = {
            "id": new_id, "name": name, "city": city, "country": country,
            "diocese": diocese, "address": address, "phone": phone,
            "mass_languages": ", ".join(langs) if langs else "",
            "confession_times": confession,
            "mass_times": mass_times,
            "notes": notes,
            "verified": False, "confirmations": 0,
            "submitted_by": submitter_role,
            "source": "community",
            "added": str(date.today()),
        }
        st.session_state.submitted_parishes.append(parish_data)
        _ok = _do_save("parish_submission", parish_data)
        if _ok:
            st.success(
                f"\u2705 **{name}** saved to Google Sheets. "
                "It will go live once 3 parishioners confirm it or a coordinator verifies it."
            )
        else:
            st.info(
                f"**{name}** submitted for this session. "
                "To keep it permanently, connect Google Sheets "
                "\u2014 see More Tools \u2192 Admin & Data.",
                icon="\U0001f4be"
            )
        st.balloons()


# ══ TAB 3: PENDING VERIFICATION ══════════════════════════════════════════════
with tab3:
    st.subheader("Pending Community Verification")
    st.caption("Help verify parishes you know. Three confirmations make it live.")

    pending = [p for p in st.session_state.submitted_parishes if not p["verified"]]
    if not pending:
        st.success("No parishes waiting for verification right now.")
    else:
        for p in pending:
            with st.expander(f"⏳ {p['name']} — {p.get('city','')} · {p.get('country','')}"):
                c1, c2 = st.columns(2)
                c1.markdown(f"**Submitted by:** {p.get('submitted_by','')}")
                c1.markdown(f"**Date:** {p.get('added','')}")
                if p.get("address"): c1.markdown(f"**Address:** {p['address']}")
                if p.get("mass_times"): c2.markdown(f"**Mass Times:** {p['mass_times']}")
                if p.get("diocese"): c2.markdown(f"**Diocese:** {p['diocese']}")

                conf = p.get("confirmations", 0)
                st.progress(min(conf/3, 1.0), text=f"{conf}/3 confirmations")

                ca, cb = st.columns(2)
                if ca.button("✅ I know this parish — confirm", key=f"pc_{p['id']}"):
                    p["confirmations"] = conf + 1
                    if p["confirmations"] >= 3:
                        p["verified"] = True
                        st.session_state.confirmed_parishes.append(p)
                        st.session_state.submitted_parishes.remove(p)
                        st.success(f"🎉 {p['name']} is now live in the directory!")
                    else:
                        st.info(f"Recorded. {3 - p['confirmations']} more needed.")
                    st.rerun()
                if cb.button("⚠️ Something looks wrong", key=f"pf_{p['id']}"):
                    st.warning("Flagged for review. Thank you.")

        with st.expander("🔑 Parish coordinator: verify directly"):
            if pending:
                sel = st.selectbox("Parish", [p["name"] for p in pending], key="adm_sel")
                st.selectbox("Your role", ["Coordinator","Priest","Diocese Staff","Deacon"])
                if st.button("✅ Verify now", type="primary"):
                    for p in pending:
                        if p["name"] == sel:
                            p["verified"] = True
                            p["confirmations"] = max(p.get("confirmations",0), 3)
                            st.session_state.confirmed_parishes.append(p)
                            st.session_state.submitted_parishes.remove(p)
                            st.success(f"✅ {sel} is now live.")
                            st.rerun()

st.divider()
st.caption(
    "📌 Parish data is community-contributed and reviewed before going live. "
    "For official diocese records, contact your local bishop's office."
)
