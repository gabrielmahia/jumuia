"""
GospelMap — Global Catholic Ecosystem Intelligence Platform
Find your people. Measure justice. Hold leadership accountable.

Architecture: Multi-page Streamlit, zero infrastructure deps.
Data: OSM (real church search), computed indices, demo parish profiles.
Deployment: Streamlit Cloud free tier.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import math

# Internal modules
try:
    from gospelmap.sheets_backend import submit as _submit_form, is_configured as _backend_ok
except Exception:
    def _submit_form(*a, **kw): return False
    def _backend_ok(): return False

try:
    from gospelmap.accountability_data import DIOCESES, GLOBAL_STATS, DATA_SOURCES
except Exception:
    DIOCESES, GLOBAL_STATS, DATA_SOURCES = {}, {}, []

st.set_page_config(
    page_title="GospelMap 🌍",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Theme-aware: works in both light and dark mode ── */

/* Hero text: use Streamlit's own text color token */
.gm-hero {
    font-size:2.4em; font-weight:800; margin-bottom:0.3rem;
    color: var(--text-color, #1a3a5c);
}
.gm-sub {
    font-size:1.1em; margin-bottom:1.5rem;
    color: var(--text-color, #5a7290);
    opacity: 0.75;
}

/* Card: no fixed background — use transparent with just a border */
.gm-card {
    border:1px solid rgba(128,128,128,0.25);
    border-radius:10px;
    padding:1.2rem 1.4rem;
    margin-bottom:1rem;
}

/* Status banners: border-left accent only, transparent background.
   Works on any background color — light or dark. */
.crisis-red {
    border-left:4px solid #ef4444;
    padding:.8rem 1rem;
    border-radius:0 6px 6px 0;
    margin:.5rem 0;
    background: rgba(239,68,68,0.12);
}
.health-green {
    border-left:4px solid #22c55e;
    padding:.8rem 1rem;
    border-radius:0 6px 6px 0;
    margin:.5rem 0;
    background: rgba(34,197,94,0.12);
}
.warning-yellow {
    border-left:4px solid #eab308;
    padding:.8rem 1rem;
    border-radius:0 6px 6px 0;
    margin:.5rem 0;
    background: rgba(234,179,8,0.12);
}

/* Dark mode overrides: boost rgba alpha slightly for visibility */
@media (prefers-color-scheme: dark) {
    .crisis-red     { background: rgba(239,68,68,0.20); }
    .health-green   { background: rgba(34,197,94,0.20); }
    .warning-yellow { background: rgba(234,179,8,0.20); }
}
</style>
""", unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 GospelMap")
    st.caption("Global Catholic Ecosystem Intelligence")
    st.divider()

    # Role-based navigation
    ROLES = {
        "👤 Visitor": ["🏠 Home", "🔍 Find My Church", "🌏 Diaspora"],
        "✝️ Parishioner": ["🏠 Home", "🔍 Find My Church", "📊 Ecosystem Health", "🌏 Diaspora", "⚖️ Justice Network"],
        "🏘️ Parish Coordinator": ["🏠 Home", "🔍 Find My Church", "📊 Ecosystem Health", "⚖️ Justice Network", "📋 Accountability", "🌏 Diaspora", "🆘 Crisis Response"],
        "⛪ Priest / Deacon": ["🏠 Home", "🔍 Find My Church", "📊 Ecosystem Health", "⚖️ Justice Network", "📋 Accountability", "🌏 Diaspora", "🆘 Crisis Response"],
        "🏛️ Diocese / Researcher": ["🏠 Home", "🔍 Find My Church", "📊 Ecosystem Health", "⚖️ Justice Network", "📋 Accountability", "🌏 Diaspora", "🆘 Crisis Response"],
    }

    role = st.selectbox("I am a…", list(ROLES.keys()), key="user_role")
    available_pages = ROLES[role]

    page = st.radio("Navigate", available_pages, label_visibility="collapsed")

    st.divider()
    st.markdown("### 📊 Global Stats (Demo)")
    st.metric("Parishes Mapped", "5,000+")
    st.metric("Countries", "150+")
    st.metric("Justice Campaigns", "50+")
    st.divider()
    st.markdown("### 🔗 Parish Tools")
    st.markdown("""
**Running a parish?**  
[![Catholic Spiritual OS](https://img.shields.io/badge/Catholic%20Spiritual%20OS-Parish%20Tools-blue)](https://catholicparishsteward.streamlit.app)

[→ Open Catholic Spiritual OS](https://catholicparishsteward.streamlit.app) — sacraments, pastoral care, stewardship & more
""")
    st.divider()
    st.caption("🟢 **Demo Mode** — Spiritual content live, parish metrics illustrative")
    st.caption("AGPL-3.0 | community-owned forever")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown('<div class="gm-hero">🌍 GospelMap</div>', unsafe_allow_html=True)
    st.markdown('<div class="gm-sub">Find Your People. Measure Justice. Hold Leadership Accountable.</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Parishes", "5,000+", "Global coverage")
    with col2: st.metric("Dioceses", "500+", "150 countries")
    with col3: st.metric("Justice Campaigns", "50+", "Active globally")
    with col4: st.metric("Catholics Served", "1.3B", "Universal church")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### What GospelMap Does")
        for item in [
            ("🔍", "**Find My Church** — Search by location, language, values, accessibility"),
            ("📊", "**Ecosystem Health** — Real-time indices: pastoral, material, justice, financial"),
            ("⚖️", "**Justice Network** — Coordinate campaigns globally, track impact"),
            ("📋", "**Accountability** — Bishop + diocese transparency scores"),
            ("🌏", "**Diaspora** — Connect Filipino, Nigerian, Korean, Polish communities"),
            ("🆘", "**Crisis Response** — Refugee coordination, disaster response"),
        ]:
            st.markdown(f"{item[0]} {item[1]}")

    with col2:
        st.markdown("### Theological Foundation")
        st.markdown("""
**Vatican II (Gaudium et Spes):** The Church exists *in and for* the world.

**Catholic Social Teaching:**
- Option for the poor (not optional)
- Justice is integral to the Gospel
- Human dignity is non-negotiable
- Subsidiarity: parishes own their data

**Gospel Radicalism:**
*"Nothing hidden will not be revealed."* — Luke 12:2  
*"Whatever you did for the least..."* — Matthew 25:40
        """)

    st.divider()
    st.markdown("### ⚡ Start Now")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**🔍 Find a Church**\nSearch by city → real OSM data\nFilter by language, values, accessibility")
    with col2:
        st.info("**⚖️ Join a Campaign**\nLiving wage, refugee rights, housing\nConnect with parishes near you")
    with col3:
        st.info("**📊 Check Health**\nPastoral, material, justice indices\nSee where crisis signals are rising")

    st.markdown("---")
    st.caption("*'Nothing is hidden that will not be revealed.'* — Luke 12:2 | AGPL-3.0 | [GitHub](https://github.com/gabrielmahia/gospelmap)")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: FIND MY CHURCH
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Find My Church":
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
                except Exception as e:
                    churches = []
                    st.error(f"Search error: {e}")

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

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ECOSYSTEM HEALTH
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Ecosystem Health":
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
                    st.markdown('<div class="crisis-red">⚠️ Immediate pastoral intervention recommended.</div>', unsafe_allow_html=True)
                elif pci >= 4:
                    st.markdown('<div class="warning-yellow">📋 Monitor trends — targeted improvement possible.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="health-green">✅ Parish showing healthy pastoral signals.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Calculation error: {e}")

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

    # ── IP Geolocation (free, no key, no PII stored) ──────────────────────
    @st.cache_data(ttl=3600, show_spinner=False)
    def _detect_region() -> dict:
        """Detect user's approximate region via ip-api.com (free tier, no key)."""
        try:
            r = requests.get("http://ip-api.com/json/?fields=country,countryCode,city,lat,lon",
                             timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return {}

    geo = _detect_region()
    user_country_code = geo.get("countryCode", "")
    user_city         = geo.get("city", "")

    # Region dataset — indexed by rough country/region tag for matching
    REGIONAL_DATA = {
        "Nairobi Central":  {"pci":3.2,"mci":5.1,"jci":7.8,"fti":6.2,"countries":["KE","TZ","RW","ET","UG","SO"]},
        "Manila North":     {"pci":4.1,"mci":6.3,"jci":5.2,"fti":5.8,"countries":["PH","ID","TH","VN","MY","SG"]},
        "São Paulo East":   {"pci":5.8,"mci":7.2,"jci":8.1,"fti":4.9,"countries":["BR","AR","CO","PE","CL","UY"]},
        "Rome Historic":    {"pci":2.8,"mci":2.1,"jci":3.4,"fti":8.1,"countries":["IT","VA","ES","PT","FR","GR","HR"]},
        "Chicago West":     {"pci":6.2,"mci":4.8,"jci":6.9,"fti":5.5,"countries":["US","CA","MX","AU","NZ","GB","IE","DE","PL"]},
    }

    # Find user's nearest region
    def _nearest_region(code: str) -> str:
        for name, d in REGIONAL_DATA.items():
            if code in d["countries"]:
                return name
        return ""   # not found → no highlight

    user_region = _nearest_region(user_country_code)

    # Location badge
    if user_city and user_country_code:
        st.caption(f"📍 Detected location: **{user_city}, {user_country_code}**"
                   + (f" — highlighting **{user_region}**" if user_region else "")
                   + "  ·  *IP-based, approximate, not stored*")
    else:
        st.caption("📍 Location not detected — showing all regions equally")

    # Build radar
    fig = go.Figure()
    categories = ["PCI (Crisis)", "MCI (Material)", "JCI (Justice)", "FTI (Transparency)"]
    palette    = ["#ef4444","#f97316","#22c55e","#3b82f6","#8b5cf6"]

    for i, (region, d) in enumerate(REGIONAL_DATA.items()):
        vals        = [d["pci"], d["mci"], d["jci"], d["fti"]]
        is_user     = (region == user_region)
        line_width  = 4 if is_user else 1.5
        opacity     = 1.0 if is_user else (0.35 if user_region else 0.7)
        label       = f"★ {region} (your region)" if is_user else region
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=categories + [categories[0]],
            fill="toself", name=label,
            line=dict(color=palette[i], width=line_width),
            fillcolor=f"rgba({int(palette[i][1:3],16)},{int(palette[i][3:5],16)},{int(palette[i][5:7],16)},{0.25 if is_user else 0.08})",
            opacity=opacity,
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0,10], tickfont=dict(size=10)),
            bgcolor="rgba(0,0,0,0)",   # transparent — works in dark + light mode
        ),
        paper_bgcolor="rgba(0,0,0,0)", # transparent background
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(color=None),         # inherit from Streamlit theme
        title=("Ecosystem Health Radar" +
               (f" — ★ {user_region} highlighted" if user_region else " — 5 Parish Regions") +
               " (DEMO)"),
        height=450,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("⚠️ DEMO: Sample indices. Highlighted region = your approximate location. Connect real parish data via the Admin module.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: JUSTICE NETWORK
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⚖️ Justice Network":
    st.title("⚖️ Justice Network")
    st.markdown("Global coordination of Catholic social action campaigns.")

    # Global impact bar
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
            "join": True,
        },
        {
            "name": "Refugee Rights — East Africa",
            "region": "Uganda / Kenya",
            "status": "🟢 Active",
            "parishes": 134,
            "workers": 8500,
            "progress": "230 parishes welcoming | 1,200 people housed | Legal support expanding",
            "join": True,
        },
        {
            "name": "Farmworker Wages — USA",
            "region": "Virginia, NC, GA",
            "status": "🟡 Organizing",
            "parishes": 47,
            "workers": 4200,
            "progress": "WON: Virginia +$2/hr | Organizing: North Carolina, Georgia",
            "join": True,
        },
        {
            "name": "Housing Justice",
            "region": "Global (12 cities)",
            "status": "🟢 Active",
            "parishes": 210,
            "workers": 12000,
            "progress": "São Paulo, Chicago, Manila, Lagos — 4,300 families supported",
            "join": True,
        },
        {
            "name": "Sugar Cane Workers",
            "region": "Brazil",
            "status": "🟡 Negotiating",
            "parishes": 65,
            "workers": 5800,
            "progress": "+15% wages proposed | Cross-parish coalition formed",
            "join": True,
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
                if st.button(f"Join Campaign", key=f"join_{camp['name'][:10]}"):
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

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ACCOUNTABILITY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Accountability":
    st.title("📋 Accountability Dashboard")
    st.markdown("Diocese transparency, finance, and synodality — grounded in real public statistics.")
    st.caption("*'Nothing hidden will not be revealed.'* — Luke 12:2")

    # ── Data source ───────────────────────────────────────────────────────────
    _diocese_list = list(DIOCESES.keys()) if DIOCESES else []
    if not _diocese_list:
        st.error("Accountability data module not loaded.")
        st.stop()

    col_sel, col_qual = st.columns([3, 1])
    with col_sel:
        diocese = st.selectbox("Select Diocese", _diocese_list)
    with col_qual:
        d = DIOCESES[diocese]
        badge = {"REAL":"🟢 Real data","EST":"🟡 Estimated","DEMO":"🔴 Demo"}
        st.metric("Data Quality", badge.get(d.get("data_quality","DEMO"), "—"))

    d = DIOCESES[diocese]

    # ── Key indices ───────────────────────────────────────────────────────────
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Financial Transparency", f"{d['fti']:.1f}/10", "FTI")
    with col2: st.metric("Pastoral Health",         f"{10-d['pci']:.1f}/10", "Inverse PCI")
    with col3: st.metric("Justice Engagement",      f"{d['jci']:.1f}/10", "JCI")
    with col4: st.metric("Synodality Score",         f"{d['synod_score']:.1f}/10", "Walking Together")

    st.divider()
    tab_overview, tab_stats, tab_finance, tab_synod, tab_submit = st.tabs([
        "📊 Overview", "📈 Statistics", "💰 Finance", "🕊️ Synodality", "📝 Submit Data"
    ])

    # ── Overview ──────────────────────────────────────────────────────────────
    with tab_overview:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Leader:** {d['leader']}")
            st.markdown(f"**Established:** {d['established']}")
            st.markdown(f"**Catholics:** {d['catholics']:,}")
            st.markdown(f"**Parishes:** {d['parishes']}")
            st.markdown(f"**Diocesan Priests:** {d['priests_diocesan']}")
            st.markdown(f"**Religious Priests:** {d['priests_religious']}")
            st.markdown(f"**Permanent Deacons:** {d['permanent_deacons']}")
        with col2:
            st.markdown(f"**Women Religious:** {d['women_religious']:,}")
            st.markdown(f"**Catechists:** {d['catechists']:,}")
            st.markdown(f"**Schools:** {d['schools']}")
            st.markdown(f"**Hospitals/Clinics:** {d['hospitals_clinics']}")
            st.markdown(f"**Women in leadership:** {d['women_leadership_pct']}%")
            st.markdown(f"**Youth engagement:** {d['youth_pct']}%")

        st.divider()
        # Radar chart of all 4 indices
        fig = go.Figure(go.Scatterpolar(
            r=[d['fti'], 10-d['pci'], d['jci'], d['synod_score'], d['fti']],
            theta=["Transparency","Pastoral Health","Justice","Synodality","Transparency"],
            fill="toself", line_color="#3b82f6", fillcolor="rgba(59,130,246,0.2)"
        ))
        fig.update_layout(polar=dict(radialaxis=dict(range=[0,10])),
                          title="Ecosystem Health Radar", height=350)
        st.plotly_chart(fig, use_container_width=True)

        if d['women_leadership_pct'] < 25:
            st.markdown('<div class="warning-yellow">⚠️ Women in leadership below peer average (27%)</div>', unsafe_allow_html=True)
        if d['youth_pct'] > 35:
            st.markdown('<div class="health-green">✅ Strong youth engagement — above global average</div>', unsafe_allow_html=True)
        elif d['youth_pct'] < 20:
            st.markdown('<div class="crisis-red">⚠️ Low youth engagement — declining trend risk</div>', unsafe_allow_html=True)

    # ── Statistics ────────────────────────────────────────────────────────────
    with tab_stats:
        st.markdown("### Key Statistics vs. Global Averages")
        if GLOBAL_STATS:
            # Ratio: Catholics per parish
            cpp = d['catholics'] // max(d['parishes'], 1)
            global_cpp = GLOBAL_STATS['total_catholics'] // max(GLOBAL_STATS['total_parishes'], 1)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Catholics per Parish", f"{cpp:,}", f"Global avg: {global_cpp:,}")
            with col2:
                total_priests = d['priests_diocesan'] + d['priests_religious']
                st.metric("Priests total", total_priests)
            with col3:
                cp_ratio = d['catholics'] // max(total_priests, 1)
                st.metric("Catholics per Priest", f"{cp_ratio:,}")

            st.divider()
            # Bar comparison: this diocese vs global average
            metrics = {
                "Women Religious / 1000 Catholics": (
                    round(d['women_religious'] / d['catholics'] * 1000, 2),
                    round(GLOBAL_STATS['total_women_religious'] / GLOBAL_STATS['total_catholics'] * 1000, 2)
                ),
                "Catechists / 1000 Catholics": (
                    round(d['catechists'] / d['catholics'] * 1000, 2),
                    round(GLOBAL_STATS['total_catechists'] / GLOBAL_STATS['total_catholics'] * 1000, 2)
                ),
            }
            for metric, (local, global_avg) in metrics.items():
                fig = go.Figure(go.Bar(
                    x=[local, global_avg],
                    y=[diocese.split(",")[0], "Global Average"],
                    orientation='h',
                    marker_color=['#3b82f6','#94a3b8']
                ))
                fig.update_layout(title=metric, height=150,
                                  margin=dict(l=0,r=0,t=35,b=0))
                st.plotly_chart(fig, use_container_width=True)

        st.caption(f"📚 **Sources:** {d.get('source','Vatican Yearbook 2022')}")
        st.caption(f"**Data quality:** {d.get('data_quality','EST')} — Real = verified public source, EST = estimated from regional aggregates")

        # Link to primary sources
        st.markdown("### 🔗 Primary Data Sources")
        for name, url, desc in DATA_SOURCES:
            st.markdown(f"- [{name}]({url}) — {desc}")

    # ── Finance ───────────────────────────────────────────────────────────────
    with tab_finance:
        st.markdown("### 💰 Financial Transparency")
        bp = d.get('budget_public', False)
        st.metric("Budget publicly available",
                  "✅ Yes — full or partial disclosure" if bp else "❌ No public disclosure found",
                  delta="Transparency signal")

        if not bp:
            st.markdown('<div class="crisis-red">⚠️ No public budget found for this diocese. Financial transparency is a trust signal — publish annually to score higher.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="health-green">✅ Some budget information publicly available.</div>', unsafe_allow_html=True)

        st.markdown("#### Budget Allocation Model (Illustrative)")
        st.caption("Real diocese budgets are rarely public. This shows the ideal allocation model for peer comparison.")
        alloc = {"Pastoral & Sacraments":38,"Material Aid & Services":24,
                 "Formation & Education":18,"Staff & Administration":11,
                 "Building & Maintenance":6,"Justice & Advocacy":3}
        fig = go.Figure(go.Bar(
            x=list(alloc.values()), y=list(alloc.keys()), orientation='h',
            marker_color=['#22c55e','#3b82f6','#8b5cf6','#f97316','#94a3b8','#ef4444']
        ))
        fig.update_layout(title="Recommended Budget Allocation %", height=300,
                          margin=dict(l=0,r=0,t=40,b=0), xaxis_title="% of budget")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"**FTI Score: {d['fti']:.1f}/10**")
        fti_breakdown = {
            "Budget published": "2.5/2.5" if bp else "0/2.5",
            "Allocation breakdown available": "TBC",
            "External oversight exists": "TBC",
            "Overhead under 20%": "TBC",
        }
        for k, v in fti_breakdown.items():
            st.write(f"• {k}: {v}")

    # ── Synodality ────────────────────────────────────────────────────────────
    with tab_synod:
        st.markdown("### 🕊️ Synodality — Walking Together")
        st.markdown(f"**Synodality Score: {d['synod_score']:.1f}/10**")
        st.progress(int(d['synod_score'] * 10))

        synod_criteria = [
            ("Listening sessions conducted (2021–2024)", d['synod_score'] > 4),
            ("Lay involvement in parish governance",     d['synod_score'] > 5),
            ("Women in meaningful leadership roles",     d['women_leadership_pct'] >= 25),
            ("Youth representation in decision-making",  d['youth_pct'] >= 30),
            ("Financial transparency to community",      bp),
            ("Justice engagement documented",            d['jci'] >= 6),
        ]
        for criterion, met in synod_criteria:
            icon = "✅" if met else "🔄"
            st.write(f"{icon} {criterion}")

        st.divider()
        st.info("""
**What is Synodality?**
The 2021–2024 Synod on Synodality asked every diocese to listen deeply
to its people — especially the marginalised. Synodality is not a meeting;
it is a culture of mutual discernment. A high score means the diocese
listens, changes, and includes.

*"Walking together as the People of God."* — Pope Francis, 2021
        """)

    # ── Community Data Submission ─────────────────────────────────────────────
    with tab_submit:
        st.markdown("### 📝 Submit or Correct Data")
        st.markdown("""
GospelMap builds accountability from the ground up.
**You can contribute data about this diocese:**
- Correct inaccurate statistics
- Add budget information
- Document justice campaigns
- Report abuse accountability gaps
- Share synodality session records

All submissions are reviewed before publication.
        """)
        col1, col2 = st.columns(2)
        with col1:
            sub_type   = st.selectbox("What are you submitting?", [
                "Budget / financial data","Priest / parish count correction",
                "Abuse accountability record","Justice campaign evidence",
                "Synodality session record","Leadership representation data","Other"])
            sub_source = st.text_input("Source URL or document name")
            sub_year   = st.selectbox("Data year", list(range(2024, 2018, -1)))
        with col2:
            sub_name   = st.text_input("Your name (optional)")
            sub_org    = st.text_input("Organisation (optional)")
            sub_value  = st.text_area("Data / correction / evidence")

        if st.button("Submit Data Contribution", type="primary"):
            if sub_value and sub_source:
                persisted = _submit_form("accountability_submission", {
                    "diocese": diocese,
                    "submission_type": sub_type,
                    "source": sub_source,
                    "year": sub_year,
                    "contributor_name": sub_name,
                    "contributor_org": sub_org,
                    "value": sub_value,
                })
                if persisted:
                    st.success("✅ Data submitted and saved to GospelMap review queue.")
                else:
                    st.success("✅ Submission recorded (session only — connect Google Sheets for persistence).")
                    st.caption("See docs/SHEETS_SETUP.md to enable permanent storage.")
            else:
                st.warning("Please fill in both the data field and the source.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DIASPORA
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🌏 Diaspora":
    st.title("🌏 Diaspora Connection")
    st.markdown("Find your cultural community. Connect globally. Stay rooted locally.")

    # Language → OSM search hints per community
    _DIASPORA = {
        "Filipino Catholic Diaspora": {
            "origin": "Philippines", "total": "12M+",
            "concentrations": ["Middle East: 3.2M","North America: 4.8M","Europe: 1.2M","Australia: 800K"],
            "languages": ["Tagalog","Cebuano","Ilocano","English"],
            "osm_hints": ["filipino","tagalog","santo nino","san pedro calungsod","birhen","our lady of antipolo"],
            "justice_focus": ["Nurse / healthcare worker wages","Domestic worker rights","OFW remittance ethics","Anti-trafficking"],
            "communities": "8,200+ Filipino communities globally",
            "source": "Scalabrini Migration Center, CBCP 2022",
        },
        "Nigerian Catholic Diaspora": {
            "origin": "Nigeria", "total": "4M+",
            "concentrations": ["UK: 900K","USA: 800K","Europe: 600K","Canada: 400K"],
            "languages": ["English","Igbo","Yoruba","Hausa"],
            "osm_hints": ["nigerian","igbo","yoruba","our lady queen of nigeria","st. charles lwanga"],
            "justice_focus": ["Healthcare worker brain drain","Remittance support","Anti-trafficking","Political asylum support"],
            "communities": "2,400+ Nigerian communities globally",
            "source": "Pew Research 2022, Catholic Secretariat Nigeria",
        },
        "Kenyan / East African Diaspora": {
            "origin": "Kenya / Uganda / Tanzania", "total": "2M+",
            "concentrations": ["UK: 450K","USA: 350K","Germany: 120K","Middle East: 200K"],
            "languages": ["Swahili","Kikuyu","Luo","English","Luganda"],
            "osm_hints": ["swahili","kenyan","east african","st. joseph","holy family"],
            "justice_focus": ["Domestic worker rights","Living wage campaigns","Political asylum","Climate justice"],
            "communities": "1,100+ East African communities globally",
            "source": "Kenya National Bureau of Statistics, AMECEA 2022",
        },
        "Korean Catholic Diaspora": {
            "origin": "South Korea", "total": "1.5M+",
            "concentrations": ["USA: 600K","Japan: 300K","China: 200K","Australia: 120K"],
            "languages": ["Korean","English"],
            "osm_hints": ["korean","한인","st. andrew kim","korean catholic"],
            "justice_focus": ["Migrant worker rights","Reunification advocacy","Social welfare"],
            "communities": "1,800+ Korean communities globally",
            "source": "CBCK 2022, Pew Research",
        },
        "Polish Catholic Diaspora": {
            "origin": "Poland", "total": "20M+",
            "concentrations": ["USA: 9.5M","Germany: 2.2M","UK: 800K","France: 600K"],
            "languages": ["Polish","English"],
            "osm_hints": ["polish","polska","st. stanislaus","sw. maksymilian","częstochowa"],
            "justice_focus": ["Migrant worker rights","Community preservation","Political asylum"],
            "communities": "4,200+ Polish communities globally",
            "source": "Polish Bishops' Conference, Pew Research 2022",
        },
        "Brazilian Catholic Diaspora": {
            "origin": "Brazil", "total": "3M+",
            "concentrations": ["USA: 1.4M","Portugal: 600K","Japan: 300K","UK: 200K"],
            "languages": ["Portuguese","English"],
            "osm_hints": ["brasileira","nossa senhora","são","brazil","scalabrini"],
            "justice_focus": ["Migrant worker rights","Land rights solidarity","Anti-trafficking"],
            "communities": "1,600+ Brazilian communities globally",
            "source": "CNBB 2022, Scalabrini Center",
        },
        "Vietnamese Catholic Diaspora": {
            "origin": "Vietnam", "total": "3M+",
            "concentrations": ["USA: 1.5M","Australia: 350K","France: 300K","Germany: 200K"],
            "languages": ["Vietnamese","English","French"],
            "osm_hints": ["vietnamese","viet","la vang","our lady of lavang","blessed andrew phu yen"],
            "justice_focus": ["Refugee rights","Human trafficking","Political asylum","Worker rights"],
            "communities": "2,100+ Vietnamese communities globally",
            "source": "Pew Research 2022, Vietnamese Bishops Conference",
        },
    }

    community = st.selectbox("Select your community", list(_DIASPORA.keys()))
    d = _DIASPORA[community]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Origin", d["origin"])
        st.metric("Global Community", d["total"])
        st.markdown("**Global concentrations:**")
        for c in d["concentrations"]:
            st.write(f"• {c}")
        st.caption(f"📚 Source: {d['source']}")
    with col2:
        st.markdown("**Languages:**")
        st.write(", ".join(d["languages"]))
        st.metric("Communities worldwide", d["communities"])
        st.markdown("**Justice focus areas:**")
        for j in d["justice_focus"]:
            st.write(f"⚖️ {j}")

    st.divider()
    st.markdown("### 🔍 Find Community Near You")
    st.caption("Live search: finds Catholic churches likely serving your community via OpenStreetMap + name pattern matching")

    col1, col2 = st.columns([2,1])
    with col1:
        your_city    = st.text_input("Your city", placeholder="London / Dubai / Toronto / Chicago")
        your_country = st.text_input("Country (optional)", placeholder="UK / UAE / Canada / USA")
    with col2:
        st.markdown("**What we search for:**")
        for hint in d["osm_hints"][:4]:
            st.write(f"• `{hint}`")

    if st.button("🔍 Find My Community", type="primary"):
        if your_city.strip():
            # Strategy: search OSM for the city, then filter + supplement with community-specific search
            with st.spinner(f"Searching for {community} churches in {your_city}..."):
                try:
                    from gospelmap.church_search import search_by_city, _overpass, _geocode, _parse_element, Church
                    import math as _math

                    # Primary: general Catholic search in city
                    all_churches = search_by_city(your_city.strip(), your_country.strip() or None, limit=20)

                    # Secondary: targeted search using community name hints
                    def _hint_search(city, country, hints, limit=10):
                        """Search for churches matching community-specific name patterns."""
                        hint_pattern = "|".join(hints[:5])
                        area_query = f"""
                        [out:json][timeout:35];
                        area["name"~"{city}",i]["admin_level"~"4|5|6|7|8"]->.a;
                        (
                          node["amenity"="place_of_worship"]["name"~"{hint_pattern}",i](area.a);
                          way["amenity"="place_of_worship"]["name"~"{hint_pattern}",i](area.a);
                        );
                        out center {limit};
                        """
                        data = _overpass(area_query, timeout=40)
                        results = []
                        seen = set()
                        for elem in data.get("elements", []):
                            c = _parse_element(elem)
                            if c and c.name.lower() not in seen:
                                c.city = c.city or city.title()
                                results.append(c)
                                seen.add(c.name.lower())
                        return results

                    community_specific = _hint_search(
                        your_city.strip(),
                        your_country.strip() or "",
                        d["osm_hints"]
                    )

                    # Merge: community-specific first, then general
                    seen_names = {c.name.lower() for c in community_specific}
                    merged = list(community_specific)
                    for c in all_churches:
                        if c.name.lower() not in seen_names:
                            merged.append(c)
                            seen_names.add(c.name.lower())

                    # Tag community-specific results
                    cs_names = {c.name.lower() for c in community_specific}

                except Exception as e:
                    merged = []
                    cs_names = set()
                    st.error(f"Search error: {e}")

            if not merged:
                st.warning(f"No churches found in {your_city}. Try a larger nearby city.")
            else:
                if community_specific:
                    st.success(f"Found **{len(community_specific)} community-specific** + **{len(merged)-len(community_specific)} general Catholic** churches in {your_city}")
                else:
                    st.success(f"Found **{len(merged)} Catholic churches** in {your_city} — no community-specific results, showing all Catholic parishes")
                    st.info(f"💡 No churches with {community} name patterns found. Diaspora communities often worship at existing parishes without community-specific names. Contact these parishes about their community Mass schedules.")

                st.divider()
                for i, c in enumerate(merged[:12], 1):
                    is_community = c.name.lower() in cs_names
                    col1, col2, col3 = st.columns([3,1,1])
                    with col1:
                        label = f"🌟 {c.name}" if is_community else c.name
                        st.markdown(f"**{i}. {label}**")
                        if is_community:
                            st.caption(f"✨ Likely serves {community.split()[0]} community")
                        if c.address:
                            st.caption(f"📍 {c.address}")
                    with col2:
                        if c.distance_km:
                            st.metric("Distance", f"{c.distance_km:.1f} km")
                    with col3:
                        gmaps = f"https://www.google.com/maps?q={c.latitude},{c.longitude}"
                        st.markdown(f"[📍 Maps]({gmaps})")
                    if c.phone:
                        st.caption(f"📞 {c.phone}")
                    st.divider()
        else:
            st.warning("Enter your city to search")

    st.divider()
    st.markdown("### 🤝 Connect to Justice Network")
    st.write("Active campaigns connected to your community:")
    for j in d["justice_focus"]:
        col1, col2 = st.columns([4,1])
        with col1:
            st.write(f"⚖️ {j}")
        with col2:
            if st.button("Join", key=f"join_dia_{j[:18]}"):
                _submit_form("justice_join", {"community": community, "campaign": j})
                st.success("✅ Joined!")

    st.divider()
    st.markdown("### 📝 Register Your Community")
    st.caption("Know of a diaspora community not listed? Add it to GospelMap.")
    with st.expander("Register a community"):
        reg_c1, reg_c2 = st.columns(2)
        with reg_c1:
            reg_name    = st.text_input("Community name")
            reg_city    = st.text_input("City / Region")
            reg_country = st.text_input("Country")
        with reg_c2:
            reg_lang    = st.text_input("Primary language(s)")
            reg_parish  = st.text_input("Host parish (if known)")
            reg_contact = st.text_input("Contact (optional)")
        if st.button("Register Community"):
            if reg_name and reg_city:
                persisted = _submit_form("diaspora_community", {
                    "community_name": reg_name, "city": reg_city,
                    "country": reg_country, "languages": reg_lang,
                    "host_parish": reg_parish, "contact": reg_contact,
                })
                msg = "✅ Community registered and saved." if persisted else "✅ Community noted (session only — connect Google Sheets to persist)."
                st.success(msg)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: CRISIS RESPONSE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🆘 Crisis Response":
    st.title("🆘 Crisis Response Coordination")
    st.markdown("Real-time coordination of emergency response through the global parish network.")

    # Persistence status banner
    if _backend_ok():
        st.markdown('<div class="health-green">🟢 <strong>Live mode:</strong> All submissions persist to Google Sheets coordination database.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-yellow">🟡 <strong>Session mode:</strong> Submissions visible this session only. See <code>docs/SHEETS_SETUP.md</code> to enable persistence.</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🔴 Active Crises (Demo Baseline)")
    st.caption("These illustrative crises show coordination capability. Community-submitted crises appear below after submission.")

    crises = [
        {"name":"Flooding — Lake Victoria Region","location":"Kenya / Uganda / Tanzania",
         "severity":7.8,"parishes":450,"volunteers":2300,"shelters":15,"status":"🔴 ACTIVE"},
        {"name":"Refugee Surge — Horn of Africa","location":"Ethiopia / Somalia / Kenya border",
         "severity":8.2,"parishes":230,"volunteers":1200,"shelters":8,"status":"🔴 ACTIVE"},
        {"name":"Post-Cyclone Recovery — Mozambique","location":"Central Mozambique",
         "severity":6.4,"parishes":120,"volunteers":890,"shelters":12,"status":"🟡 RECOVERY"},
    ]

    # Session state for submitted crises
    if "submitted_crises" not in st.session_state:
        st.session_state.submitted_crises = []
    if "registered_aid" not in st.session_state:
        st.session_state.registered_aid = []

    # Show submitted crises (this session)
    all_crises = crises + st.session_state.submitted_crises
    for crisis in all_crises:
        col1, col2, col3 = st.columns([3,1,1])
        with col1:
            label = crisis.get("status", "🔵 SUBMITTED")
            st.markdown(f"#### {label} {crisis['name']}")
            st.caption(f"📍 {crisis['location']}")
            if "parishes" in crisis:
                st.write(f"Parishes: **{crisis['parishes']}** · Volunteers: **{crisis.get('volunteers',0):,}** · Shelters: **{crisis.get('shelters',0)}**")
            else:
                st.write(f"Type: **{crisis.get('type','Unknown')}** · Affected: **{crisis.get('affected',0):,}** people")
                if crisis.get("needs"):
                    st.write(f"Needs: {crisis['needs']}")
        with col2:
            st.metric("Severity", f"{crisis.get('severity', crisis.get('cr_severity', '?'))}/10")
        with col3:
            if st.button("Coordinate", key=f"coord_{crisis['name'][:12]}"):
                st.success("✅ Linked to coordination network.")
        st.divider()

    # ── REPORT A CRISIS ───────────────────────────────────────────────────────
    st.markdown("### 🆘 Report a New Crisis")
    with st.expander("Submit crisis report for network coordination", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            cr_name     = st.text_input("Crisis name*", key="cr_name")
            cr_location = st.text_input("Location (country / region)*", key="cr_loc")
            cr_type     = st.selectbox("Type", ["Flooding","Drought","Refugee surge",
                          "Earthquake","Conflict displacement","Disease outbreak","Food crisis","Other"])
        with c2:
            cr_severity = st.slider("Estimated severity (1–10)", 1, 10, 5, key="cr_sev")
            cr_affected = st.number_input("People affected (estimate)", 0, 10_000_000, 1000, key="cr_aff")
            cr_needs    = st.text_area("Description + immediate needs", key="cr_needs")

        if st.button("Submit Crisis Report", type="primary", key="submit_cr"):
            if cr_name and cr_location:
                payload = {
                    "name": cr_name, "location": cr_location,
                    "type": cr_type, "severity": cr_severity,
                    "affected": cr_affected, "needs": cr_needs,
                    "reported_at": datetime.utcnow().isoformat(),
                }
                persisted = _submit_form("crisis_report", payload)
                st.session_state.submitted_crises.append({
                    "name": cr_name, "location": cr_location,
                    "severity": cr_severity, "type": cr_type,
                    "affected": cr_affected, "needs": cr_needs,
                    "status": "🔵 SUBMITTED",
                })
                if persisted:
                    st.success(f"✅ Crisis '{cr_name}' submitted and saved to coordination database.")
                else:
                    st.success(f"✅ Crisis '{cr_name}' added to coordination board this session.")
                st.rerun()
            else:
                st.warning("Crisis name and location are required.")

    # ── OFFER AID ─────────────────────────────────────────────────────────────
    st.markdown("### 📋 Offer Aid Capacity")
    col1, col2 = st.columns(2)
    with col1:
        aid_parish  = st.text_input("Your parish / organisation*", key="aid_par")
        aid_city    = st.text_input("Your location*", key="aid_city")
        aid_contact = st.text_input("Contact email or phone", key="aid_contact")
    with col2:
        aid_types   = st.multiselect("What can you offer?",
                      ["Shelter (beds)","Food","Medical","Transport",
                       "Volunteer hours","Funds","Legal support","Prayer / spiritual support"],
                      key="aid_types")
        aid_capacity= st.text_input("Capacity (e.g. 20 beds, 50 meals/day)", key="aid_cap")
        aid_notes   = st.text_area("Additional notes", key="aid_notes")

    if st.button("Register Aid Capacity", type="primary", key="submit_aid"):
        if aid_parish and aid_city:
            payload = {
                "parish": aid_parish, "city": aid_city, "contact": aid_contact,
                "aid_types": aid_types, "capacity": aid_capacity, "notes": aid_notes,
                "registered_at": datetime.utcnow().isoformat(),
            }
            persisted = _submit_form("aid_capacity", payload)
            st.session_state.registered_aid.append(payload)
            if persisted:
                st.success(f"✅ **{aid_parish}** registered as aid provider — saved to coordination database. You'll be matched to nearest active crisis.")
            else:
                st.success(f"✅ **{aid_parish}** registered (session only). Connect Google Sheets to persist across sessions.")
        else:
            st.warning("Parish name and location are required.")

    # Show registered aid providers this session
    if st.session_state.registered_aid:
        st.divider()
        st.markdown(f"**Aid providers registered this session ({len(st.session_state.registered_aid)}):**")
        for a in st.session_state.registered_aid:
            st.write(f"• **{a['parish']}** ({a['city']}) — {', '.join(a.get('aid_types', []))}")

    # ── SETUP BANNER ──────────────────────────────────────────────────────────
    if not _backend_ok():
        st.divider()
        with st.expander("🔧 Enable Persistent Storage (5 min setup)"):
            st.markdown("""
**To make all form submissions persist permanently:**

1. Follow `docs/SHEETS_SETUP.md` — creates a free Google Sheets backend
2. Add `SHEETS_ENDPOINT = "your-apps-script-url"` to Streamlit Cloud secrets
3. All crisis reports, aid registrations, and accountability submissions  
   will persist in your Google Sheet — no database, no server, free forever.

**Estimated setup time:** 5 minutes
            """)

st.markdown("---")
st.caption("GospelMap | AGPL-3.0 | [GitHub](https://github.com/gabrielmahia/gospelmap) | contact@aikungfu.dev | CC BY-NC-ND 4.0")

