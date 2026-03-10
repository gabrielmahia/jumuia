"""
⚖️ Justice Network
Global coordination of Catholic social action campaigns.
"""

import streamlit as st

# ── Mobile CSS ──────────────────────────────────────────────────────────────
import sys as _sys
_sys.path.insert(0, ".")
try:
    from services.mobile_ux import inject_mobile_css as _inj; _inj()
except Exception:
    pass


st.set_page_config(page_title="Justice Network", page_icon="⚖️", layout="wide")

st.title("⚖️ Justice Network")
st.markdown("Global coordination of Catholic social action campaigns.")

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Active Campaigns", "54")
with col2: st.metric("Workers Benefited", "26,000+")
with col3: st.metric("Parishes Involved", "890+")
with col4: st.metric("Policy Wins (2025)", "7")

st.divider()

campaigns = [
    {
        "name": "Living Wage — Tea Farmers",
        "region": "Kenya",
        "status": "🟢 Active",
        "parishes": 89,
        "workers": 3000,
        "progress": "WON: Kiambu +25%, Nyeri +28% | Negotiating: Murang'a, Embu",
    },
    {
        "name": "Refugee Rights — East Africa",
        "region": "Uganda / Kenya",
        "status": "🟢 Active",
        "parishes": 134,
        "workers": 8500,
        "progress": "230 parishes welcoming | 1,200 people housed | Legal support expanding",
    },
    {
        "name": "Farmworker Wages — USA",
        "region": "Virginia, NC, GA",
        "status": "🟡 Organizing",
        "parishes": 47,
        "workers": 4200,
        "progress": "WON: Virginia +$2/hr | Organizing: North Carolina, Georgia",
    },
    {
        "name": "Housing Justice",
        "region": "Global (12 cities)",
        "status": "🟢 Active",
        "parishes": 210,
        "workers": 12000,
        "progress": "São Paulo, Chicago, Manila, Lagos — 4,300 families supported",
    },
]

for camp in campaigns:
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"#### {camp['name']}")
            st.caption(f"📍 {camp['region']} · {camp['status']}")
            st.write(camp["progress"])
        with col2:
            st.metric("Parishes", camp["parishes"])
            st.metric("People", f"{camp['workers']:,}")
        with col3:
            if st.button("Join Campaign", key=f"join_{camp['name'][:10]}"):
                st.success("✅ You've joined! You'll receive action alerts and coordination updates.")
        st.divider()

st.markdown("### ➕ Submit a Justice Campaign")
with st.expander("Propose a new campaign for coordination"):
    c1, c2 = st.columns(2)
    with c1:
        cam_name    = st.text_input("Campaign name")
        cam_region  = st.text_input("Region / Country")
        cam_issue   = st.selectbox("Issue area", ["Living wage","Housing","Refugee rights","Healthcare","Education","Environmental","Racial justice","Other"])
    with c2:
        cam_workers = st.number_input("People directly affected", 0, 1000000, 1000)
        cam_parishes= st.number_input("Parishes already involved", 0, 10000, 5)
        cam_desc    = st.text_area("Description")
    if st.button("Submit Campaign"):
        if cam_name and cam_region:
            st.success(f"✅ Campaign '{cam_name}' submitted for network review.")
