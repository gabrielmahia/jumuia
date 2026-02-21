"""
Catholic Parish Steward — Google Sheets Backend
================================================
Zero-infra persistence via Google Apps Script web app.
No credentials stored — just a public POST endpoint.

Apps Script (already deployed):
  doPost() receives JSON, routes to tab by form_type,
  auto-creates headers on first write.

Setup (one-time):
  1. Deploy Apps Script → copy web app URL
  2. Add to Streamlit secrets: SHEETS_ENDPOINT = "https://..."
  3. Done — all form submissions land in Google Sheets permanently

Without SHEETS_ENDPOINT: submissions succeed in-session only (no data loss
for the user, but nothing persists across sessions).
"""

import json
import urllib.request
import urllib.error
import logging
import streamlit as st
from datetime import datetime, UTC
from typing import Optional

logger = logging.getLogger(__name__)


def _endpoint() -> Optional[str]:
    try:
        ep = st.secrets.get("SHEETS_ENDPOINT")
        if ep:
            return ep
    except Exception:
        pass
    import os
    return os.environ.get("SHEETS_ENDPOINT")


def is_configured() -> bool:
    return bool(_endpoint())


def submit(form_type: str, data: dict) -> bool:
    """
    POST form data to Google Sheets backend.
    Automatically adds form_type and timestamp fields.
    Returns True if persisted, False if no endpoint or on error.
    """
    endpoint = _endpoint()
    if not endpoint:
        return False

    # Enrich with parish identity if set
    try:
        from services.parish_identity import inject_into_record
        data = inject_into_record(data)
    except Exception:
        pass

    payload = {
        "form_type": form_type,
        "timestamp": datetime.now(UTC).isoformat(),
        **{k: (str(v) if not isinstance(v, (str, int, float, bool)) else v)
           for k, v in data.items()}
    }

    try:
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            resp = json.loads(r.read().decode("utf-8"))
            if resp.get("status") == "ok":
                logger.debug("Sheets: persisted %s", form_type)
                return True
            logger.warning("Sheets: non-ok response for %s: %s", form_type, resp)
            return False
    except urllib.error.HTTPError as e:
        logger.warning("Sheets HTTP %s for %s", e.code, form_type)
        return False
    except Exception as e:
        logger.warning("Sheets error for %s: %s", form_type, e)
        return False

def fetch(sheet_name: str, max_rows: int = 200) -> list[dict]:
    """
    Read rows from a Google Sheet tab via the doGet endpoint.
    Returns list of dicts (one per row). Returns [] if unavailable or not configured.

    Requires doGet() deployed in the Apps Script — see docs/SHEETS_SETUP.md.
    Never raises — silently returns empty list on any error.
    """
    endpoint = _endpoint()
    if not endpoint:
        return []

    try:
        import urllib.parse
        params = urllib.parse.urlencode({"sheet": sheet_name})
        url = f"{endpoint}?{params}"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=10) as r:
            resp = json.loads(r.read().decode("utf-8"))
            if resp.get("status") == "ok":
                rows = resp.get("rows", [])
                return rows[-max_rows:] if len(rows) > max_rows else rows
    except Exception as e:
        logger.debug("Sheets fetch error for %s: %s", sheet_name, e)
    return []

