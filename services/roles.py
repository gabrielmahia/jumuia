"""
Role-Based Access — Catholic Parish Steward
============================================
Spec §4: Design role-based architecture with server-side permission enforcement.

Roles (ascending trust):
    parishioner   — default, public-facing tools only
    catechist     — formation + catechist pages
    coordinator   — full parish coordinator tools
    priest        — coordinator + clergy-specific views (read-only pastoral data)
    diocese_admin — multi-parish view, diocesan reports
    global_admin  — platform team, all access

Implementation note:
    Production path = Firebase Auth / Supabase with JWT.
    Current path = session-based with PIN confirmation (diocese provides PINs).
    Migration path: replace _verify_pin() with JWT decode — no page changes needed.

Usage:
    from services.roles import require_role, current_role, role_gate

    require_role("coordinator")  # blocks page if insufficient role
    role_gate("priest")          # inline check — returns True/False
"""

import hashlib
import logging

logger = logging.getLogger(__name__)

# Role hierarchy — higher index = more trust
ROLES = ["parishioner", "catechist", "coordinator", "priest", "diocese_admin", "global_admin"]

ROLE_LABELS = {
    "parishioner":  "Parishioner",
    "catechist":    "Catechist",
    "coordinator":  "Parish Coordinator",
    "priest":       "Priest / Deacon",
    "diocese_admin":"Diocese Administrator",
    "global_admin": "Platform Administrator",
}

ROLE_ICONS = {
    "parishioner":  "🙏",
    "catechist":    "🎓",
    "coordinator":  "📋",
    "priest":       "✝️",
    "diocese_admin":"⛪",
    "global_admin": "🌐",
}

# Pages requiring minimum role
PAGE_REQUIREMENTS = {
    "Sacraments":           "coordinator",
    "Small Communities":    "catechist",
    "Catechists":           "catechist",
    "Pastoral Care":        "coordinator",
    "Formation & RCIA":     "catechist",
    "Admin & Data":         "coordinator",
    "Transparency":         "coordinator",
}


def _rank(role: str) -> int:
    try:
        return ROLES.index(role)
    except ValueError:
        return 0


def current_role() -> str:
    """Return the current session role. Default: 'parishioner'."""
    import streamlit as st
    return st.session_state.get("_user_role", "parishioner")


def is_at_least(minimum_role: str) -> bool:
    """True if current role meets or exceeds minimum."""
    return _rank(current_role()) >= _rank(minimum_role)


def role_gate(minimum_role: str) -> bool:
    """Inline check — returns True if permitted. Does not block."""
    return is_at_least(minimum_role)


def require_role(minimum_role: str, page_name: str = "") -> None:
    import streamlit as st
    """
    Block a page if the current role is insufficient.
    Shows a clear, actionable upgrade prompt — not a bare error.
    Call at the TOP of any coordinator/catechist page.
    """
    if is_at_least(minimum_role):
        return  # Permitted — continue rendering

    current = current_role()
    icon = ROLE_ICONS.get(minimum_role, "🔒")
    label = ROLE_LABELS.get(minimum_role, minimum_role.title())

    st.warning(
        f"{icon} **{page_name or 'This page'} requires {label} access.**\n\n"
        "Ask your parish coordinator to set your access level in the sidebar, "
        "or select your role below.",
        icon=None,
    )
    _role_upgrade_widget()
    st.stop()


def set_role(role: str) -> None:
    """Set role in session. In production: call only after JWT verification."""
    import streamlit as st
    if role in ROLES:
        st.session_state["_user_role"] = role
        logger.info("Role set: %s", role)
        try:
            from services.privacy import audit_log
            audit_log("role_set", role, f"Role elevated to {role}")
        except Exception:
            pass


def _role_upgrade_widget():
    import streamlit as st
    """
    Session-based role selector with coordinator PIN confirmation.
    In production: replace with SSO/JWT flow.
    """
    st.markdown("---")
    st.markdown("**Access level**")

    cols = st.columns(3)
    visible_roles = ["parishioner", "catechist", "coordinator"]

    for i, role in enumerate(visible_roles):
        with cols[i % 3]:
            icon = ROLE_ICONS[role]
            label = ROLE_LABELS[role]
            is_current = current_role() == role
            if st.button(
                f"{icon} {label}",
                key=f"role_btn_{role}",
                type="primary" if is_current else "secondary",
                use_container_width=True,
            ):
                if role in ("catechist", "coordinator"):
                    st.session_state["_pending_role"] = role
                else:
                    set_role(role)
                    st.rerun()

    # PIN confirmation for elevated roles
    pending = st.session_state.get("_pending_role")
    if pending in ("catechist", "coordinator"):
        pending_label = ROLE_LABELS[pending]
        st.info(
            f"Your coordinator can provide the **{pending_label} PIN** — "
            "set when the parish first connects Google Sheets.",
            icon="🔑"
        )
        pin = st.text_input(
            f"{pending_label} PIN",
            type="password",
            key="role_pin_input",
            placeholder="Enter PIN from your coordinator",
        )
        c1, c2 = st.columns(2)
        if c1.button("Confirm", key="role_confirm", type="primary"):
            if _verify_pin(pending, pin):
                set_role(pending)
                st.session_state.pop("_pending_role", None)
                st.success(f"✅ Access granted: {pending_label}")
                st.rerun()
            else:
                st.error("Incorrect PIN. Ask your parish coordinator.")
        if c2.button("Cancel", key="role_cancel"):
            st.session_state.pop("_pending_role", None)
            st.rerun()


def _verify_pin(role: str, pin: str) -> bool:
    """
    Verify coordinator/catechist PIN.
    PINs stored as SHA-256 hashes in Streamlit secrets or env.
    Default (no secret set): any non-empty PIN grants access — usable for demo/pilot.
    Production: set COORDINATOR_PIN_HASH and CATECHIST_PIN_HASH in Streamlit secrets.
    """
    import os
    if not pin:
        return False

    env_key = f"{role.upper()}_PIN_HASH"
    stored_hash = None

    try:
        import streamlit as st
        stored_hash = st.secrets.get(env_key)
    except Exception:
        pass

    if not stored_hash:
        stored_hash = os.environ.get(env_key)

    if not stored_hash:
        # No PIN configured — accept any non-empty PIN (pilot/demo mode)
        # Log this so coordinators know to set a PIN
        logger.warning("No PIN hash configured for role %s — accepting any PIN (demo mode)", role)
        return len(pin.strip()) >= 4

    pin_hash = hashlib.sha256(pin.strip().encode()).hexdigest()
    return pin_hash == stored_hash


def sidebar_role_badge():
    import streamlit as st
    """Small role badge for the sidebar. Call inside with st.sidebar: block."""
    role = current_role()
    icon = ROLE_ICONS.get(role, "🙏")
    label = ROLE_LABELS.get(role, role.title())

    is_elevated = role != "parishioner"

    color = "rgba(201,168,76,0.8)" if is_elevated else "rgba(255,255,255,0.35)"
    st.markdown(
        f"<div style='font-size:0.68rem;color:{color};margin-top:0.5rem;"
        f"text-align:center;font-weight:600;letter-spacing:0.05em;'>"
        f"{icon} {label}</div>",
        unsafe_allow_html=True,
    )
