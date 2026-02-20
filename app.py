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

# ── Navigation — full control via st.navigation() ────────────────────────────
home        = st.Page("pages/home.py",                         title="Home",              icon="✝️",  default=True)
find_church = st.Page("pages/07_Parish_Directory.py",          title="Find a Church",     icon="🗺️")
prayers     = st.Page("pages/09_Daily_Prayers.py",             title="Daily Prayers",     icon="📖")
assistant   = st.Page("pages/06_AI_Assistant.py",              title="AI Assistant",      icon="🤖")
sacraments  = st.Page("pages/10_Sacraments.py",                title="Sacraments",        icon="✝️")
sccs        = st.Page("pages/11_SCCs.py",                      title="Small Communities", icon="🏘️")
catechist   = st.Page("pages/12_Catechist_Certification.py",   title="Catechists",        icon="🎓")
pastoral    = st.Page("pages/13_Pastoral_Care.py",             title="Pastoral Care",     icon="🤲")
formation   = st.Page("pages/14_Formation.py",                 title="Formation & RCIA",  icon="📚")
giving      = st.Page("pages/08_Giving.py",                    title="Parish Giving",     icon="💰")
liturgy     = st.Page("pages/_00_Liturgy.py",                  title="Liturgy & Calendar",icon="📋")
ecosystem   = st.Page("pages/_02_Ecosystem_Health.py",         title="Ecosystem Health",  icon="📊")
justice     = st.Page("pages/_03_Justice_Network.py",          title="Justice Network",   icon="⚖️")
accountability = st.Page("pages/_04_Accountability.py",        title="Accountability",    icon="📋")
diaspora    = st.Page("pages/_05_Diaspora.py",                 title="Diaspora Connect",  icon="🌏")
ussd_guide  = st.Page("pages/_16_USSD_Setup.py",         title="Set Up USSD",       icon="📱")
admin       = st.Page("pages/_15_Admin_Data.py",               title="Admin & Data",      icon="📁")

pg = st.navigation(
    {
        "": [home],
        "For Parishioners": [find_church, prayers, assistant],
        "Parish Coordinators": [sacraments, sccs, catechist, pastoral, formation, giving],
        "More Tools": [liturgy, ecosystem, justice, accountability, diaspora, admin, ussd_guide],
    },
    position="sidebar",
    expanded=False,
)

# ── Sidebar footer ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="margin-top:1rem;padding:0.75rem;background:rgba(201,168,76,0.08);
     border-radius:8px;border:1px solid rgba(201,168,76,0.2);text-align:center;">
  <div style="font-size:0.65rem;color:rgba(201,168,76,0.75);text-transform:uppercase;
       letter-spacing:0.08em;margin-bottom:0.25rem;">Basic phone access</div>
  <div style="font-family:monospace;font-size:1.1rem;color:white;font-weight:600;">*384*248724#</div>
  <div style="font-size:0.65rem;color:rgba(255,255,255,0.5);margin-top:0.25rem;line-height:1.4;">
    Available once your diocese<br>registers with Africa's Talking.<br>See <em>More Tools → Set Up USSD</em>
  </div>
</div>
""", unsafe_allow_html=True)

# sidebar collapse button icon left as Streamlit default

pg.run()
