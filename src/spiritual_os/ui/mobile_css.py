"""
Mobile-First CSS for Catholic Spiritual OS

Optimizations for mobile devices (critical for Kenya/Africa):
- 80% of internet in Kenya is mobile
- Slow connections (3G common)
- Small screens (5-6 inch)
- Touch-first interaction

Design principles:
- Readable text (16px minimum)
- Large touch targets (44px minimum)
- Efficient loading (minimal CSS, no unnecessary images)
- Offline-friendly (service worker ready)
"""

MOBILE_CSS = """
<style>
/* ============================================================================
   MOBILE-FIRST RESPONSIVE DESIGN
   ============================================================================ */

/* Base: Mobile devices (320px - 768px) */
@media (max-width: 768px) {
    /* Typography - Larger for mobile */
    body {
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    
    h1 {
        font-size: 24px !important;
        line-height: 1.3 !important;
        margin-bottom: 16px !important;
    }
    
    h2 {
        font-size: 20px !important;
        line-height: 1.3 !important;
    }
    
    h3 {
        font-size: 18px !important;
    }
    
    /* Touch Targets - Minimum 44px for fingers */
    button, .stButton > button {
        min-height: 44px !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
    }
    
    /* Form inputs */
    input, select, textarea {
        min-height: 44px !important;
        font-size: 16px !important; /* Prevents iOS zoom */
        padding: 12px !important;
    }
    
    /* Links and interactive elements */
    a {
        min-height: 44px !important;
        display: inline-block !important;
        padding: 8px !important;
    }
    
    /* Expanders - Larger click area */
    .streamlit-expanderHeader {
        min-height: 44px !important;
        padding: 12px !important;
    }
    
    /* Cards and containers */
    .stMarkdown, .stInfo, .stWarning, .stSuccess, .stError {
        padding: 16px !important;
        margin: 12px 0 !important;
    }
    
    /* Columns stack on mobile */
    .row-widget.stHorizontal {
        flex-direction: column !important;
    }
    
    /* Full-width buttons on mobile */
    .stButton > button {
        width: 100% !important;
    }
    
    /* Reduce sidebar width on mobile */
    section[data-testid="stSidebar"] {
        width: 280px !important;
    }
    
    /* Prayer text - Larger for readability */
    .prayer-text {
        font-size: 18px !important;
        line-height: 1.8 !important;
        padding: 20px !important;
    }
    
    /* Mass readings - Optimized for reading */
    .reading-text {
        font-size: 17px !important;
        line-height: 1.7 !important;
        padding: 16px !important;
        margin: 16px 0 !important;
    }
    
    /* Tables - Horizontal scroll */
    table {
        display: block !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
    }
    
    /* Metrics - Stack vertically */
    .metric-container {
        flex-direction: column !important;
        align-items: flex-start !important;
    }
}

/* Tablet (769px - 1024px) */
@media (min-width: 769px) and (max-width: 1024px) {
    /* Moderate touch targets */
    button, .stButton > button {
        min-height: 40px !important;
        padding: 10px 16px !important;
    }
    
    input, select, textarea {
        min-height: 40px !important;
    }
}

/* ============================================================================
   PERFORMANCE OPTIMIZATIONS
   ============================================================================ */

/* Reduce animations on slow connections */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* ============================================================================
   LITURGICAL COLORS
   ============================================================================ */

/* Catholic liturgical color palette */
.liturgical-green {
    background-color: #2E7D32 !important;
    color: white !important;
}

.liturgical-white {
    background-color: #FFFFFF !important;
    color: #1B5E20 !important;
    border: 2px solid #2E7D32 !important;
}

.liturgical-red {
    background-color: #C62828 !important;
    color: white !important;
}

.liturgical-purple {
    background-color: #6A1B9A !important;
    color: white !important;
}

.liturgical-rose {
    background-color: #F48FB1 !important;
    color: #4A148C !important;
}

/* ============================================================================
   ACCESSIBILITY
   ============================================================================ */

/* High contrast for low vision */
@media (prefers-contrast: high) {
    * {
        border-color: #000 !important;
    }
    
    button, .stButton > button {
        border: 2px solid #000 !important;
    }
}

/* Focus indicators for keyboard navigation */
*:focus {
    outline: 3px solid #2E7D32 !important;
    outline-offset: 2px !important;
}

/* Skip to main content (accessibility) */
.skip-to-main {
    position: absolute;
    top: -40px;
    left: 0;
    background: #2E7D32;
    color: white;
    padding: 8px;
    text-decoration: none;
    z-index: 100;
}

.skip-to-main:focus {
    top: 0;
}

/* ============================================================================
   OFFLINE INDICATOR
   ============================================================================ */

.offline-banner {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: #FF6F00;
    color: white;
    text-align: center;
    padding: 12px;
    z-index: 1000;
    font-weight: bold;
}

.offline-banner.hidden {
    display: none;
}

/* ============================================================================
   PRINT STYLES (for bulletins, certificates)
   ============================================================================ */

@media print {
    /* Hide navigation and interactive elements */
    .stSidebar, button, .stButton, .stSelectbox, .stTextInput {
        display: none !important;
    }
    
    /* Show only content */
    .main {
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Prayer text - Optimized for printing */
    .prayer-text {
        font-size: 12pt !important;
        line-height: 1.5 !important;
        color: black !important;
        background: white !important;
    }
    
    /* Page breaks */
    .page-break {
        page-break-after: always !important;
    }
    
    /* No shadows or decorations */
    * {
        box-shadow: none !important;
        text-shadow: none !important;
    }
}

/* ============================================================================
   DARK MODE (respects system preference)
   ============================================================================ */

@media (prefers-color-scheme: dark) {
    /* Streamlit already handles this, but we can enhance */
    .prayer-text {
        background-color: #1E1E1E !important;
        color: #E0E0E0 !important;
    }
    
    .liturgical-white {
        background-color: #2E2E2E !important;
        color: #FFFFFF !important;
        border: 2px solid #757575 !important;
    }
}

/* ============================================================================
   LOADING STATES (for slow connections)
   ============================================================================ */

.loading-skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: loading 1.5s ease-in-out infinite;
    border-radius: 4px;
}

@keyframes loading {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}

/* ============================================================================
   CUSTOM COMPONENTS
   ============================================================================ */

/* Prayer card styling */
.prayer-card {
    background: linear-gradient(135deg, #F1F8F6 0%, #FFFFFF 100%);
    border-left: 4px solid #2E7D32;
    padding: 20px;
    border-radius: 8px;
    margin: 16px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Church finder result card */
.church-card {
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 16px;
    margin: 12px 0;
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    transition: box-shadow 0.2s;
}

.church-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.12);
}

/* SCC meeting card */
.scc-card {
    background: linear-gradient(135deg, #E8F5E9 0%, #F1F8F4 100%);
    border-radius: 8px;
    padding: 16px;
    margin: 12px 0;
    border-left: 4px solid #43A047;
}

</style>
"""


def inject_mobile_css():
    """
    Inject mobile-responsive CSS into Streamlit app
    
    Call this at the top of each page for mobile optimization.
    """
    import streamlit as st
    st.markdown(MOBILE_CSS, unsafe_allow_html=True)
