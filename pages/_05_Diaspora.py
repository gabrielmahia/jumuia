"""
🌏 Diaspora Connection
Find your cultural community. Connect globally. Stay rooted locally.
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

st.set_page_config(page_title="Diaspora", page_icon="🌏", layout="wide")

st.title("🌏 Diaspora Connection")
st.markdown("Find your cultural community. Connect globally. Stay rooted locally.")

DIASPORA = {
    "Filipino Catholic Diaspora": {
        "origin": "Philippines", "total": "12M+",
        "languages": ["Tagalog","Cebuano","Ilocano","English"],
        "justice_focus": ["Nurse / healthcare worker wages","Domestic worker rights","OFW remittance ethics"],
    },
    "Nigerian Catholic Diaspora": {
        "origin": "Nigeria", "total": "4M+",
        "languages": ["English","Igbo","Yoruba","Hausa"],
        "justice_focus": ["Healthcare worker brain drain","Remittance support","Anti-trafficking"],
    },
    "Kenyan / East African Diaspora": {
        "origin": "Kenya / Uganda / Tanzania", "total": "2M+",
        "languages": ["Swahili","Kikuyu","Luo","English","Luganda"],
        "justice_focus": ["Domestic worker rights","Living wage campaigns","Climate justice"],
    },
    "Korean Catholic Diaspora": {
        "origin": "South Korea", "total": "1.5M+",
        "languages": ["Korean","English"],
        "justice_focus": ["Migrant worker rights","Reunification advocacy"],
    },
    "Polish Catholic Diaspora": {
        "origin": "Poland", "total": "20M+",
        "languages": ["Polish","English"],
        "justice_focus": ["Migrant worker rights","Community preservation"],
    },
}

community = st.selectbox("Select your community", list(DIASPORA.keys()))
d = DIASPORA[community]

col1, col2 = st.columns(2)
with col1:
    st.metric("Origin", d["origin"])
    st.metric("Global Community", d["total"])
    st.markdown("**Languages:**")
    st.write(", ".join(d["languages"]))
with col2:
    st.markdown("**Justice focus areas:**")
    for j in d["justice_focus"]:
        st.write(f"⚖️ {j}")

st.divider()
st.markdown("### 🔍 Find Community Near You")

col1, col2 = st.columns([2,1])
with col1:
    your_city    = st.text_input("Your city", placeholder="London / Dubai / Toronto / Chicago")
    your_country = st.text_input("Country (optional)", placeholder="UK / UAE / Canada / USA")

if st.button("🔍 Find My Community", type="primary"):
    if your_city.strip():
        with st.spinner(f"Searching for {community} churches in {your_city}..."):
            try:
                from gospelmap.church_search import search_by_city
                churches = search_by_city(your_city.strip(), your_country.strip() or None, limit=12)
            except Exception:
                churches = []
                st.warning("Search is not available right now. Please try again shortly.")

        if not churches:
            st.warning(f"No churches found in {your_city}. Try a larger nearby city.")
        else:
            st.success(f"Found **{len(churches)} Catholic churches** in {your_city}")
            st.divider()
            for i, c in enumerate(churches[:10], 1):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.markdown(f"**{i}. {c.name}**")
                    if c.address:
                        st.caption(f"📍 {c.address}")
                with col2:
                    gmaps = f"https://www.google.com/maps?q={c.latitude},{c.longitude}"
                    st.markdown(f"[📍 Maps]({gmaps})")
                if c.phone:
                    st.caption(f"📞 {c.phone}")
                st.divider()
    else:
        st.warning("Enter your city to search")
