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
    saved_ok: True = just saved to Sheets, False = save failed, None = show last saved time
    """
    key = f"_last_saved_{form_type}"
    last_saved = st.session_state.get(key)

    if saved_ok is True:
        st.success("✓ Saved to parish register", icon=None)
        mark_saved(form_type)
    elif saved_ok is False:
        st.warning(
            "⚠ Saved for this session only — "
            "ask your coordinator to check the register connection.",
            icon=None
        )
    elif last_saved:
        time_str = last_saved.strftime("%-I:%M %p")
        st.caption(f"Last saved: today {time_str}")


def trust_banner(module_name: str = ""):
    """
    Connection-aware banner replacing "Preview mode".
    Shows data safety status honestly — never calls experience a demo.
    """
    import streamlit as st
    try:
        from services.sheets import is_live as _is_live
        live = _is_live()
    except Exception:
        live = False

    if live:
        label = f"Your {module_name} records " if module_name else "Your records "
        st.success(
            f"🟢 {label}are saved to your parish register · "
            "Private to your parish · Data stays in your Google Sheet",
            icon=None
        )
    else:
        st.info(
            "📋 Records are saved for this session. "
            "To keep them permanently, connect Google Sheets — "
            "see **More Tools → Admin & Data** for setup.",
            icon=None
        )
