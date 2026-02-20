"""
Catholic Parish Steward
A complete spiritual OS for parishes worldwide.
"""

import streamlit as st
from services.i18n import lang_selector
from services.parish_identity import sidebar_widget as _parish_widget
from services.roles import sidebar_role_badge as _role_badge
from services.privacy import privacy_sidebar_widget as _privacy_widget

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

# ── Settings-driven accessibility ─────────────────────────────────────────────
try:
    from services.settings import get as _get_setting, init as _init_settings
    _init_settings()
    _css_overrides = []
    if _get_setting("large_text"):
        _css_overrides.append("html { font-size: 120% !important; }")
    if _get_setting("text_only"):
        _css_overrides.append(
            "[data-testid='stPlotlyChart'], [data-testid='stVegaLiteChart'], "
            ".element-container img { display: none !important; }"
        )
    if _css_overrides:
        st.markdown(f"<style>{'  '.join(_css_overrides)}</style>", unsafe_allow_html=True)
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
ecosystem   = st.Page("pages/_02_Ecosystem_Health.py",         title="Parish Health",  icon="📊")
justice     = st.Page("pages/_03_Justice_Network.py",          title="Justice & Care",   icon="⚖️")
accountability = st.Page("pages/_04_Accountability.py",        title="Transparency",    icon="📋")
diaspora    = st.Page("pages/_05_Diaspora.py",                 title="Global Diaspora",  icon="🌏")
ussd_guide  = st.Page("pages/_16_USSD_Setup.py",         title="Set Up USSD",       icon="📱")
settings_pg = st.Page("pages/15_Settings.py",               title="Settings",          icon="⚙️")
admin       = st.Page("pages/_15_Admin_Data.py",               title="Admin & Data",      icon="📁")

pg = st.navigation(
    {
        "": [home],
        "For Parishioners": [find_church, prayers, assistant],
        "Parish Coordinators": [sacraments, sccs, catechist, pastoral, formation, giving],
        "More Tools": [liturgy, ecosystem, justice, accountability, diaspora, admin, ussd_guide, settings_pg],
    },
    position="sidebar",
    expanded=False,
)

# ── Parish identity, role badge + language selector ──────────────────────────
with st.sidebar:
    _parish_widget()
    _role_badge()
    lang_selector()

# ── Sidebar footer ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="margin-top:1rem;padding:0.75rem;background:rgba(201,168,76,0.08);
     border-radius:8px;border:1px solid rgba(201,168,76,0.2);text-align:center;">
  <div style="font-size:0.65rem;color:rgba(201,168,76,0.75);text-transform:uppercase;
       letter-spacing:0.08em;margin-bottom:0.25rem;">Basic phone access</div>
  <div style="font-family:monospace;font-size:1.1rem;color:white;font-weight:600;">*384*248724#</div>
  <div style="font-size:0.68rem;color:rgba(255,255,255,0.62);margin-top:0.25rem;line-height:1.4;">
    Available once your diocese<br>registers with Africa's Talking.<br>See <em>More Tools → Set Up USSD</em>
  </div>
</div>
<div style="font-size:0.68rem;color:rgba(255,255,255,0.42);text-align:center;margin-top:0.75rem;line-height:1.5;padding:0 0.5rem;">
  Parish data stays in your Google Sheet.<br>Nothing shared with third parties.
</div>
""", unsafe_allow_html=True)

# sidebar collapse button icon left as Streamlit default

pg.run()
