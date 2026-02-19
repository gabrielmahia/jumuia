"""
Sheets persistence — Catholic Parish Steward
============================================
Thin wrapper around gospelmap.sheets_backend.
Import _save() in any page that collects data.

Every submission routes to a dedicated tab in Google Sheets,
named after form_type (e.g. "parish_submission", "baptism", "scc_meeting").

Requires SHEETS_ENDPOINT in Streamlit secrets or SHEETS_ENDPOINT env var.
If not configured, submissions silently succeed in-session only.
"""

import streamlit as st


def _save(form_type: str, data: dict) -> bool:
    """
    Persist a form submission to Google Sheets.
    Returns True if saved to Sheets, False if session-only.
    Always safe to call — never raises.
    """
    try:
        from gospelmap.sheets_backend import submit
        return submit(form_type, data)
    except Exception:
        pass
    return False


def is_live() -> bool:
    """True if SHEETS_ENDPOINT is configured."""
    try:
        from gospelmap.sheets_backend import is_configured
        return is_configured()
    except Exception:
        return False


def persistence_badge():
    """
    Show a small status badge — only call this on admin/coordinator pages,
    never on public-facing flows.
    """
    if is_live():
        st.caption("🟢 Submissions saving to Google Sheets")
    else:
        st.caption(
            "🟡 Session only — add SHEETS_ENDPOINT to Streamlit secrets to persist data. "
            "See docs/SHEETS_SETUP.md"
        )
