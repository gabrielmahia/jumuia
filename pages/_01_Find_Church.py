"""
🔍 Find My Local Church
Search by location, values, and accessibility. Powered by OpenStreetMap.
"""

import streamlit as st
import sys
sys.path.insert(0, ".")

st.set_page_config(page_title="Find My Church", page_icon="🔍", layout="wide")

st.title("🔍 Find My Local Church")
st.markdown("Search by location, values, and accessibility. Powered by OpenStreetMap — real global data, no API key required.")

col1, col2 = st.columns([1, 1])
with col1:
    city    = st.text_input("City", placeholder="Nairobi / Manila / São Paulo / Rome")
    country = st.text_input("Country (optional, improves accuracy)", placeholder="Kenya / Philippines / Brazil")
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

if search_btn:
    if not city.strip():
        st.warning("Please enter a city name")
    else:
        with st.spinner(f"Searching for Catholic churches in {city}... (OSM live data)"):
            try:
                from gospelmap.church_search import search_by_city
                churches = search_by_city(city.strip(), country.strip() or None, limit=15)
            except Exception:
                churches = []
                st.warning("Search is not available right now. Please check your connection and try again.")

        if not churches:
            st.warning(f"No churches found in {city}. Try a larger city or different spelling.")
            st.info("💡 OSM coverage varies by region. Major cities in East Africa, Philippines, Brazil, Europe have good coverage.")
        else:
            st.success(f"Found **{len(churches)} Catholic churches** near {city}")
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
                    st.divider()

st.info("""
**Data Source:** OpenStreetMap (crowdsourced, real-time)
Coverage is best in Europe and East Africa, growing globally.
Help improve coverage: [openstreetmap.org](https://openstreetmap.org)
""")
