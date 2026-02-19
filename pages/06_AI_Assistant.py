"""AI Assistant — Gemini-powered parish helper."""
import streamlit as st, os, sys
sys.path.insert(0, ".")

st.set_page_config(page_title="AI Parish Assistant", page_icon="🤖", layout="wide")

try:
    from services.theme import inject, hero, quota_notice
    inject()
except Exception:
    pass

# ── Load AI service ───────────────────────────────────────────────────────────
_AI_READY = False
_ai_setup_msg = ""

try:
    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if k in st.secrets:
            os.environ[k] = st.secrets[k]
    from services.ai_service import (
        translate_text, homily_helper, generate_parish_insights,
        bot_respond, SUPPORTED_LANGUAGES,
    )
    _AI_READY = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    if not _AI_READY:
        _ai_setup_msg = "setup"
except Exception:
    _ai_setup_msg = "setup"

# ── Hero ─────────────────────────────────────────────────────────────────────
try:
    hero("AI Parish Assistant", "Multilingual · Liturgically aware · Powered by Gemini", "AI")
except Exception:
    st.title("🤖 AI Parish Assistant")

# ── Not configured ────────────────────────────────────────────────────────────
if not _AI_READY:
    st.info(
        "The AI assistant has not been set up for this parish yet. "
        "Your parish coordinator can activate it — no technical knowledge required.",
        icon="✝️",
    )
    st.markdown("""
**Once activated, this assistant helps with:**

- 💬 **Chat** — Ask about Mass times, sacraments, and the liturgical calendar
- 🌍 **Translation** — Bulletins and announcements in English, Kiswahili, Luganda, French, and more
- 📖 **Homily Helper** — Preparation notes for priests and deacons
- 📊 **Parish Insights** — Plain-language summaries of parish activity
""")
    st.stop()

# ── Helpers ───────────────────────────────────────────────────────────────────
SUPPORTED_LANGUAGES_FALLBACK = {
    "en":"English","sw":"Kiswahili","fr":"French",
    "es":"Spanish","pt":"Portuguese","lg":"Luganda",
}
_langs = SUPPORTED_LANGUAGES if "_AI_READY" else SUPPORTED_LANGUAGES_FALLBACK
_all_langs = list(_langs.values())
_lang_code = {v: k for k, v in _langs.items()}

def _show_error(result: dict):
    """Show a public-friendly message. Never shows technical details."""
    err = result.get("error", "")
    msg = result.get("message", "")

    if err == "quota":
        st.markdown(
            f"""<div style="background:#FFF8E7;border-left:4px solid #C9A84C;
            border-radius:8px;padding:1rem 1.25rem;margin:0.5rem 0;
            color:#5C4A1E;font-size:0.93rem;">
            ⏳ {msg}
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.info(msg or "This feature is not available right now. Please try again in a moment.")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Chat", "🌍 Translation", "📖 Homily Helper", "📊 Parish Insights"
])

# ── CHAT ─────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Ask your parish assistant")
    st.caption("Mass times · Sacraments · Calendar · Ministries · For pastoral counseling, speak with your priest.")

    lang_sel = st.selectbox("Language / Lugha", _all_langs, key="chat_lang",
                            label_visibility="visible")
    lang_code = _lang_code.get(lang_sel, "en")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for turn in st.session_state.chat_history:
        with st.chat_message(turn["role"]):
            st.markdown(turn["content"])

    if prompt := st.chat_input("Ask anything about your parish…"):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("…"):
                result = bot_respond(prompt, st.session_state.chat_history, language_code=lang_code)
            if result["success"]:
                st.markdown(result["reply"])
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state.chat_history.append({"role": "assistant", "content": result["reply"]})
            else:
                _show_error(result)
                # Still show the friendly reply for quota messages
                reply = result.get("reply", "")
                if reply and result.get("error") == "quota":
                    st.markdown(reply)

    if st.session_state.chat_history:
        if st.button("Clear conversation", key="clr_chat"):
            st.session_state.chat_history = []
            st.rerun()

# ── TRANSLATION ───────────────────────────────────────────────────────────────
with tab2:
    st.subheader("Translate parish text")
    st.caption("Liturgical terminology and saint names preserved across all languages.")
    c1, c2 = st.columns(2)
    src = c1.selectbox("From", _all_langs, key="src_lang")
    tgt = c2.selectbox("To", [v for v in _all_langs if v != src], key="tgt_lang")
    ctx = st.text_input("What is this text for? (optional)",
                        placeholder="e.g. Sunday bulletin, Mass announcement")
    txt = st.text_area("Text to translate", height=120)
    if st.button("Translate", type="primary"):
        if not txt.strip():
            st.warning("Please enter some text to translate.")
        else:
            sc = _lang_code.get(src, "en")
            tc = _lang_code.get(tgt, "sw")
            with st.spinner(f"Translating to {tgt}…"):
                r = translate_text(txt, tc, sc, ctx or "Catholic parish communication")
            if r["success"]:
                st.text_area("Translation", r["translated"], height=120)
            else:
                _show_error(r)

# ── HOMILY HELPER ─────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Homily Preparation Notes")
    st.markdown(
        """<div style="background:#F0F7FF;border-left:4px solid #4A90D9;
        border-radius:8px;padding:0.75rem 1rem;font-size:0.9rem;color:#1a3a6b">
        ✝️ These notes are a preparation aid — they do not replace personal prayer or the priest's own discernment.
        </div>""",
        unsafe_allow_html=True,
    )
    st.write("")
    c1, c2 = st.columns(2)
    gospel_ref = c1.text_input("Reading or Gospel passage", placeholder="e.g. John 6:51-58")
    season_sel = c1.selectbox("Liturgical season",
        ["Ordinary Time","Advent","Christmas","Lent","Holy Week","Easter"])
    dlang = c2.selectbox("Delivery language", _all_langs, key="homily_lang")
    audience = c2.text_input("Who is the congregation?", value="General mixed-age parish")
    pctx = st.text_area("Any context about your parish? (optional)", height=60,
        placeholder="e.g. Urban parish, many young families, celebrating a school anniversary…")
    if st.button("Prepare Notes", type="primary"):
        if not gospel_ref.strip():
            st.warning("Please enter a reading or Gospel reference.")
        else:
            lc = _lang_code.get(dlang, "en")
            with st.spinner("Preparing notes…"):
                r = homily_helper(gospel_ref, season_sel, pctx, lc, audience)
            if r["success"]:
                st.caption(r["disclaimer"])
                st.markdown(r["content"])
            else:
                _show_error(r)

# ── PARISH INSIGHTS ───────────────────────────────────────────────────────────
with tab4:
    st.subheader("Parish Activity Insights")
    st.caption("Paste your parish numbers and get a plain-language summary.")
    _labels = {
        "community_summary": "Community Overview — for coordinators",
        "action_brief":      "What Needs Attention This Week",
        "monthly_report":    "Monthly Summary — for the parish priest",
    }
    itype = st.selectbox("What kind of summary do you need?",
                         list(_labels.keys()), format_func=lambda x: _labels[x])
    pdata = st.text_area("Parish data", height=160,
        placeholder="Sunday attendance: 240\nGiving this month: KES 42,000\nBaptisms this quarter: 8\nActive SCCs: 12")
    if st.button("Generate Summary", type="primary"):
        if not pdata.strip():
            st.warning("Please enter some parish data first.")
        else:
            with st.spinner("Preparing summary…"):
                r = generate_parish_insights(pdata, itype)
            if r["success"]:
                st.markdown(r["insights"])
            else:
                _show_error(r)

    st.divider()
    st.caption("Information entered here is used only to generate your summary and is not saved or shared.")
