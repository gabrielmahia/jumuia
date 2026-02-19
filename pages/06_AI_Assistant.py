"""AI Assistant — Translation, Homily Helper, Parish Insights, Chat
Powered by Gemini 2.0 (Google) via services/ai_service.py
"""
import streamlit as st
import os, sys
sys.path.insert(0, ".")

st.set_page_config(page_title="AI Parish Assistant", page_icon="🤖", layout="wide")

_AI_AVAILABLE = False
_ai_error_msg = ""

try:
    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if k in st.secrets:
            os.environ[k] = st.secrets[k]
    from services.ai_service import (
        translate_text, homily_helper, generate_parish_insights, bot_respond, SUPPORTED_LANGUAGES,
    )
    _AI_AVAILABLE = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    if not _AI_AVAILABLE:
        _ai_error_msg = "AI key not yet configured."
except Exception as e:
    _ai_error_msg = str(e)

st.title("🤖 AI Parish Assistant")
st.caption("Multilingual · Liturgically aware · Powered by Gemini")

if not _AI_AVAILABLE:
    st.warning(
        "AI features need a Gemini API key to activate. "
        "A free key is available at aistudio.google.com — ask your parish coordinator to add it.",
        icon="🔑",
    )
    st.markdown("""
**When active, this assistant helps with:**
- 💬 **Chat** — Mass times, sacraments, liturgical calendar questions
- 🌍 **Translation** — English ↔ Kiswahili / Luganda / French / Spanish / Portuguese
- 📖 **Homily Helper** — Preparation notes for priests and deacons
- 📊 **Parish Insights** — Plain-language analysis of parish data
""")
    st.stop()

_all_langs = list(SUPPORTED_LANGUAGES.values())
lang_options = {v: k for k, v in SUPPORTED_LANGUAGES.items()}

tab1, tab2, tab3, tab4 = st.tabs(
    ["💬 Chat", "🌍 Translation", "📖 Homily Helper", "📊 Parish Insights"]
)

with tab1:
    st.subheader("Ask your parish assistant")
    st.caption("Mass times · Sacraments · Calendar · Ministries. For pastoral counseling, speak with your priest.")
    sel = st.selectbox("Language / Lugha", _all_langs, key="chat_lang")
    lang_code = lang_options[sel]

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
                st.error(f"Error: {result['error']}")

    if st.session_state.chat_history and st.button("Clear conversation", key="clr_chat"):
        st.session_state.chat_history = []
        st.rerun()

with tab2:
    st.subheader("Translate parish text")
    st.caption("Preserves liturgical terminology and saint names.")
    c1, c2 = st.columns(2)
    with c1:
        src = st.selectbox("From", _all_langs, key="src_lang")
    with c2:
        tgt = st.selectbox("To", [v for v in _all_langs if v != src], key="tgt_lang")
    ctx = st.text_input("Context (optional)", placeholder="Sunday bulletin, announcement…")
    txt = st.text_area("Text to translate", height=120)
    if st.button("Translate", type="primary") and txt.strip():
        sc = [k for k, v in SUPPORTED_LANGUAGES.items() if v == src][0]
        tc = [k for k, v in SUPPORTED_LANGUAGES.items() if v == tgt][0]
        with st.spinner(f"Translating to {tgt}…"):
            r = translate_text(txt, tc, sc, ctx or "Catholic parish communication")
        if r["success"]:
            st.text_area("Translation", r["translated"], height=120)
        else:
            st.error(r["error"])

with tab3:
    st.subheader("Homily Preparation")
    st.warning("Preparation aid only — not a finished homily.", icon="⚠️")
    c1, c2 = st.columns(2)
    with c1:
        gospel_ref = st.text_input("Reading / Gospel", placeholder="John 6:51-58")
        season_sel = st.selectbox("Liturgical season",
            ["Ordinary Time","Advent","Christmas","Lent","Holy Week","Easter"])
    with c2:
        dlang = st.selectbox("Delivery language", _all_langs, key="homily_lang")
        audience = st.text_input("Congregation", value="General mixed-age parish")
    pctx = st.text_area("Parish context (optional)", height=60)
    if st.button("Generate Notes", type="primary") and gospel_ref.strip():
        lc = [k for k, v in SUPPORTED_LANGUAGES.items() if v == dlang][0]
        with st.spinner("Preparing notes…"):
            r = homily_helper(gospel_ref, season_sel, pctx, lc, audience)
        if r["success"]:
            st.info(r["disclaimer"])
            st.markdown(r["content"])
        else:
            st.error(r["error"])

with tab4:
    st.subheader("Parish Data Insights")
    _labels = {
        "community_summary": "Community Summary",
        "action_brief": "What Needs Attention This Week",
        "monthly_report": "Monthly Report (for priest)",
    }
    itype = st.selectbox("Report type", list(_labels.keys()),
                         format_func=lambda x: _labels[x])
    pdata = st.text_area("Parish data", height=180,
        placeholder="Sunday attendance: 240\nGiving this month: KES 42,000\nBaptisms: 3")
    if st.button("Generate Insights", type="primary") and pdata.strip():
        with st.spinner("Generating…"):
            r = generate_parish_insights(pdata, itype)
        if r["success"]:
            st.markdown(r["insights"])
        else:
            st.error(r["error"])
    st.caption("🔒 Data is sent to Gemini for analysis and is not stored. Do not include personally identifiable parishioner data.")
