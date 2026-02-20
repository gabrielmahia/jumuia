"""Formation & Spiritual Education — Programmes, enrolment, curriculum, progress tracking."""

import streamlit as st
try:
    from services.save_indicator import mark_saved, show_save_status
except Exception:
    def mark_saved(x): pass
    def show_save_status(x, y=None): pass
from datetime import date

st.set_page_config(page_title="Formation", page_icon="🎓", layout="wide")

st.title("🎓 Formation & Spiritual Education")
st.caption("RCIA · Adult faith · Youth · Bible study · Retreats · Vocations")

if "formation_programmes" not in st.session_state:
    try:
        from services.sheets import fetch as _fetch_sheets
        _saved = _fetch_sheets("formation_programme")
        st.session_state.formation_programmes = _saved if _saved else []
    except Exception:
        st.session_state.formation_programmes = []

if "formation_participants" not in st.session_state:
    try:
        from services.sheets import fetch as _fetch_sheets
        _saved = _fetch_sheets("formation_participant")
        st.session_state.formation_participants = _saved if _saved else []
    except Exception:
        st.session_state.formation_participants = []
