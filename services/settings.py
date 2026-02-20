"""
Settings Matrix — Catholic Parish Steward
==========================================
Centralised user/parish settings persisted in session state.
Spec §5 Settings Matrix: Localisation, Accessibility, Notifications,
Privacy (via privacy.py), Cultural sensitivity, Sacramental state.
"""

import streamlit as st
from typing import Any

DEFAULTS: dict[str, Any] = {
    "language": "en",
    "scripture_translation": "RSVCE",
    "timezone": "UTC",
    "diocese": "",
    "rite": "Roman",
    "large_text": False,
    "audio_mode": False,
    "low_bandwidth": False,
    "text_only": False,
    "notif_daily_readings": False,
    "notif_feasts": False,
    "notif_confession": False,
    "notif_events": False,
    "notif_lenten_advent": False,
    "analytics_enabled": True,
    "marian_devotion": "standard",
    "prayer_language": "contemporary",
    "sacramental_state": [],
}

SCRIPTURE_TRANSLATIONS = {
    "RSVCE": "RSV Catholic Edition",
    "NAB": "New American Bible",
    "JB": "Jerusalem Bible",
    "NJB": "New Jerusalem Bible",
    "NRSV": "NRSV (Catholic Edition)",
    "DRC": "Douay-Rheims (Traditional)",
    "NABRE": "NABRE (US Lectionary)",
}

RITES = {
    "Roman": "Roman Rite (Ordinary Form)",
    "EF": "Extraordinary Form (Latin Mass)",
    "Ambrosian": "Ambrosian Rite",
}

MARIAN_OPTIONS = {
    "standard": "Standard (Rosary, Angelus)",
    "rosary_daily": "Rosary daily + Mysteries",
    "fatima": "Fatima devotion emphasis",
    "guadalupe": "Our Lady of Guadalupe",
    "africa_mary": "Mary, Mother of Africa",
}

SACRAMENTAL_STATES = [
    "Baptized",
    "Confirmed",
    "Married (Catholic)",
    "Preparing for a sacrament",
    "RCIA (becoming Catholic)",
    "Religious life",
]


def get(key: str) -> Any:
    init()
    return st.session_state.get(f"_setting_{key}", DEFAULTS.get(key))


def set_val(key: str, value: Any) -> None:
    st.session_state[f"_setting_{key}"] = value


def init() -> None:
    for key, default in DEFAULTS.items():
        if f"_setting_{key}" not in st.session_state:
            st.session_state[f"_setting_{key}"] = default
    if st.session_state.get("data_saver"):
        st.session_state["_setting_low_bandwidth"] = True


def settings_page() -> None:
    init()
    try:
        from services.i18n import LANGUAGES
    except Exception:
        LANGUAGES = {"en": "English"}

    st.title("⚙️ Settings")
    st.caption("Personalise your experience · All settings are optional")

    with st.expander("🌍 Language & Localisation", expanded=True):
        c1, c2 = st.columns(2)
        lang_keys = list(LANGUAGES.keys())
        cur_lang = get("language")
        lang_idx = lang_keys.index(cur_lang) if cur_lang in lang_keys else 0
        lang = c1.selectbox("Language", options=lang_keys,
                             format_func=lambda k: LANGUAGES[k],
                             index=lang_idx, key="set_language")
        set_val("language", lang)
        st.session_state["ui_lang"] = lang

        trans_keys = list(SCRIPTURE_TRANSLATIONS.keys())
        cur_trans = get("scripture_translation")
        trans_idx = trans_keys.index(cur_trans) if cur_trans in trans_keys else 0
        trans = c2.selectbox("Scripture translation", options=trans_keys,
                              format_func=lambda k: SCRIPTURE_TRANSLATIONS[k],
                              index=trans_idx, key="set_scripture")
        set_val("scripture_translation", trans)

        c3, c4 = st.columns(2)
        tz = c3.text_input("Timezone", value=get("timezone"),
                            placeholder="e.g. Africa/Nairobi", key="set_tz")
        set_val("timezone", tz or "UTC")
        diocese = c4.text_input("Diocese", value=get("diocese"),
                                 placeholder="e.g. Diocese of Nairobi", key="set_diocese")
        set_val("diocese", diocese)

        rite_keys = list(RITES.keys())
        cur_rite = get("rite")
        rite_idx = rite_keys.index(cur_rite) if cur_rite in rite_keys else 0
        rite = st.selectbox("Liturgical rite", options=rite_keys,
                             format_func=lambda k: RITES[k],
                             index=rite_idx, key="set_rite")
        set_val("rite", rite)

    with st.expander("♿ Accessibility", expanded=False):
        c1, c2 = st.columns(2)
        lt = c1.toggle("Large text mode", value=get("large_text"), key="set_large_text")
        set_val("large_text", lt)
        if lt:
            st.markdown("<style>html { font-size: 120% !important; }</style>",
                        unsafe_allow_html=True)
        lb = c2.toggle("Low bandwidth / Data Saver", value=get("low_bandwidth"), key="set_low_bw")
        set_val("low_bandwidth", lb)
        st.session_state["data_saver"] = lb
        to = c1.toggle("Text-only mode", value=get("text_only"), key="set_text_only",
                        help="Hides charts and decorative images")
        set_val("text_only", to)
        am = c2.toggle("Audio mode", value=get("audio_mode"), key="set_audio",
                        help="Audio delivery via WhatsApp/USSD once channels are live")
        set_val("audio_mode", am)

    with st.expander("🔔 Notifications", expanded=False):
        st.caption("Delivered via WhatsApp or SMS when parish channels are active")
        c1, c2 = st.columns(2)
        set_val("notif_daily_readings",
                c1.toggle("Daily readings", value=get("notif_daily_readings"), key="notif_dr"))
        set_val("notif_feasts",
                c2.toggle("Feast day reminders", value=get("notif_feasts"), key="notif_f"))
        set_val("notif_confession",
                c1.toggle("Confession schedule", value=get("notif_confession"), key="notif_c"))
        set_val("notif_events",
                c2.toggle("Parish events", value=get("notif_events"), key="notif_e"))
        set_val("notif_lenten_advent",
                c1.toggle("Lenten / Advent mode", value=get("notif_lenten_advent"), key="notif_la",
                           help="Extra reflections during penitential seasons"))

    with st.expander("🌺 Cultural & Devotional Preferences", expanded=False):
        marian_keys = list(MARIAN_OPTIONS.keys())
        cur_marian = get("marian_devotion")
        marian_idx = marian_keys.index(cur_marian) if cur_marian in marian_keys else 0
        marian = st.selectbox("Marian devotion style", options=marian_keys,
                               format_func=lambda k: MARIAN_OPTIONS[k],
                               index=marian_idx, key="set_marian")
        set_val("marian_devotion", marian)
        pl = st.radio("Prayer language",
                       options=["contemporary", "traditional"],
                       format_func=lambda x: ("Contemporary (you/your)" if x == "contemporary"
                                               else "Traditional (thee/thou/thy)"),
                       index=0 if get("prayer_language") == "contemporary" else 1,
                       horizontal=True, key="set_prayer_lang")
        set_val("prayer_language", pl)

    with st.expander("✝️ Sacramental Journey (optional)", expanded=False):
        st.caption("Entirely optional. Personalises content. Never required or shared.")
        states = st.multiselect("Select all that apply",
                                 options=SACRAMENTAL_STATES,
                                 default=get("sacramental_state"),
                                 key="set_sac_state")
        set_val("sacramental_state", states)

    st.divider()
    if st.button("✅ Save settings", type="primary"):
        st.success("Settings saved for this session.")
        st.info("To keep settings across sessions, connect Google Sheets — see Admin & Data.",
                icon="💾")
