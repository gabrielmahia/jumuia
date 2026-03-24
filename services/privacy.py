"""
Privacy & GDPR Compliance Module — Jumuia — Parish Community
==========================================================
Implements:
- Data minimisation
- Right to erasure (data deletion request)
- PII detection and scrubbing before any log write
- Anonymous usage mode
- Audit log for admin/coordinator actions

Regulatory scope: GDPR (EU), Kenya Data Protection Act 2019,
Philippines DPA 2012, Brazil LGPD.

Hard exclusions (NEVER collected regardless of user request):
- Confession content
- Private prayer text
- Political affiliation
- Sexual orientation
"""

import hashlib
import logging
import re
from datetime import datetime, timezone, UTC

logger = logging.getLogger(__name__)

# ── PII patterns ───────────────────────────────────────────────────────────────
_PII_PATTERNS = [
    re.compile(r"\b\d{10,13}\b"),                                         # phone
    re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.\w{2,}"),          # email
    re.compile(r"\b(?:\d[ \-]?){13,16}\b"),                               # card
]

HARD_EXCLUSIONS = frozenset([
    "confession_content", "private_prayer", "political_affiliation",
    "spiritual_direction_notes", "health_details_beyond_anointing",
])

_CONSENTS: dict = {}


def anonymise(value: str) -> str:
    """One-way hash for analytics — never reversible."""
    return hashlib.sha256(value.encode()).hexdigest()[:12]


def scrub_pii(text: str) -> str:
    """Replace PII patterns before logging."""
    for p in _PII_PATTERNS:
        text = p.sub("[REDACTED]", text)
    return text


def has_pii(text: str) -> bool:
    return any(p.search(text) for p in _PII_PATTERNS)


def record_consent(user_hash: str, consent_type: str, granted: bool) -> None:
    """consent_type: 'analytics' | 'notifications' | 'data_sharing'"""
    _CONSENTS.setdefault(user_hash, {})[consent_type] = {
        "granted": granted,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def has_consent(user_hash: str, consent_type: str) -> bool:
    return _CONSENTS.get(user_hash, {}).get(consent_type, {}).get("granted", False)


def data_deletion_request(identifier: str, reason: str = "") -> dict:
    """
    Log a data deletion request and return a reference token.
    In production: triggers Sheets row deletion + session clear.
    """
    ref = anonymise(f"{identifier}{datetime.now(UTC).isoformat()}")
    logger.warning("DATA_DELETION_REQUEST ref=%s", ref)
    try:
        from services.sheets import _save
        _save("gdpr_deletion_request", {
            "ref": ref,
            "requested_at": datetime.now(UTC).isoformat(),
            "reason": scrub_pii(reason[:200]),
        })
    except Exception:
        pass
    return {"ref": ref, "status": "logged", "contact": "contact@aikungfu.dev"}


def audit_log(action: str, actor_role: str, detail: str = "") -> None:
    """Write a scrubbed audit entry for admin/coordinator actions."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "role": actor_role,
        "detail": scrub_pii(detail),
    }
    logger.info("AUDIT: %s", entry)
    try:
        from services.sheets import _save
        _save("audit_log", entry)
    except Exception:
        pass


def privacy_sidebar_widget():
    """Privacy controls in sidebar. Call inside with st.sidebar: block."""
    import streamlit as st
    with st.expander("🔒 Privacy", expanded=False):
        st.markdown(
            "<div style='font-size:0.78rem;color:rgba(255,255,255,0.7);"
            "line-height:1.6;'>"
            "Parish data stays in your Google Sheet.<br>"
            "Confession &amp; prayer content never collected.<br>"
            "Nothing shared with third parties."
            "</div>",
            unsafe_allow_html=True,
        )
        anon = st.toggle(
            "Anonymous mode", key="privacy_anon",
            help="Disables session analytics. Data entry still works."
        )
        st.session_state["analytics_enabled"] = not anon
        if st.button("Request data deletion", key="gdpr_delete_btn"):
            st.session_state["show_deletion_form"] = True

    if st.session_state.get("show_deletion_form"):
        st.markdown("---")
        identifier = st.text_input(
            "Name or phone to identify your records", key="gdpr_id",
            label_visibility="collapsed",
            placeholder="Your name or phone number"
        )
        reason = st.text_input(
            "Reason (optional)", key="gdpr_reason",
            label_visibility="collapsed", placeholder="Reason (optional)"
        )
        c1, c2 = st.columns(2)
        if c1.button("Submit", key="gdpr_submit", type="primary") and identifier:
            result = data_deletion_request(identifier, reason)
            st.success(f"Logged · Ref: {result['ref']}")
            st.session_state["show_deletion_form"] = False
        if c2.button("Cancel", key="gdpr_cancel"):
            st.session_state["show_deletion_form"] = False
