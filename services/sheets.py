"""
Sheets persistence — Jumuia — Parish Community
==============================================
Direct POST to Google Apps Script endpoint. Zero dependency on gospelmap.

Deploy docs/AppsScript_Sheets.js to Google Apps Script (bound to your Sheet).
Then add SHEETS_ENDPOINT to Streamlit secrets:

  [secrets.toml]
  SHEETS_ENDPOINT = "https://script.google.com/macros/s/YOUR_ID/exec"

Every form_type creates its own tab in the Sheet.
All calls are safe — never raise, log failures silently.
"""
import json
import logging
import urllib.request
import urllib.error

try:
    import streamlit as st
    _st_available = True
except Exception:
    _st_available = False

logger = logging.getLogger(__name__)

_ENDPOINT: str | None = None


def _get_endpoint() -> str | None:
    global _ENDPOINT
    if _ENDPOINT:
        return _ENDPOINT
    # Streamlit Cloud: st.secrets
    if _st_available:
        try:
            ep = st.secrets.get("SHEETS_ENDPOINT")
            if ep:
                _ENDPOINT = ep
                return _ENDPOINT
        except Exception:
            pass
    # Local / Cloud Run: environment variable
    import os
    ep = os.environ.get("SHEETS_ENDPOINT")
    if ep:
        _ENDPOINT = ep
    return _ENDPOINT


def is_configured() -> bool:
    """True if SHEETS_ENDPOINT is set — i.e. submissions will actually persist."""
    return bool(_get_endpoint())


def _save(form_type: str, data: dict) -> bool:
    """
    POST a form submission to Google Sheets via Apps Script.

    Args:
        form_type: Becomes the tab name in the Sheet
                   (e.g. "parish_submission", "baptism", "scc_meeting")
        data:      Dict of field→value pairs

    Returns:
        True  — saved to Sheets
        False — session-only (endpoint not configured or network error)
    """
    endpoint = _get_endpoint()
    if not endpoint:
        logger.debug("SHEETS_ENDPOINT not configured — session-only save for %s", form_type)
        return False

    payload = json.dumps({"form_type": form_type, "data": data}).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            result = json.loads(body)
            if result.get("status") == "ok":
                logger.info("Sheets saved: form=%s", form_type)
                return True
            else:
                logger.warning("Sheets non-ok response for %s: %s", form_type, body[:200])
                return False
    except urllib.error.HTTPError as e:
        logger.warning("Sheets HTTP %s for %s", e.code, form_type)
    except Exception as e:
        logger.warning("Sheets save failed for %s: %s", form_type, e)
    return False


# Backward-compat alias used by gospelmap.sheets_backend callers
submit = _save


def is_live() -> bool:
    """Alias for is_configured() — used by persistence_badge."""
    return is_configured()


def fetch(sheet_name: str, max_rows: int = 200) -> list:
    """
    Read rows back from a Google Sheet tab via the Apps Script doGet endpoint.

    The Apps Script must implement doGet(e) — see docs/AppsScript_Sheets.js.
    Returns list of dicts. Returns [] if not configured or doGet not deployed.
    """
    endpoint = _get_endpoint()
    if not endpoint:
        return []

    url = f"{endpoint}?sheet={sheet_name}&max_rows={max_rows}"
    try:
        with urllib.request.urlopen(url, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list):
                return data
            return data.get("rows", [])
    except Exception as e:
        logger.warning("Sheets fetch failed for %s: %s", sheet_name, e)
        return []


def persistence_badge() -> None:
    """
    Render a small save-status badge.
    Only call on coordinator/admin pages — never on public-facing flows.
    """
    if not _st_available:
        return
    if is_configured():
        st.caption("🟢 Submissions saving to Google Sheets")
    else:
        st.caption(
            "🟡 Session only — add SHEETS_ENDPOINT to Streamlit secrets to persist data. "
            "See docs/SHEETS_SETUP.md"
        )
