"""
Catholic Parish Steward
A complete spiritual OS for parishes worldwide.
"""

import streamlit as st

st.set_page_config(
    page_title="Catholic Parish Steward",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme ─────────────────────────────────────────────────────────────────────
try:
    from services.theme import inject as _inject_theme
    _inject_theme()
except Exception:
    pass

# ── Mobile UX ─────────────────────────────────────────────────────────────────
try:
    from services.mobile_ux import inject_mobile_css, data_saver_banner
    inject_mobile_css()
    data_saver_banner()
except Exception:
    pass

# ── Sidebar branding ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="padding:1.25rem 0 0.75rem; border-bottom:1px solid rgba(201,168,76,0.25); margin-bottom:1rem;">
  <div style="font-family:'DM Serif Display',Georgia,serif; font-size:1.2rem; color:white; font-weight:400; line-height:1.2;">
    Catholic Parish<br>Steward
  </div>
  <div style="font-size:0.72rem; color:rgba(201,168,76,0.75); text-transform:uppercase; letter-spacing:0.1em; margin-top:0.3rem;">
    Serving parishes worldwide
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Primary tools (3 things a parishioner needs) ───────────────────────
    st.markdown('<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:rgba(201,168,76,0.75);padding:0 0 0.4rem;">For Parishioners</div>', unsafe_allow_html=True)
    st.page_link("pages/01_Find_Church.py" if False else "pages/07_Parish_Directory.py", label="🗺️ Find a Church")
    st.page_link("pages/09_Daily_Prayers.py", label="📖 Daily Prayers & Readings")
    st.page_link("pages/06_AI_Assistant.py", label="🤖 Ask the Assistant")

    st.divider()

    # ── Coordinator tools ──────────────────────────────────────────────────
    st.markdown('<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:rgba(201,168,76,0.75);padding:0 0 0.4rem;">Parish Coordinators</div>', unsafe_allow_html=True)
    st.page_link("pages/10_Sacraments.py", label="✝️ Sacraments Register")
    st.page_link("pages/11_SCCs.py", label="🏘️ Small Communities")
    st.page_link("pages/12_Catechist_Certification.py", label="🎓 Catechists")
    st.page_link("pages/13_Pastoral_Care.py", label="🤲 Pastoral Care")
    st.page_link("pages/14_Formation.py", label="📚 Formation & RCIA")
    st.page_link("pages/08_Giving.py", label="💰 Parish Giving")

    st.divider()

    # ── More tools (collapsed) ─────────────────────────────────────────────
    with st.expander("More tools"):
        st.page_link("pages/_00_Liturgy.py", label="📋 Liturgy & Calendar")
        st.page_link("pages/_02_Ecosystem_Health.py", label="📊 Ecosystem Health")
        st.page_link("pages/_03_Justice_Network.py", label="⚖️ Justice Network")
        st.page_link("pages/_04_Accountability.py", label="📋 Accountability")
        st.page_link("pages/_05_Diaspora.py", label="🌏 Diaspora Connect")
        st.page_link("pages/_15_Admin_Data.py", label="📁 Admin & Data")

    st.divider()

    # ── USSD dial code ─────────────────────────────────────────────────────
    st.markdown("""
<div style="padding:0.75rem;background:rgba(201,168,76,0.1);border-radius:8px;border:1px solid rgba(201,168,76,0.25);text-align:center;">
  <div style="font-size:0.65rem;color:rgba(201,168,76,0.75);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.25rem;">Any phone in Kenya</div>
  <div style="font-family:monospace;font-size:1.1rem;color:white;font-weight:600;">*384*248724#</div>
  <div style="font-size:0.65rem;color:rgba(255,255,255,0.4);margin-top:0.2rem;">No internet needed</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HOMEPAGE — Three entry points
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap');

.cps-home-hero {
    background: linear-gradient(135deg, #0B1F3A 0%, #1a3a6b 100%);
    border-radius: 16px;
    padding: 3rem 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.cps-home-hero::before {
    content:'✝';
    position:absolute; right:2.5rem; top:50%; transform:translateY(-50%);
    font-size:8rem; color:rgba(201,168,76,0.10); font-family:serif;
    line-height:1;
}
.cps-home-title {
    font-family:'DM Serif Display',Georgia,serif;
    font-size:2.8rem; font-weight:400;
    color:white; margin:0 0 0.5rem; line-height:1.1;
}
.cps-home-sub {
    font-family:'DM Sans',system-ui,sans-serif;
    font-size:1.1rem; color:rgba(240,217,138,0.85);
    margin:0 0 1.5rem;
}
.cps-home-verse {
    font-family:'DM Serif Display',Georgia,serif;
    font-size:0.95rem; font-style:italic;
    color:rgba(255,255,255,0.5); margin:0;
}

/* Three action cards */
.cps-action-card {
    border: 1px solid rgba(11,31,58,0.10);
    border-radius: 14px;
    padding: 2rem 1.75rem 1.75rem;
    background: #F8F4EC;
    height: 100%;
    transition: box-shadow 0.2s, transform 0.2s;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.cps-action-card::after {
    content:'';
    position:absolute; bottom:0; left:0; right:0; height:4px;
    border-radius:0 0 14px 14px;
}
.cps-action-card.church::after { background: #C9A84C; }
.cps-action-card.readings::after { background: #1A5C3A; }
.cps-action-card.ai::after { background: #1a3a6b; }

.cps-card-icon { font-size:2.5rem; margin-bottom:1rem; display:block; }
.cps-card-title {
    font-family:'DM Serif Display',Georgia,serif;
    font-size:1.4rem; font-weight:400;
    color:#0B1F3A; margin:0 0 0.5rem;
}
.cps-card-desc {
    font-family:'DM Sans',system-ui,sans-serif;
    font-size:0.92rem; color:#4A5568;
    line-height:1.6; margin:0 0 1.25rem;
}
.cps-card-examples {
    font-family:'DM Sans',system-ui,sans-serif;
    font-size:0.78rem; color:#6B7280;
}
.cps-card-examples span {
    display:inline-block;
    background:rgba(11,31,58,0.06);
    border-radius:4px; padding:0.15rem 0.45rem;
    margin:0.15rem 0.15rem 0 0;
}

/* More features strip */
.cps-more-strip {
    background: rgba(11,31,58,0.04);
    border: 1px solid rgba(11,31,58,0.08);
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-top: 1.5rem;
}
.cps-more-title {
    font-family:'DM Sans',system-ui,sans-serif;
    font-size:0.72rem; font-weight:700;
    text-transform:uppercase; letter-spacing:0.1em;
    color:#C9A84C; margin:0 0 0.75rem;
}
.cps-more-grid {
    display:grid; grid-template-columns: repeat(auto-fill, minmax(180px,1fr));
    gap:0.5rem;
}
.cps-more-item {
    font-family:'DM Sans',system-ui,sans-serif;
    font-size:0.88rem; color:#4A5568; padding:0.35rem 0;
}

/* Stats row */
.cps-stats {
    display:flex; gap:2rem; flex-wrap:wrap;
    margin-top:1.5rem; padding-top:1.5rem;
    border-top:1px solid rgba(11,31,58,0.08);
}
.cps-stat-num {
    font-family:'DM Serif Display',Georgia,serif;
    font-size:1.6rem; color:#0B1F3A; display:block; line-height:1;
}
.cps-stat-label {
    font-size:0.72rem; font-weight:700; text-transform:uppercase;
    letter-spacing:0.07em; color:#9CA3AF; display:block; margin-top:0.2rem;
}

@media (prefers-color-scheme: dark) {
    .cps-action-card { background: rgba(255,255,255,0.04); border-color:rgba(255,255,255,0.08); }
    .cps-card-title  { color: #F0D98A; }
    .cps-card-desc   { color: #D1D5DB; }
    .cps-stat-num    { color: #F0D98A; }
    .cps-more-strip  { background: rgba(255,255,255,0.04); border-color:rgba(255,255,255,0.08); }
    .cps-more-item   { color: #D1D5DB; }
}
@media (max-width:640px) {
    .cps-home-title { font-size:2rem; }
    .cps-home-hero::before { display:none; }
    .cps-home-hero { padding:2rem 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cps-home-hero">
  <div class="cps-home-title">Catholic Parish Steward</div>
  <div class="cps-home-sub">
    Find your church · Follow the daily readings · Ask a question in any language
  </div>
  <div class="cps-home-verse">
    "Whatever you did for the least of these, you did for me." — Matthew 25:40
  </div>
</div>
""", unsafe_allow_html=True)

# ── Three action cards ────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown("""
<div class="cps-action-card church">
  <span class="cps-card-icon">🗺️</span>
  <div class="cps-card-title">Find a Church</div>
  <div class="cps-card-desc">
    Search 40,000+ Catholic churches worldwide by name, city, or region.
    Works in cities and remote rural areas alike.
  </div>
  <div class="cps-card-examples">
    <span>Nairobi</span><span>Samburu Kenya</span><span>Manassas Virginia</span>
    <span>Consolata Shrine</span><span>Sacred Heart</span>
  </div>
</div>
""", unsafe_allow_html=True)
    st.write("")
    if st.button("🗺️ Find a Church", type="primary", use_container_width=True, key="btn_church"):
        st.switch_page("pages/07_Parish_Directory.py")

with c2:
    st.markdown("""
<div class="cps-action-card readings">
  <span class="cps-card-icon">📖</span>
  <div class="cps-card-title">Daily Readings</div>
  <div class="cps-card-desc">
    Today's Mass readings, the Rosary in full, Divine Mercy Chaplet,
    Stations of the Cross, and the liturgical calendar.
  </div>
  <div class="cps-card-examples">
    <span>Rosary</span><span>Divine Mercy</span><span>Stations</span>
    <span>Kiswahili</span><span>Luganda</span>
  </div>
</div>
""", unsafe_allow_html=True)
    st.write("")
    if st.button("📖 Daily Readings & Prayers", type="primary", use_container_width=True, key="btn_prayers"):
        st.switch_page("pages/09_Daily_Prayers.py")

with c3:
    st.markdown("""
<div class="cps-action-card ai">
  <span class="cps-card-icon">🤖</span>
  <div class="cps-card-title">Ask the Assistant</div>
  <div class="cps-card-desc">
    Questions about Mass times, sacraments, the liturgical calendar,
    or translate a bulletin into Kiswahili, French, or Luganda.
  </div>
  <div class="cps-card-examples">
    <span>Mass times</span><span>Sacraments</span><span>Translation</span>
    <span>Homily prep</span><span>6 languages</span>
  </div>
</div>
""", unsafe_allow_html=True)
    st.write("")
    if st.button("🤖 AI Parish Assistant", type="primary", use_container_width=True, key="btn_ai"):
        st.switch_page("pages/06_AI_Assistant.py")

# ── More features ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="cps-more-strip">
  <div class="cps-more-title">More parish tools — use the sidebar to navigate</div>
  <div class="cps-more-grid">
    <div class="cps-more-item">📋 Liturgy &amp; Calendar</div>
    <div class="cps-more-item">📊 Ecosystem Health</div>
    <div class="cps-more-item">⚖️ Justice Network</div>
    <div class="cps-more-item">📋 Diocese Accountability</div>
    <div class="cps-more-item">🌏 Diaspora Connect</div>
    <div class="cps-more-item">💰 Parish Giving</div>
    <div class="cps-more-item">✝️ Sacraments Register</div>
    <div class="cps-more-item">🏘️ Small Christian Communities</div>
    <div class="cps-more-item">🎓 Catechist Certification</div>
    <div class="cps-more-item">🤲 Pastoral Care</div>
    <div class="cps-more-item">📚 Formation &amp; RCIA</div>
    <div class="cps-more-item">📁 Admin &amp; Data</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Stats strip ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="cps-stats">
  <div>
    <span class="cps-stat-num">40,000+</span>
    <span class="cps-stat-label">Churches searchable</span>
  </div>
  <div>
    <span class="cps-stat-num">150+</span>
    <span class="cps-stat-label">Countries</span>
  </div>
  <div>
    <span class="cps-stat-num">6</span>
    <span class="cps-stat-label">Languages</span>
  </div>
  <div>
    <span class="cps-stat-num">1.3B</span>
    <span class="cps-stat-label">Catholics worldwide</span>
  </div>
  <div>
    <span class="cps-stat-num">AGPL-3.0</span>
    <span class="cps-stat-label">Open source · community owned</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.caption(
    "Catholic Parish Steward · "
    "[GitHub](https://github.com/gabrielmahia/catholic-network-tools) · "
    "Built on the AMECEA tradition of Small Christian Communities · "
    "Data: OpenStreetMap contributors · "
    "AGPL-3.0"
)
