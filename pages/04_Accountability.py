"""
📋 Accountability Dashboard
Diocese transparency, finance, and synodality.
"""

import streamlit as st

# Guard plotly import
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

st.set_page_config(page_title="Accountability", page_icon="📋", layout="wide")

st.title("📋 Accountability Dashboard")
st.markdown("Diocese transparency, finance, and synodality — grounded in real public statistics.")
st.caption("*'Nothing hidden will not be revealed.'* — Luke 12:2")

try:
    from gospelmap.accountability_data import DIOCESES, DATA_SOURCES
except ImportError:
    DIOCESES = {
        "Nairobi, Kenya": {
            "leader": "Archbishop Philip Anyolo",
            "established": 1953,
            "catholics": 3200000,
            "parishes": 106,
            "priests_diocesan": 245,
            "priests_religious": 180,
            "permanent_deacons": 12,
            "women_religious": 1850,
            "catechists": 4200,
            "schools": 187,
            "hospitals_clinics": 24,
            "women_leadership_pct": 32,
            "youth_pct": 38,
            "fti": 6.2,
            "pci": 3.2,
            "jci": 7.8,
            "synod_score": 6.5,
            "budget_public": True,
            "data_quality": "EST",
            "source": "Vatican Yearbook 2022, KCCB estimates"
        }
    }
    DATA_SOURCES = []

diocese_list = list(DIOCESES.keys())
if not diocese_list:
    st.error("Accountability data module not loaded.")
    st.stop()

col_sel, col_qual = st.columns([3, 1])
with col_sel:
    diocese = st.selectbox("Select Diocese", diocese_list)
with col_qual:
    d = DIOCESES[diocese]
    badge = {"REAL":"🟢 Real data","EST":"🟡 Estimated","DEMO":"🔴 Demo"}
    st.metric("Data Quality", badge.get(d.get("data_quality","DEMO"), "—"))

d = DIOCESES[diocese]

st.divider()
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Financial Transparency", f"{d['fti']:.1f}/10", "FTI")
with col2: st.metric("Pastoral Health", f"{10-d['pci']:.1f}/10", "Inverse PCI")
with col3: st.metric("Justice Engagement", f"{d['jci']:.1f}/10", "JCI")
with col4: st.metric("Synodality Score", f"{d['synod_score']:.1f}/10", "Walking Together")

st.divider()
tab_overview, tab_stats, tab_finance = st.tabs(["📊 Overview", "📈 Statistics", "💰 Finance"])

with tab_overview:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Leader:** {d['leader']}")
        st.markdown(f"**Established:** {d['established']}")
        st.markdown(f"**Catholics:** {d['catholics']:,}")
        st.markdown(f"**Parishes:** {d['parishes']}")
        st.markdown(f"**Diocesan Priests:** {d['priests_diocesan']}")
    with col2:
        st.markdown(f"**Women Religious:** {d['women_religious']:,}")
        st.markdown(f"**Catechists:** {d['catechists']:,}")
        st.markdown(f"**Schools:** {d['schools']}")
        st.markdown(f"**Women in leadership:** {d['women_leadership_pct']}%")
        st.markdown(f"**Youth engagement:** {d['youth_pct']}%")

    st.divider()
    if PLOTLY_AVAILABLE:
        fig = go.Figure(go.Scatterpolar(
            r=[d['fti'], 10-d['pci'], d['jci'], d['synod_score'], d['fti']],
            theta=["Transparency","Pastoral Health","Justice","Synodality","Transparency"],
            fill="toself", line_color="#3b82f6", fillcolor="rgba(59,130,246,0.2)"
        ))
        fig.update_layout(polar=dict(radialaxis=dict(range=[0,10])),
                          title="Ecosystem Health Radar", height=350)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("**📊 Ecosystem Health Summary:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Transparency", f"{d['fti']}/10", "FTI")
        with col2: st.metric("Pastoral Health", f"{10-d['pci']}/10", "Inverse PCI")
        with col3: st.metric("Justice", f"{d['jci']}/10", "JCI")
        with col4: st.metric("Synodality", f"{d['synod_score']}/10", "Walking Together")

with tab_stats:
    st.markdown("### Key Statistics")
    cpp = d['catholics'] // max(d['parishes'], 1)
    total_priests = d['priests_diocesan'] + d['priests_religious']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Catholics per Parish", f"{cpp:,}")
    with col2:
        st.metric("Total Priests", total_priests)
    with col3:
        cp_ratio = d['catholics'] // max(total_priests, 1)
        st.metric("Catholics per Priest", f"{cp_ratio:,}")

with tab_finance:
    st.markdown("### 💰 Financial Transparency")
    bp = d.get('budget_public', False)
    st.metric("Budget publicly available",
              "✅ Yes — full or partial disclosure" if bp else "❌ No public disclosure found")
    
    if not bp:
        st.error("⚠️ No public budget found for this diocese.")
    else:
        st.success("✅ Some budget information publicly available.")
    
    st.markdown(f"**FTI Score: {d['fti']:.1f}/10**")
