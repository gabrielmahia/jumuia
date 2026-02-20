"""
Theme & Design System — Catholic Network Tools

Aesthetic direction: "Sacred Utility"
- Rooted in the liturgical colour tradition (deep navy, Vatican gold, pure white)
- Expressed through a restrained, editorial lens — not ornate, not generic
- Typography: DM Serif Display (headlines) + DM Sans (body) — serious but approachable
- Works in both light and dark mode
- Optimised for mobile-first, rural-network constraints
- Touch targets: min 48px (WCAG 2.5.5)
"""

import streamlit as st

# ── Design tokens ─────────────────────────────────────────────────────────────
NAVY     = "#0B1F3A"   # Primary brand — deep night-sky navy
GOLD     = "#C9A84C"   # Vatican gold — accents, CTAs
GOLD_LT  = "#F0D98A"   # Light gold for dark mode text
CREAM    = "#F8F4EC"   # Warm white — backgrounds
CRIMSON  = "#8B1A1A"   # Alert / danger
GREEN    = "#1A5C3A"   # Success
GREY_700 = "#4A5568"
GREY_300 = "#CBD5E0"


GLOBAL_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════
   GOOGLE FONTS — DM Serif Display + DM Sans
   Loaded async, fallback to Georgia/system
═══════════════════════════════════════════════════════════ */
/* Fonts loaded async — app is fully usable before they arrive */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap&font-display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block&font-display=block');

/* Font-stack fallbacks apply instantly — no FOIT even on 2G */
body, .stApp {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
                 'Noto Sans', 'Liberation Sans', sans-serif !important;
}
h1, h2, h3, .cnt-hero-title, .cnt-stat-num, .cps-home-title {
    font-family: 'DM Serif Display', Georgia, 'Times New Roman',
                 'Noto Serif', serif !important;
}

/* ═══════════════════════════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════════════════════════ */
:root {
    --navy:     #0B1F3A;
    --gold:     #C9A84C;
    --gold-lt:  #F0D98A;
    --cream:    #F8F4EC;
    --crimson:  #8B1A1A;
    --green:    #1A5C3A;
    --radius:   10px;
    --shadow:   0 2px 12px rgba(11,31,58,0.10);
    --shadow-md:0 4px 24px rgba(11,31,58,0.15);
}

/* ═══════════════════════════════════════════════════════════
   BASE TYPOGRAPHY
═══════════════════════════════════════════════════════════ */
html, body, [class*="css"], .stMarkdown {
    font-family: 'DM Sans', system-ui, -apple-system, sans-serif !important;
    font-size: 16px;
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3 {
    font-family: 'DM Serif Display', Georgia, serif !important;
    font-weight: 400 !important;
    letter-spacing: -0.01em;
}

h1 { font-size: 2rem !important; }
h2 { font-size: 1.45rem !important; }
h3 { font-size: 1.15rem !important; }

/* ═══════════════════════════════════════════════════════════
   SIDEBAR — clean, branded, non-cluttered
═══════════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: var(--navy) !important;
    border-right: 1px solid rgba(201,168,76,0.20);
}

/* Sidebar text — explicit selectors, NOT wildcard */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] div.stMarkdown,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #E8E4DC !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
}

/* Sidebar inputs — always light bg + dark text for readability */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    background-color: #ffffff !important;
    color: #0B1F3A !important;
    border: 1px solid rgba(201,168,76,0.45) !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
}
section[data-testid="stSidebar"] input::placeholder,
section[data-testid="stSidebar"] textarea::placeholder {
    color: #9CA3AF !important;
}
section[data-testid="stSidebar"] input:focus,
section[data-testid="stSidebar"] textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.25) !important;
    outline: none !important;
}

/* Sidebar primary buttons — gold bg, navy text */
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: var(--gold) !important;
    color: var(--navy) !important;
    border: none !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: #B8953E !important;
}

/* Sidebar secondary/default buttons — visible border + light text */
section[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {
    background: rgba(255,255,255,0.08) !important;
    color: #E8E4DC !important;
    border: 1.5px solid rgba(201,168,76,0.55) !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover {
    background: rgba(201,168,76,0.15) !important;
    color: var(--gold-lt) !important;
    border-color: var(--gold) !important;
}

/* Sidebar expander — readable header */
section[data-testid="stSidebar"] .streamlit-expanderHeader {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(201,168,76,0.20) !important;
    border-radius: 8px !important;
    color: #E8E4DC !important;
    font-size: 0.85rem !important;
}
section[data-testid="stSidebar"] .streamlit-expanderContent {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(201,168,76,0.15) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 0.5rem !important;
}

/* Sidebar selectbox (language selector) */
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.09) !important;
    border: 1px solid rgba(201,168,76,0.35) !important;
    color: #E8E4DC !important;
}
section[data-testid="stSidebar"] .stSelectbox svg { fill: #E8E4DC !important; }

/* Sidebar toggle (Data Saver Mode) */
section[data-testid="stSidebar"] .stToggle label span {
    color: #E8E4DC !important;
}

/* Sidebar logo area */
section[data-testid="stSidebar"] .sidebar-logo {
    padding: 1.5rem 1rem 0.5rem;
    border-bottom: 1px solid rgba(201,168,76,0.25);
    margin-bottom: 0.5rem;
}

/* Radio nav items */
section[data-testid="stSidebar"] .stRadio > div {
    gap: 0.15rem !important;
}
section[data-testid="stSidebar"] .stRadio label {
    border-radius: 8px !important;
    padding: 0.55rem 0.85rem !important;
    cursor: pointer;
    transition: background 0.15s;
    font-size: 0.93rem !important;
    font-weight: 500;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(201,168,76,0.12) !important;
}
section[data-testid="stSidebar"] .stRadio [data-checked="true"] label,
section[data-testid="stSidebar"] .stRadio input:checked + div {
    background: rgba(201,168,76,0.20) !important;
    color: var(--gold-lt) !important;
}

section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 8px !important;
    color: #E8E4DC !important;
}
section[data-testid="stSidebar"] .stSelectbox label {
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    opacity: 0.6;
    margin-bottom: 0.2rem;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(201,168,76,0.20) !important;
    margin: 0.75rem 0 !important;
}
section[data-testid="stSidebar"] .stToggle label {
    font-size: 0.82rem !important;
    opacity: 0.8;
}

/* ═══════════════════════════════════════════════════════════
   MAIN CONTENT AREA
═══════════════════════════════════════════════════════════ */
.main .block-container {
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1100px !important;
}
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 0.85rem !important;
    }
}

/* ═══════════════════════════════════════════════════════════
   BUTTONS — prominent, tactile, touch-friendly
═══════════════════════════════════════════════════════════ */
.stButton > button {
    min-height: 48px !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
    transition: all 0.15s ease !important;
    cursor: pointer;
}

.stButton > button[kind="primary"] {
    background: var(--gold) !important;
    color: var(--navy) !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(201,168,76,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #B8953E !important;
    box-shadow: 0 4px 16px rgba(201,168,76,0.45) !important;
    transform: translateY(-1px) !important;
}

.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1.5px solid var(--gold) !important;
    color: var(--gold) !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(201,168,76,0.08) !important;
}

/* Full-width on mobile */
@media (max-width: 640px) {
    .stButton > button { width: 100% !important; }
}

/* ═══════════════════════════════════════════════════════════
   INPUTS — clean, spacious
═══════════════════════════════════════════════════════════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    min-height: 46px !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
    font-size: 0.97rem !important;
    border: 1.5px solid var(--grey-300, #CBD5E0) !important;
    transition: border-color 0.15s !important;
    padding: 0.5rem 0.85rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.15) !important;
}
.stTextInput > label, .stTextArea > label, .stSelectbox > label {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    opacity: 0.65;
    margin-bottom: 0.3rem !important;
}

/* Chat input */
.stChatInput > div {
    border-radius: 12px !important;
    border: 1.5px solid var(--gold) !important;
}

/* ═══════════════════════════════════════════════════════════
   TABS
═══════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    border-bottom: 2px solid rgba(201,168,76,0.20) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    min-height: 46px !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
    color: var(--grey-700, #4A5568) !important;
    border-bottom: 2.5px solid transparent !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.15s !important;
}
.stTabs [aria-selected="true"][data-baseweb="tab"] {
    color: var(--gold, #C9A84C) !important;
    border-bottom-color: var(--gold, #C9A84C) !important;
    background: transparent !important;
}

/* ═══════════════════════════════════════════════════════════
   EXPANDERS / CARDS
═══════════════════════════════════════════════════════════ */
.streamlit-expanderHeader {
    min-height: 52px !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}

/* ═══════════════════════════════════════════════════════════
   METRICS
═══════════════════════════════════════════════════════════ */
[data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', Georgia, serif !important;
    font-size: 2.2rem !important;
    font-weight: 400 !important;
    color: var(--navy) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    opacity: 0.55;
}

/* ═══════════════════════════════════════════════════════════
   ALERT / INFO / SUCCESS BOXES
═══════════════════════════════════════════════════════════ */
.stAlert {
    border-radius: 8px !important;
    border-left-width: 4px !important;
    font-size: 0.94rem !important;
}

/* ═══════════════════════════════════════════════════════════
   CUSTOM COMPONENT CLASSES  (use via st.markdown unsafe_allow_html)
═══════════════════════════════════════════════════════════ */

/* Page hero */
.cnt-hero {
    background: linear-gradient(135deg, var(--navy) 0%, #1a3a6b 100%);
    color: white;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.cnt-hero::before {
    content: '';
    position: absolute;
    right: -40px; top: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(201,168,76,0.10);
}
.cnt-hero-title {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 2rem;
    font-weight: 400;
    margin: 0 0 0.4rem;
    color: white;
}
.cnt-hero-sub {
    font-size: 1rem;
    opacity: 0.75;
    margin: 0;
    color: #E8E4DC;
}
.cnt-hero-badge {
    display: inline-block;
    background: rgba(201,168,76,0.25);
    border: 1px solid rgba(201,168,76,0.50);
    color: var(--gold-lt);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    margin-bottom: 0.75rem;
}

/* Stat card */
.cnt-stat-card {
    background: var(--cream);
    border: 1px solid rgba(11,31,58,0.08);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    text-align: center;
    box-shadow: var(--shadow);
}
.cnt-stat-num {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 2.5rem;
    color: var(--navy);
    line-height: 1;
    margin-bottom: 0.3rem;
}
.cnt-stat-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6B7280;
}

/* Section divider with label */
.cnt-section-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--gold);
    margin: 1.5rem 0 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.cnt-section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(201,168,76,0.25);
}

/* Quota warning — friendly, not alarming */
.cnt-quota-notice {
    background: #FFF8E7;
    border: 1px solid rgba(201,168,76,0.4);
    border-left: 4px solid var(--gold);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-size: 0.93rem;
    color: #5C4A1E;
}

/* ═══════════════════════════════════════════════════════════
   DARK MODE — system preference + Streamlit dark theme
═══════════════════════════════════════════════════════════ */
@media (prefers-color-scheme: dark) {
    [data-testid="stMetricValue"] { color: var(--gold-lt) !important; }
    .cnt-stat-card { background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.08); }
    .cnt-stat-num { color: var(--gold-lt); }
    .cnt-quota-notice { background: rgba(201,168,76,0.08); color: var(--gold-lt); }

    /* Inputs in dark mode — keep readable */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: rgba(255,255,255,0.08) !important;
        color: #F0EDE8 !important;
        border-color: rgba(201,168,76,0.35) !important;
    }
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(240,237,232,0.45) !important;
    }

    /* Tab text in dark mode */
    .stTabs [data-baseweb="tab"] {
        color: rgba(240,237,232,0.65) !important;
    }
    .stTabs [aria-selected="true"][data-baseweb="tab"] {
        color: var(--gold-lt) !important;
    }

    /* Expanders in dark mode */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.04) !important;
        color: #E8E4DC !important;
    }
}

/* ═══════════════════════════════════════════════════════════
   ACCESSIBILITY & LOW-POWER
═══════════════════════════════════════════════════════════ */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
@media (prefers-contrast: high) {
    .stButton > button { border: 2px solid currentColor !important; }
    section[data-testid="stSidebar"] * { border-color: rgba(255,255,255,0.6) !important; }
}

/* High-contrast / forced-colors mode (Windows, some Android accessibility) */
@media (forced-colors: active) {
    .stButton > button { border: 2px solid ButtonText !important; }
    section[data-testid="stSidebar"] input { border: 2px solid ButtonText !important; }
}

/* Ensure no text falls below WCAG AA threshold in sidebar (4.5:1 ratio) */
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    font-size: 0.75rem !important;
    color: rgba(255,255,255,0.65) !important;
}

/* Minimum touch target for all interactive sidebar elements */
section[data-testid="stSidebar"] .stButton > button,
section[data-testid="stSidebar"] select,
section[data-testid="stSidebar"] input[type="checkbox"],
section[data-testid="stSidebar"] input[type="radio"] {
    min-height: 44px !important;
    min-width: 44px !important;
}

[data-testid="stDataFrame"] { overflow-x: auto !important; }
</style>
"""


def inject():
    """Call once per page to apply the global theme."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str = "", badge: str = ""):
    """Render a page hero section."""
    badge_html = f'<div class="cnt-hero-badge">{badge}</div>' if badge else ""
    sub_html   = f'<p class="cnt-hero-sub">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f"""<div class="cnt-hero">
            {badge_html}
            <div class="cnt-hero-title">{title}</div>
            {sub_html}
        </div>""",
        unsafe_allow_html=True,
    )


def section_label(text: str):
    st.markdown(f'<div class="cnt-section-label">{text}</div>', unsafe_allow_html=True)


def quota_notice(message: str):
    st.markdown(
        f'<div class="cnt-quota-notice">⏳ {message}</div>',
        unsafe_allow_html=True,
    )
