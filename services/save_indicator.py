"""
Save Indicator Service
Shows coordinators when data was last saved to Google Sheets.
Prevents the silent data loss fear.
"""
import streamlit as st
from datetime import datetime


def mark_saved(form_type: str):
    """Call this after a successful save. Stores timestamp in session."""
    key = f"_last_saved_{form_type}"
    st.session_state[key] = datetime.now()


def show_save_status(form_type: str, saved_ok: bool = None):
    """
    Display a small, calm save status indicator.
    saved_ok: True = just saved, False = save failed, None = show last saved time
    """
    key = f"_last_saved_{form_type}"
    last_saved = st.session_state.get(key)

    if saved_ok is True:
        st.success("✓ Saved", icon=None)
        mark_saved(form_type)
    elif saved_ok is False:
        st.warning("⚠ Not saved to cloud — stored locally", icon=None)
    elif last_saved:
        time_str = last_saved.strftime("%-I:%M %p")
        st.caption(f"Last saved: today {time_str}")
