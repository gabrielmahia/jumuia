"""
Catholic Network Tools — Main Application Entry Point

Pages:
  /              → Home / Role selector
  /AI_Assistant  → Translation, Homily Helper, Parish Insights, Chat Bot
  /Directory     → Parish Directory (local + GCatholic rails)
  /Giving        → M-Pesa giving (sandbox)
  /Bot_Setup     → WhatsApp bot activation status
"""

import streamlit as st

st.set_page_config(
    page_title="Catholic Network Tools",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar branding
st.sidebar.markdown("## ✝️ Catholic Network Tools")
st.sidebar.caption("Decision support for parish communities worldwide.")
st.sidebar.divider()

# ─────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────

st.title("✝️ Catholic Network Tools")
st.markdown(
    """
    A community-built platform for parishes, coordinators, priests, and diocesan leaders.
    Serving 1.3 billion Catholics with decision support, directory, and giving infrastructure.
    """
)

st.info(
    "**DEMO ENVIRONMENT** — Parish data is seeded sample data. "
    "M-Pesa giving uses Safaricom sandbox (no real transactions). "
    "AI features require a valid ANTHROPIC_API_KEY in your `.env`.",
    icon="ℹ️"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 🤖 AI Assistant")
    st.markdown("Translation · Homily prep · Insights · Chat")
    if st.button("Open AI Assistant", use_container_width=True):
        st.switch_page("pages/01_AI_Assistant.py")

with col2:
    st.markdown("### 🗺️ Parish Directory")
    st.markdown("Search parishes · Kenya + Global · GCatholic rails")
    if st.button("Open Directory", use_container_width=True):
        st.switch_page("pages/02_Parish_Directory.py")

with col3:
    st.markdown("### 🤝 Parish Giving")
    st.markdown("M-Pesa STK push · Sandbox active · Live rails ready")
    if st.button("Open Giving", use_container_width=True):
        st.switch_page("pages/03_Giving.py")

with col4:
    st.markdown("### 💬 WhatsApp Bot")
    st.markdown("Message-based access · Framework ready · Activation guide")
    if st.button("Open Bot Setup", use_container_width=True):
        st.switch_page("pages/04_Bot_Setup.py")

st.divider()
st.caption(
    "© Catholic Network Tools — CC BY-NC-ND 4.0 | "
    "contact@aikungfu.dev | "
    "[Security Policy](SECURITY.md)"
)
