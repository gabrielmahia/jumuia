"""
📊 Ecosystem Health Dashboard
Real-time crisis signal indices for parishes and dioceses.
"""

import streamlit as st
import sys
sys.path.insert(0, ".")

# Guard plotly import
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

st.set_page_config(page_title="Ecosystem Health", page_icon="📊", layout="wide")

st.title("📊 Ecosystem Health Dashboard")
st.markdown("Real-time crisis signal indices for parishes and dioceses.")

st.divider()
st.markdown("### 🧮 Calculate Indices (Interactive)")
st.markdown("Enter your parish data to calculate actual health indices.")

with st.expander("📊 Pastoral Crisis Index (PCI) Calculator"):
    c1, c2, c3 = st.columns(3)
    with c1:
        priest_vacancies = st.number_input("Priest vacancies", 0, 50, 2)
        total_priests    = st.number_input("Current priests", 1, 100, 6)
    with c2:
        abuse_allegations= st.number_input("Abuse allegations (last 5 yrs)", 0, 50, 0)
        youth_pct        = st.slider("Youth engagement %", 0, 100, 20)
    with c3:
        integration_score= st.slider("Immigrant integration (0–10)", 0, 10, 5)
        opacity_score    = st.slider("Leadership opacity (0=transparent, 10=opaque)", 0, 10, 3)

    if st.button("Calculate PCI"):
        from gospelmap.indices import EcosystemIndices
        try:
            pci = EcosystemIndices.calculate_pastoral_crisis_index(
                priest_vacancies, total_priests, abuse_allegations,
                youth_pct, integration_score, opacity_score
            )
            level = "🔴 CRISIS" if pci >= 7 else "🟡 MONITOR" if pci >= 4 else "🟢 HEALTHY"
            st.metric("Pastoral Crisis Index", f"{pci:.1f} / 10", level)
            if pci >= 7:
                st.error("⚠️ Immediate pastoral intervention recommended.")
            elif pci >= 4:
                st.warning("📋 Monitor trends — targeted improvement possible.")
            else:
                st.success("✅ Parish showing healthy pastoral signals.")
        except Exception:
            st.info("This section is loading. Please refresh if it does not appear.")

with st.expander("💰 Financial Transparency Index (FTI) Calculator"):
    c1, c2 = st.columns(2)
    with c1:
        budget_public   = st.checkbox("Budget publicly available?", True)
        allocation_pub  = st.checkbox("Budget allocation published?", True)
        overhead_pct    = st.slider("Admin overhead %", 0, 50, 12)
    with c2:
        charitable_pct  = st.slider("% to charitable/pastoral work", 0, 100, 75)
        accountability  = st.selectbox("Accountability structure", ["None","Internal only","Lay council","External audit","All of the above"])

    if st.button("Calculate FTI"):
        score = 0
        if budget_public:   score += 2.5
        if allocation_pub:  score += 2.0
        if overhead_pct <= 15: score += 2.0
        elif overhead_pct <= 25: score += 1.0
        if charitable_pct >= 70: score += 2.0
        elif charitable_pct >= 50: score += 1.0
        acc_map = {"None":0,"Internal only":0.5,"Lay council":1.0,"External audit":1.5,"All of the above":2.0}
        score += acc_map.get(accountability, 0)
        score = min(score, 10)
        level = "🟢 Transparent" if score >= 7 else "🟡 Partial" if score >= 4 else "🔴 Opaque"
        st.metric("Financial Transparency Index", f"{score:.1f} / 10", level)

st.divider()
st.markdown("### 🗺️ Regional Health Overview")

if not PLOTLY_AVAILABLE:
    st.info("📊 Chart visualization requires plotly. Showing text summary instead:")
    REGIONAL_DATA = {
        "Nairobi Central":  {"pci":3.2,"mci":5.1,"jci":7.8,"fti":6.2},
        "Manila North":     {"pci":4.1,"mci":6.3,"jci":5.2,"fti":5.8},
        "São Paulo East":   {"pci":5.8,"mci":7.2,"jci":8.1,"fti":4.9},
        "Rome Historic":    {"pci":2.8,"mci":2.1,"jci":3.4,"fti":8.1},
        "Chicago West":     {"pci":6.2,"mci":4.8,"jci":6.9,"fti":5.5},
    }
    for region, d in REGIONAL_DATA.items():
        st.markdown(f"**{region}**: PCI {d['pci']}/10 | MCI {d['mci']}/10 | JCI {d['jci']}/10 | FTI {d['fti']}/10")
    st.caption("⚠️ DEMO: Sample indices. Connect real parish data via the Admin module.")
    st.stop()

# Regional dataset
REGIONAL_DATA = {
    "Nairobi Central":  {"pci":3.2,"mci":5.1,"jci":7.8,"fti":6.2},
    "Manila North":     {"pci":4.1,"mci":6.3,"jci":5.2,"fti":5.8},
    "São Paulo East":   {"pci":5.8,"mci":7.2,"jci":8.1,"fti":4.9},
    "Rome Historic":    {"pci":2.8,"mci":2.1,"jci":3.4,"fti":8.1},
    "Chicago West":     {"pci":6.2,"mci":4.8,"jci":6.9,"fti":5.5},
}

fig = go.Figure()
categories = ["PCI (Crisis)", "MCI (Material)", "JCI (Justice)", "FTI (Transparency)"]
palette    = ["#ef4444","#f97316","#22c55e","#3b82f6","#8b5cf6"]

for i, (region, d) in enumerate(REGIONAL_DATA.items()):
    vals = [d["pci"], d["mci"], d["jci"], d["fti"]]
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]], theta=categories + [categories[0]],
        fill="toself", name=region,
        line=dict(color=palette[i], width=1.5),
        fillcolor=f"rgba({int(palette[i][1:3],16)},{int(palette[i][3:5],16)},{int(palette[i][5:7],16)},0.15)",
    ))

fig.update_layout(
    polar=dict(radialaxis=dict(range=[0,10])),
    title="Ecosystem Health Radar — 5 Parish Regions (DEMO)",
    height=450,
)
st.plotly_chart(fig, use_container_width=True)

st.caption("⚠️ DEMO: Sample indices. Connect real parish data via the Admin module.")
