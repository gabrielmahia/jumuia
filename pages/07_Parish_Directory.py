"""Parish Directory — Search Catholic Parishes Worldwide"""
import streamlit as st
import sys
sys.path.insert(0, ".")

from services.directory_service import init_db, search_parishes, get_stats, sync_gcatholic

st.set_page_config(page_title="Parish Directory — CNT", page_icon="🗺️", layout="wide")

# Init DB on first load
init_db()

st.title("🗺️ Parish Directory")

# Stats bar
stats = get_stats()
col1, col2, col3 = st.columns(3)
col1.metric("Total Parishes", f"{stats['total']:,}")
col2.metric("Verified Listings", f"{stats['verified']:,}")
col3.metric("Countries Covered", len(stats["top_countries"]))

st.caption(
    "**Current directory:** Seed data with ~500 parishes worldwide. "
    "More parishes are being added continuously via OpenStreetMap and community contributions."
)
st.divider()

# ─────────────────────────────────────────────
# SEARCH
# ─────────────────────────────────────────────
st.subheader("Search Parishes")

col1, col2, col3 = st.columns([3, 2, 2])
with col1:
    query = st.text_input("Search by name, city, or address", placeholder="e.g. Holy Family, Nairobi")
with col2:
    diocese_filter = st.text_input("Diocese", placeholder="e.g. Nairobi")
with col3:
    country_options = [""] + [r["country"] for r in stats["top_countries"] if r["country"]]
    country_filter = st.selectbox("Country", country_options)

if st.button("Search", type="primary") or query or diocese_filter or country_filter:
    results = search_parishes(query, country_filter, diocese_filter, limit=50)

    if results:
        st.success(f"Found {len(results)} parish(es)")
        for p in results:
            with st.expander(f"{'✅ ' if p['verified'] else ''}{p['name']} — {p['city']}, {p['country']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Diocese:** {p.get('diocese') or '—'}")
                    st.markdown(f"**Address:** {p.get('address') or '—'}")
                    st.markdown(f"**Phone:** {p.get('phone') or '—'}")
                with col2:
                    st.markdown(f"**Mass Times:** {p.get('mass_times') or '—'}")
                    st.markdown(f"**Languages:** {p.get('languages') or '—'}")
                    if p.get("website"):
                        st.markdown(f"**Website:** [{p['website']}]({p['website']})")
                st.caption(f"Source: {p.get('source', 'seed')} | ID: {p['id']}")
    else:
        st.info("No parishes found. Try a broader search.")

st.divider()

st.info("💡 **Want to add your parish?** Contact us or contribute via our community portal.")

