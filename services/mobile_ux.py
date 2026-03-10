"""
Mobile & Rural UX Layer — Catholic Network Tools
Applies lightweight CSS + layout adjustments optimised for:
  - Low-bandwidth connections (2G/EDGE in Samburu, Turkana, rural Kenya)
  - Small screens (640px wide Android, Nokia feature browser)
  - High ambient light (outdoor visibility)
  - Low literacy support (icon-heavy, minimal jargon)
  - Dark mode (battery saving on AMOLED)

Inject at the top of each page via: from services.mobile_ux import inject_mobile_css; inject_mobile_css()
Or call from app.py once to apply globally.
"""

import streamlit as st


MOBILE_CSS = """
<style>
/* ── Reset & base ─────────────────────────────── */
* { box-sizing: border-box; }

/* Larger base font for readability in bright outdoor light */
html, body, [class*="css"] {
    font-size: 17px;
    line-height: 1.6;
}

/* ── Touch targets — minimum 48×48px (WCAG 2.5.5) ─ */
.stButton > button {
    min-height: 52px !important;
    font-size: 1rem !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    width: 100% !important;          /* full-width on mobile */
    margin-bottom: 0.5rem !important;
}

/* Primary buttons stand out more */
.stButton > button[kind="primary"] {
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
}

/* ── Forms — bigger inputs ────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select {
    min-height: 48px !important;
    font-size: 1rem !important;
    padding: 0.5rem 0.75rem !important;
}

/* ── Sidebar — compact on mobile ─────────────── */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        width: 220px !important;
        min-width: 220px !important;
    }
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 0.25rem !important;
    }
    section[data-testid="stSidebar"] label {
        font-size: 0.95rem !important;
    }
}

/* ── Tabs — larger, easier to tap ────────────── */
.stTabs [data-baseweb="tab"] {
    min-height: 48px !important;
    font-size: 0.95rem !important;
    padding: 0.4rem 0.8rem !important;
}

/* ── Cards & expanders ─────────────────────────── */
.streamlit-expanderHeader {
    min-height: 48px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}

/* ── Metrics — bigger numbers ─────────────────── */
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 800 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    opacity: 0.75;
}

/* ── Low-bandwidth: hide decorative images ────── */
@media (max-width: 480px) {
    img[alt="decorative"] { display: none !important; }
}

/* ── High contrast for outdoor bright light ────── */
@media (prefers-contrast: high) {
    .stButton > button {
        border: 2px solid currentColor !important;
    }
}

/* ── Scrollable tables on mobile ─────────────── */
[data-testid="stDataFrame"] {
    overflow-x: auto !important;
}

/* ── Stack all columns vertically on mobile ─── */
@media (max-width: 768px) {
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }
    [data-testid="stPlotlyChart"] > div { width: 100% !important; }
    iframe { width: 100% !important; max-width: 100% !important; }
}

/* ── Reduce motion for low-power devices ────── */
@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
}
</style>
"""


def inject_mobile_css():
    """Call once per page (or from app.py) to apply mobile-first styles."""
    st.markdown(MOBILE_CSS, unsafe_allow_html=True)


def data_saver_banner():
    """Show a lightweight 'Data Saver Mode' toggle. Stores in session state."""
    if "data_saver" not in st.session_state:
        st.session_state.data_saver = False

    with st.sidebar:
        st.session_state.data_saver = st.toggle(
            "📡 Data Saver Mode",
            value=st.session_state.data_saver,
            help="Reduces data usage. Disables maps and images.",
        )


def is_data_saver() -> bool:
    return st.session_state.get("data_saver", False)
