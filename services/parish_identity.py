"""
Parish Identity — Catholic Parish Steward
==========================================
Lightweight parish context stored in session state.
No login required. Coordinator enters name once per session.
Used by: AI assistant (context injection), page headings,
         Sheets submissions (parish field on every record).

The identity is deliberately minimal — just enough for the
app to feel like it belongs to a specific community,
not a generic demo.
"""

import streamlit as st


_KEY = "parish_identity"
_DEFAULTS = {
    "parish_name": "",
    "city": "",
    "country": "",
    "diocese": "",
    "configured": False,
}


def get() -> dict:
    """Return current parish identity. Always safe to call."""
    return st.session_state.get(_KEY, _DEFAULTS.copy())


def is_set() -> bool:
    return get().get("configured", False)


def parish_name() -> str:
    return get().get("parish_name", "")


def sidebar_widget():
    """
    Compact sidebar parish identity widget.
    Shows name if set, setup prompt if not.
    Call inside a st.sidebar context.
    """
    identity = get()

    if identity.get("configured"):
        st.markdown(
            f"<div style='font-size:0.68rem;color:rgba(201,168,76,0.7);"
            f"text-transform:uppercase;letter-spacing:0.08em;"
            f"margin-bottom:0.15rem;margin-top:0.75rem;'>Your Parish</div>"
            f"<div style='font-size:0.82rem;color:rgba(240,217,138,0.9);"
            f"font-weight:600;margin-bottom:0.1rem;line-height:1.3;'>"
            f"{identity['parish_name']}</div>"
            f"<div style='font-size:0.72rem;color:rgba(255,255,255,0.58);'>"
            f"{identity.get('city','')}{',' if identity.get('city') and identity.get('country') else ''}"
            f" {identity.get('country','')}</div>",
            unsafe_allow_html=True
        )
        if st.button("✏️ Change", key="parish_change_btn",
                     help="Update your parish details"):
            st.session_state[_KEY] = _DEFAULTS.copy()
            st.rerun()
    else:
        st.markdown(
            "<div style='font-size:0.68rem;color:rgba(201,168,76,0.7);"
            "text-transform:uppercase;letter-spacing:0.08em;"
            "margin-bottom:0.3rem;margin-top:0.75rem;'>Your Parish</div>",
            unsafe_allow_html=True
        )
        with st.expander("Set up →", expanded=True):
            name = st.text_input("Parish name", placeholder="e.g. Holy Family Basilica",
                                  key="pi_name", label_visibility="collapsed")
            col1, col2 = st.columns(2)
            city = col1.text_input("City", placeholder="City", key="pi_city",
                                    label_visibility="collapsed")
            country = col2.text_input("Country", placeholder="Country", key="pi_country",
                                       label_visibility="collapsed")
            diocese = st.text_input("Diocese (optional)", placeholder="Diocese",
                                     key="pi_diocese", label_visibility="collapsed")
            if st.button("Save", key="pi_save", type="primary",
                         use_container_width=True) and name:
                st.session_state[_KEY] = {
                    "parish_name": name.strip(),
                    "city": city.strip(),
                    "country": country.strip(),
                    "diocese": diocese.strip(),
                    "configured": True,
                }
                st.rerun()


def inject_into_record(data: dict) -> dict:
    """Add parish context fields to any Sheets submission."""
    identity = get()
    if identity.get("configured"):
        return {
            "parish_name": identity.get("parish_name", ""),
            "parish_city": identity.get("city", ""),
            "parish_country": identity.get("country", ""),
            **data,
        }
    return data


def ai_context() -> str:
    """Return a system prompt fragment for the AI assistant."""
    identity = get()
    if not identity.get("configured"):
        return ""
    name = identity.get("parish_name", "")
    city = identity.get("city", "")
    country = identity.get("country", "")
    diocese = identity.get("diocese", "")
    parts = [f"You are serving {name}"]
    if city and country:
        parts.append(f"located in {city}, {country}")
    elif country:
        parts.append(f"in {country}")
    if diocese:
        parts.append(f"in the Diocese of {diocese}")
    return ". ".join(parts) + ". Tailor your answers to this parish's context where relevant."
