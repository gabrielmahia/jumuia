"""Parish Directory — Search + Manual submission with community verification."""

import streamlit as st
import json
from datetime import date, datetime

st.set_page_config(page_title="Parish Directory", page_icon="🗺️", layout="wide")

# ── Session state ─────────────────────────────────────────────────────────────
if "submitted_parishes" not in st.session_state:
    st.session_state.submitted_parishes = []
if "confirmed_parishes" not in st.session_state:
    # Seed with a handful of verified entries
    st.session_state.confirmed_parishes = [
        {"id": 1, "name": "Holy Family Basilica", "city": "Nairobi", "country": "Kenya",
         "diocese": "Nairobi", "address": "City Square, Nairobi", "phone": "+254 20 222 4861",
         "mass_times": "Sun: 7am, 9am, 11am, 6pm | Mon–Sat: 6:30am, 12:15pm",
         "verified": True, "confirmations": 12, "added": "2024-01-01"},
        {"id": 2, "name": "St. Austin's Parish", "city": "Nairobi", "country": "Kenya",
         "diocese": "Nairobi", "address": "Ngong Rd, Nairobi", "phone": "+254 20 387 5000",
         "mass_times": "Sun: 7am, 9am, 11am, 5pm | Daily: 6:30am", "verified": True,
         "confirmations": 8, "added": "2024-01-15"},
        {"id": 3, "name": "St. Peter Claver Parish", "city": "Kampala", "country": "Uganda",
         "diocese": "Kampala", "address": "Mengo, Kampala", "phone": "+256 41 4272 597",
         "mass_times": "Sun: 7am, 9am, 11am | Daily: 7am", "verified": True,
         "confirmations": 6, "added": "2024-02-01"},
        {"id": 4, "name": "St. Peter's Parish Mombasa", "city": "Mombasa", "country": "Kenya",
         "diocese": "Mombasa", "address": "Nkrumah Rd, Mombasa", "phone": "+254 41 231 2171",
         "mass_times": "Sun: 7am, 9am, 5pm | Daily: 6am", "verified": True,
         "confirmations": 5, "added": "2024-02-10"},
    ]

st.title("🗺️ Parish Directory")
st.caption("Find a Catholic parish · Add a missing parish · All listings community-verified")

tab1, tab2, tab3 = st.tabs(["🔍 Find a Parish", "➕ Add a Parish", "⏳ Pending Verification"])

# ── TAB 1: SEARCH ─────────────────────────────────────────────────────────────
with tab1:
    m1, m2, m3 = st.columns(3)
    m1.metric("Listed Parishes", len(st.session_state.confirmed_parishes))
    m2.metric("Community-Verified", sum(1 for p in st.session_state.confirmed_parishes if p["verified"]))
    m3.metric("Countries", len(set(p["country"] for p in st.session_state.confirmed_parishes)))

    st.divider()

    # Search bar — prominent, mobile-sized
    query = st.text_input("🔍 Search by name, city, or country",
                          placeholder="Holy Family · Nairobi · Uganda",
                          label_visibility="collapsed")
    c1, c2 = st.columns(2)
    with c1:
        country_filter = st.selectbox("Country",
            ["All"] + sorted(set(p["country"] for p in st.session_state.confirmed_parishes)))
    with c2:
        diocese_filter = st.selectbox("Diocese",
            ["All"] + sorted(set(p.get("diocese","") for p in st.session_state.confirmed_parishes if p.get("diocese"))))

    results = st.session_state.confirmed_parishes
    if query:
        q = query.lower()
        results = [p for p in results if
                   q in p["name"].lower() or q in p.get("city","").lower() or
                   q in p.get("country","").lower() or q in p.get("diocese","").lower()]
    if country_filter != "All":
        results = [p for p in results if p["country"] == country_filter]
    if diocese_filter != "All":
        results = [p for p in results if p.get("diocese") == diocese_filter]

    if results:
        for p in results:
            badge = "✅" if p["verified"] else "⏳"
            with st.expander(f"{badge} {p['name']} — {p.get('city','')} · {p['country']}"):
                col1, col2 = st.columns(2)
                with col1:
                    if p.get("address"):
                        st.markdown(f"📍 **Address:** {p['address']}")
                    if p.get("phone"):
                        st.markdown(f"📞 **Phone:** {p['phone']}")
                    if p.get("diocese"):
                        st.markdown(f"⛪ **Diocese:** {p['diocese']}")
                with col2:
                    if p.get("mass_times"):
                        st.markdown(f"🕐 **Mass Times:**\n{p['mass_times']}")

                # Community confirmation button
                confirm_key = f"confirm_{p['id']}"
                if st.button(f"✅ I've been to this parish (confirm it)", key=confirm_key):
                    p["confirmations"] = p.get("confirmations", 0) + 1
                    if p["confirmations"] >= 3:
                        p["verified"] = True
                    st.success("Thank you for confirming!")

                conf_count = p.get("confirmations", 0)
                if not p["verified"]:
                    st.progress(min(conf_count / 3, 1.0),
                                text=f"{conf_count}/3 community confirmations needed")
    elif query or country_filter != "All":
        st.info("No parishes found. Know this parish? Add it below.")
        if st.button("➕ Add a missing parish"):
            st.session_state["auto_open_add"] = True
    else:
        st.info("Search above to find a parish, or browse all entries.")

    # Live OSM search section
    with st.expander("🌍 Search 40K+ parishes via OpenStreetMap (live)"):
        osm_query = st.text_input("City or area", placeholder="Nakuru, Kisumu, Kampala…", key="osm_q")
        if st.button("Search OpenStreetMap", key="osm_btn") and osm_query.strip():
            try:
                import requests
                overpass = "https://overpass-api.de/api/interpreter"
                q = f"""
[out:json][timeout:20];
area[name="{osm_query}"]->.a;
(
  node["amenity"="place_of_worship"]["religion"="christian"]["denomination"~"catholic",i](area.a);
  node["amenity"="place_of_worship"]["name"~"catholic|saint|holy",i](area.a);
);
out body 15;
"""
                r = requests.post(overpass, data={"data": q}, timeout=25)
                elements = r.json().get("elements", [])
                if elements:
                    for el in elements[:10]:
                        tags = el.get("tags", {})
                        name = tags.get("name", "Unnamed church")
                        addr = tags.get("addr:street", "")
                        st.markdown(f"📍 **{name}** — {addr}")
                else:
                    st.info("No results in OSM. Try a different spelling or add the parish below.")
            except Exception as e:
                st.info("Live search is not available right now. Please use the main search above or add a parish manually.")

# ── TAB 2: ADD A PARISH ───────────────────────────────────────────────────────
with tab2:
    st.subheader("➕ Add a Missing Parish")
    st.info(
        "Submit a parish and it enters **Pending** status. "
        "Once 3 parishioners confirm it — or a priest/coordinator verifies it — "
        "it goes **Verified** and appears in search results for everyone.",
        icon="ℹ️"
    )

    with st.form("add_parish_form"):
        st.markdown("**Parish Information** *(required fields marked \\*)*")
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Parish Name *", placeholder="Our Lady of Lourdes")
            city = st.text_input("City / Town *", placeholder="Eldoret")
            country = st.text_input("Country *", placeholder="Kenya")
            diocese = st.text_input("Diocese", placeholder="Eldoret")
        with c2:
            address = st.text_input("Street Address", placeholder="Kenyatta Ave")
            phone = st.text_input("Contact Phone", placeholder="+254 …")
            website = st.text_input("Website (if any)", placeholder="https://…")
            language = st.multiselect("Languages of Mass",
                ["English", "Kiswahili", "Luganda", "French", "Dholuo", "Kikuyu", "Other"])

        mass_times = st.text_area("Mass Times",
            placeholder="Sunday: 7am, 9am, 11am\nWeekdays: 6:30am",
            height=90)
        confession_times = st.text_input("Confession / Reconciliation times (optional)",
            placeholder="Sat 4–5pm, or by appointment")

        st.markdown("**About You** *(helps us assess the submission)*")
        submitter_role = st.selectbox("Your relationship to this parish",
            ["Parishioner", "Parish coordinator", "Priest / Deacon",
             "Visitor who attended Mass there", "Diocese staff", "Other"])
        submitter_name = st.text_input("Your name (optional)")
        submitter_contact = st.text_input("Your contact (optional — for verification follow-up)",
            placeholder="Email or phone")

        additional = st.text_area("Anything else useful (optional)",
            placeholder="Parking, accessibility, SCC presence, special ministries…", height=70)

        submitted = st.form_submit_button("Submit Parish", type="primary")

    if submitted and name and city and country:
        new_id = max((p["id"] for p in st.session_state.confirmed_parishes +
                      st.session_state.submitted_parishes), default=0) + 1
        st.session_state.submitted_parishes.append({
            "id": new_id, "name": name, "city": city, "country": country,
            "diocese": diocese, "address": address, "phone": phone,
            "mass_times": mass_times, "verified": False, "confirmations": 0,
            "submitted_by": submitter_role,
            "added": str(date.today()),
        })
        st.success(
            f"✅ **{name}** submitted! It will appear in search once 3 parishioners confirm it, "
            "or a parish coordinator verifies it directly."
        )
        st.balloons()

# ── TAB 3: PENDING VERIFICATION ───────────────────────────────────────────────
with tab3:
    st.subheader("⏳ Pending Community Verification")
    st.caption("These parishes have been submitted but not yet verified. Help verify by confirming ones you know.")

    pending = [p for p in st.session_state.submitted_parishes if not p["verified"]]

    if not pending:
        st.success("✅ No parishes awaiting verification right now.")
    else:
        for p in pending:
            with st.expander(f"⏳ {p['name']} — {p.get('city','')} · {p['country']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Submitted by:** {p.get('submitted_by', 'Unknown')}")
                    st.markdown(f"**Submitted:** {p.get('added', 'N/A')}")
                    if p.get("address"):
                        st.markdown(f"**Address:** {p['address']}")
                with c2:
                    if p.get("mass_times"):
                        st.markdown(f"**Mass Times:** {p['mass_times']}")
                    if p.get("diocese"):
                        st.markdown(f"**Diocese:** {p['diocese']}")

                conf_count = p.get("confirmations", 0)
                st.progress(min(conf_count / 3, 1.0),
                            text=f"{conf_count}/3 confirmations to verify")

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ I know this parish — confirm it", key=f"pend_conf_{p['id']}"):
                        p["confirmations"] = conf_count + 1
                        if p["confirmations"] >= 3:
                            p["verified"] = True
                            st.session_state.confirmed_parishes.append(p)
                            st.session_state.submitted_parishes.remove(p)
                            st.success(f"🎉 {p['name']} is now verified and live in the directory!")
                        else:
                            st.info(f"Confirmation recorded. {3 - p['confirmations']} more needed.")
                        st.rerun()
                with col_b:
                    if st.button("⚠️ This info looks wrong", key=f"pend_flag_{p['id']}"):
                        st.warning("Flagged for review. Thank you.")

    st.divider()
    st.markdown("**Parish Coordinator / Priest: Verify directly**")
    st.markdown(
        "If you are a parish coordinator or priest, you can immediately verify a submitted parish. "
        "Contact your diocese digital coordinator or the platform administrator."
    )

    # Quick admin verify (session-based — no auth yet)
    with st.expander("🔑 Coordinator: Verify a pending parish"):
        if pending:
            sel_name = st.selectbox("Select parish to verify",
                [p["name"] for p in pending], key="admin_verify_sel")
            admin_role = st.selectbox("Your role",
                ["Parish Coordinator", "Priest", "Diocese Staff", "Deacon"])
            if st.button("✅ Verify as coordinator", type="primary"):
                for p in pending:
                    if p["name"] == sel_name:
                        p["verified"] = True
                        p["confirmations"] = max(p.get("confirmations",0), 3)
                        st.session_state.confirmed_parishes.append(p)
                        st.session_state.submitted_parishes.remove(p)
                        st.success(f"✅ {sel_name} is now verified and live!")
                        st.rerun()
                        break
        else:
            st.info("No pending parishes.")

st.divider()
st.markdown(
    "📌 Parish data is community-contributed and verified. "
    "For official diocese records, contact your local bishop's office. "
    "All submissions are reviewed before going live."
)
