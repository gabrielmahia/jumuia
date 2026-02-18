"""
GospelMap — Google Sheets Backend
Zero-infra persistence via Google Apps Script web app.
No credentials stored in the app — just a public POST endpoint.

Setup (one-time, ~5 minutes):
  1. Go to sheets.google.com → create new sheet called "GospelMap Submissions"
  2. Extensions → Apps Script → paste the script from docs/SHEETS_SETUP.md
  3. Deploy → New deployment → Web app → Execute as Me → Anyone can access
  4. Copy the web app URL → add to Streamlit Cloud secrets as SHEETS_ENDPOINT
  5. Done — all form submissions persist in your Google Sheet

Without setup: submissions shown in session only (not persisted).
"""

import requests
import streamlit as st
from datetime import datetime
from typing import Optional


def _endpoint() -> Optional[str]:
    """Get configured endpoint from Streamlit secrets or env."""
    try:
        return st.secrets.get("SHEETS_ENDPOINT")
    except Exception:
        return None


def submit(form_type: str, data: dict) -> bool:
    """
    POST a form submission to Google Sheets backend.
    Returns True if persisted, False if no endpoint configured.
    """
    endpoint = _endpoint()
    if not endpoint:
        return False
    try:
        payload = {
            "form_type": form_type,
            "timestamp": datetime.utcnow().isoformat(),
            **data
        }
        r = requests.post(endpoint, json=payload, timeout=10)
        return r.status_code == 200
    except Exception:
        return False


def is_configured() -> bool:
    return bool(_endpoint())

