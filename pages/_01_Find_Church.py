"""
🔍 Find My Local Church
Search by location, values, and accessibility. Powered by OpenStreetMap.
"""

import streamlit as st
import sys

# ── Mobile CSS ──────────────────────────────────────────────────────────────
import sys as _sys
_sys.path.insert(0, ".")
try:
    from services.mobile_ux import inject_mobile_css as _inj; _inj()
except Exception:
    pass

sys.path.insert(0, ".")

st.set_page_config(page_title="Find My Church", page_icon="🔍", layout="wide")

st.title("🔍 Find My Local Church")
st.markdown("Search by location, values, and accessibility. Powered by OpenStreetMap — real global data, no API key required.")


# ── Quick-search popular cities ───────────────────────────────────────────────
st.markdown("**Quick search — tap to search**")
_qcols = st.columns(6)
_cities = [
    ("Nairobi", "Kenya"), ("Kampala", "Uganda"), ("Lagos", "Nigeria"),
    ("Manila", "Philippines"), ("São Paulo", "Brazil"), ("Rome", "Italy"),
]
for _col, (_qcity, _qcountry) in zip(_qcols, _cities):
    if _col.button(_qcity, key=f"qc_{_qcity}", use_container_width=True):
        st.session_state["_qcity"]    = _qcity
        st.session_state["_qcountry"] = _qcountry

# Pre-fill from quick-search
_prefill_city    = st.session_state.pop("_qcity",    "")
_prefill_country = st.session_state.pop("_qcountry", "")

col1, col2 = st.columns([1, 1])
with col1:
    city    = st.text_input("City", value=_prefill_city, placeholder="Nairobi / Manila / São Paulo / Rome")
    country = st.text_input("Country (optional, improves accuracy)", value=_prefill_country, placeholder="Kenya / Philippines / Brazil")
    radius  = st.slider("Search radius (km)", 5, 80, 30)
with col2:
    st.markdown("**Language preference**")
    languages = st.multiselect("Languages", ["English","Swahili","Spanish","Tagalog","French","Portuguese","Polish","Vietnamese","Korean","Arabic","Luganda"], default=["English"])
    st.markdown("**Accessibility**")
    wheelchair = st.checkbox("Wheelchair accessible")
    nursery    = st.checkbox("Childcare / nursery")

st.markdown("**Values matching** *(for discovery — not visible to parishes)*")
c1, c2, c3 = st.columns(3)
with c1:
    v_justice     = st.slider("Social justice engagement", 0, 10, 5)
    v_lgbtq       = st.slider("LGBTQ+ welcome", 0, 10, 5)
with c2:
    v_immigrant   = st.slider("Immigrant / refugee welcome", 0, 10, 5)
    v_transparency= st.slider("Financial transparency", 0, 10, 5)
with c3:
    v_youth       = st.slider("Youth engagement", 0, 10, 5)
    v_women       = st.slider("Women in leadership", 0, 10, 5)

search_btn = st.button("🔍 Find Churches Near Me", type="primary", use_container_width=True)

# ── Run search and cache results in session_state ─────────────────────────────
# Critical: results MUST survive reruns so save buttons can fire correctly.
if search_btn:
    if not city.strip():
        st.warning("Please enter a city name")
        st.session_state.pop("_church_results", None)
    else:
        with st.spinner(f"Searching for Catholic churches in {city}... (OSM live data)"):
            try:
                from gospelmap.church_search import search_by_city

                @st.cache_data(ttl=86400, show_spinner=False)
                def _cached_search(city, country):
                    return search_by_city(city, country or None, limit=15)

                results = _cached_search(city.strip(), country.strip() or None)
                st.session_state["_church_results"] = results
                st.session_state["_church_search_city"] = city.strip()
                st.session_state["_church_search_country"] = country.strip()
            except Exception as e:
                st.session_state.pop("_church_results", None)
                err_str = str(e)
                if "timed out" in err_str or "timeout" in err_str.lower():
                    st.warning(
                        "**The OpenStreetMap server is taking too long to respond.** "
                        "This usually resolves in a few seconds. "
                        "Try again — we automatically retry multiple servers. "
                        f"\n\nCity searched: **{city.strip()}**"
                    )
                else:
                    st.warning(
                        "**Church search unavailable right now.** "
                        "OpenStreetMap data is free and community-maintained — servers can be slow at peak times. "
                        "Try again in 10–30 seconds. Coverage is best for Nairobi, Mombasa, Kampala, Lagos, Manila, "
                        "São Paulo, Rome, and most major cities."
                    )

# ── Render cached results (persists across reruns / save button clicks) ───────
if "_church_results" in st.session_state:
    churches = st.session_state["_church_results"]
    _search_city = st.session_state.get("_church_search_city", city)
    _search_country = st.session_state.get("_church_search_country", country)

    if not churches:
        st.warning("No churches found. Try a larger city or different spelling.")
        st.info("💡 OSM coverage varies by region. Major cities in East Africa, Philippines, Brazil, Europe have good coverage.")
    else:
        st.success(f"Found **{len(churches)} Catholic churches** near {_search_city}")
        st.divider()

        for i, c in enumerate(churches, 1):
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.subheader(f"{i}. {c.name}")
                    if c.address:
                        st.caption(f"📍 {c.address}")
                    elif c.city:
                        st.caption(f"📍 {c.city}{', ' + c.country if c.country else ''}")
                with col2:
                    if c.distance_km:
                        st.metric("Distance", f"{c.distance_km:.1f} km")
                with col3:
                    gmaps = f"https://www.google.com/maps?q={c.latitude},{c.longitude}"
                    st.markdown(f"[📍 Google Maps]({gmaps})")

                detail_cols = st.columns(3)
                with detail_cols[0]:
                    if c.phone:
                        st.write(f"📞 {c.phone}")
                with detail_cols[1]:
                    if c.website:
                        st.write(f"🌐 [{c.website[:30]}]({c.website})")
                with detail_cols[2]:
                    osm_link = f"https://www.openstreetmap.org/node/{c.osm_id}" if c.osm_id else None
                    if osm_link:
                        st.markdown(f"[🗺️ OSM]({osm_link})")

                # ── Save to directory ─────────────────────────────────────────
                _saved_key = f"dir_saved_{c.name}_{c.latitude}"
                if st.session_state.get(_saved_key):
                    st.success("✅ Saved to parish directory", icon=None)
                else:
                    if st.button(
                        "➕ Save to our directory",
                        key=f"save_{i}_{c.name}",
                        type="secondary",
                    ):
                        from services.sheets import _save
                        _record = {
                            "name": c.name,
                            "address": getattr(c, "address", "") or "",
                            "city": getattr(c, "city", _search_city) or _search_city,
                            "country": getattr(c, "country", _search_country) or _search_country,
                            "latitude": str(c.latitude),
                            "longitude": str(c.longitude),
                            "phone": getattr(c, "phone", "") or "",
                            "website": getattr(c, "website", "") or "",
                            "osm_id": str(getattr(c, "osm_id", "") or ""),
                            "source": "OSM Search",
                        }
                        ok = _save("church_directory", _record)
                        st.session_state[_saved_key] = True
                        if ok:
                            st.success(f"✅ **{c.name}** saved to the directory sheet!")
                        else:
                            st.warning(
                                f"⚠️ **{c.name}** could not be saved to Sheets. "
                                "Parish directory sync is being set up. "
                                "(Admin → Data Management → connect Google Sheets)."
                            )
                        st.rerun()

                st.divider()

st.info("""
**Data Source:** OpenStreetMap (crowdsourced, real-time)
Coverage is best in Europe and East Africa, growing globally.
Help improve coverage: [openstreetmap.org](https://openstreetmap.org)
""")

# ── Manual entry ──────────────────────────────────────────────────────────────
st.divider()
with st.expander("✏️ Know a church that didn't appear? Add it manually"):
    st.caption("Your entry goes into the same parish directory sheet as search results.")
    with st.form("manual_church_entry", clear_on_submit=True):
        mc1, mc2 = st.columns(2)
        with mc1:
            m_name    = st.text_input("Church Name *", placeholder="e.g. Sacred Heart Parish")
            m_diocese = st.text_input("Diocese", placeholder="e.g. Archdiocese of Nairobi")
            m_country = st.text_input("Country *", placeholder="e.g. Kenya")
            m_city    = st.text_input("City / Region", placeholder="e.g. Westlands, Nairobi")
            m_address = st.text_input("Street Address", placeholder="e.g. Westlands Road")
        with mc2:
            m_lat     = st.text_input("Latitude", placeholder="e.g. -1.2634")
            m_lon     = st.text_input("Longitude", placeholder="e.g. 36.8022")
            m_phone   = st.text_input("Phone", placeholder="e.g. +254 20 123 4567")
            m_website = st.text_input("Website", placeholder="https://...")
            m_hours   = st.text_input("Mass / Opening Hours", placeholder="e.g. Sun 7am, 9am, 11am")
        m_notes    = st.text_area("Notes", placeholder="Languages spoken, accessibility, ministries…", height=70)
        m_added_by = st.text_input("Your name or email (optional)", placeholder="For follow-up if needed")

        if st.form_submit_button("💾 Save to Directory Sheet", type="primary"):
            if not m_name.strip():
                st.error("Church Name is required.")
            elif not m_country.strip():
                st.error("Country is required.")
            else:
                from services.sheets import _save
                _record = {
                    "name": m_name.strip(),
                    "diocese": m_diocese.strip(),
                    "country": m_country.strip(),
                    "city": m_city.strip(),
                    "address": m_address.strip(),
                    "latitude": m_lat.strip(),
                    "longitude": m_lon.strip(),
                    "phone": m_phone.strip(),
                    "website": m_website.strip(),
                    "opening_hours": m_hours.strip(),
                    "notes": m_notes.strip(),
                    "added_by": m_added_by.strip() or "anonymous",
                    "source": "Manual Entry",
                }
                ok = _save("church_directory", _record)
                if ok:
                    st.success(f"✅ **{m_name.strip()}** saved to the parish directory sheet!")
                    st.balloons()
                else:
                    st.info(f"✅ **{m_name.strip()}** noted for this session. Connect Sheets in Admin → Data for full persistence.")
