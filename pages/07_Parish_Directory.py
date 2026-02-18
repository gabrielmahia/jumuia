"""Parish Directory — Search + GCatholic Integration Status"""
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
    "**DEMO DATA** — Current directory uses seed data (~500 parishes). "
    "GCatholic integration (100K+ parishes) is in rails — see status below."
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

# ─────────────────────────────────────────────
# GCATHOLIC INTEGRATION STATUS
# ─────────────────────────────────────────────
st.subheader("🔗 GCatholic Integration Status")
status = sync_gcatholic(dry_run=True)

st.warning(f"**Status: {status['status']}** — {status['message']}", icon="🔧")

st.markdown("**Activation path to 100K+ parishes:**")
for step in status.get("next_steps", []):
    st.markdown(f"- {step}")

with st.expander("Data source alternatives (ranked by openness)"):
    st.markdown("""
| Source | Parishes | Open? | API? | Notes |
|--------|----------|-------|------|-------|
| **OpenStreetMap** (amenity=place_of_worship, denomination=catholic) | ~40K+ | ✅ Open | ✅ Overpass API | Best starting point |
| **GCatholic.org** | 100K+ | ❌ ToS review needed | ❌ Scraping only | Richest dataset |
| **The Catholic Directory** | ~18K US | Partial | ❌ | US-focused |
| **Wikipedia categories** | Varies | ✅ Open | ✅ | Incomplete, good for cathedrals |
| **Manual submissions** | As contributed | ✅ | n/a | Community-verified |

**Recommended immediate path:** Import from OpenStreetMap via Overpass API.
See `docs/GCATHOLIC_INTEGRATION_GUIDE.md` for all options.
    """)
