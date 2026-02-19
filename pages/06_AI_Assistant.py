"""AI Assistant — Translation, Homily Helper, Parish Insights, Chat
Powered by Gemini (Google) via services/ai_service.py
"""
import streamlit as st
import os
import sys
sys.path.insert(0, ".")

st.set_page_config(page_title="AI Assistant — CNT", page_icon="🤖", layout="wide")

_AI_AVAILABLE = False
_ai_error_msg = ""

try:
    for secret_key in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if secret_key in st.secrets:
            os.environ[secret_key] = st.secrets[secret_key]
    from services.ai_service import (
        translate_text, homily_helper, generate_parish_insights, bot_respond, SUPPORTED_LANGUAGES,
    )
    _AI_AVAILABLE = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    if not _AI_AVAILABLE:
        _ai_error_msg = "GEMINI_API_KEY not configured in Streamlit secrets."
except ImportError as e:
    _ai_error_msg = f"AI service unavailable: {e}"

st.title("🤖 AI Parish Assistant")
st.caption("Powered by Gemini (Google) · Multilingual · Liturgically aware")

if not _AI_AVAILABLE:
    st.warning(
        f"⚠️ **AI features offline.** {_ai_error_msg}\n\n"
        "Add `GEMINI_API_KEY` to Streamlit secrets (`Settings → Secrets`).\n\n"
        "Get a free key at [aistudio.google.com](https://aistudio.google.com) → API Keys.",
        icon="🔑",
    )
    st.markdown("""
**Features when live:**
- 💬 **Chat Bot** — Mass times, sacraments, liturgical calendar
- 🌍 **Translation** — English ↔ Swahili / Luganda / French / Spanish / Portuguese
- 📖 **Homily Helper** — Preparation notes for priests and deacons
- 📊 **Parish Insights** — Plain-language analysis of parish activity data
""")
    st.stop()

_all_langs = list(SUPPORTED_LANGUAGES.values())
lang_options = {v: k for k, v in SUPPORTED_LANGUAGES.items()}

tab1, tab2, tab3, tab4 = st.tabs(
    ["💬 Chat Bot", "🌍 Translation", "📖 Homily Helper", "📊 Parish Insights"]
)

with tab1:
    st.subheader("Parish Assistant Chat")
    st.caption("Ask about Mass times, sacraments, the liturgical calendar. For pastoral counseling: speak with your priest.")
    sel = st.selectbox("Chat language", _all_langs, key="chat_lang")
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
            with st.spinner("Thinking…"):
                result = bot_respond(prompt, st.session_state.chat_history, language_code=lang_code)
            if result["success"]:
                st.markdown(result["reply"])
                st.caption(f"Model: {result.get('model','gemini')}")
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state.chat_history.append({"role": "assistant", "content": result["reply"]})
            else:
                st.error(f"Error: {result['error']}")
    if st.session_state.chat_history:
        if st.button("Clear conversation"):
            st.session_state.chat_history = []
            st.rerun()

with tab2:
    st.subheader("Liturgical Text Translation")
    st.caption("Preserves liturgical terminology and Catholic proper nouns.")
    c1, c2 = st.columns(2)
    with c1:
        src = st.selectbox("Source language", _all_langs, key="src_lang")
    with c2:
        tgt = st.selectbox("Target language", [v for v in _all_langs if v != src], key="tgt_lang")
    ctx = st.text_input("Context (optional)", placeholder="e.g. Sunday bulletin, Mass announcement")
    txt = st.text_area("Text to translate", height=150)
    if st.button("Translate", type="primary"):
        if txt.strip():
            sc = [k for k, v in SUPPORTED_LANGUAGES.items() if v == src][0]
            tc = [k for k, v in SUPPORTED_LANGUAGES.items() if v == tgt][0]
            with st.spinner(f"Translating to {tgt}…"):
                r = translate_text(txt, tc, sc, ctx or "Catholic parish communication")
            if r["success"]:
                st.success("Translation complete")
                st.text_area("Translated text", r["translated"], height=150)
                st.caption(f"Model: {r.get('model','gemini')}")
            else:
                st.error(f"Error: {r['error']}")
        else:
            st.warning("Please enter text to translate.")

with tab3:
    st.subheader("Homily Preparation Assistant")
    st.warning("⚠️ **PREPARATION AID ONLY** — Does not replace prayer or pastoral judgment.", icon="⚠️")
    c1, c2 = st.columns(2)
    with c1:
        gospel_ref = st.text_input("Gospel / Reading reference", placeholder="e.g. John 6:51-58")
        season_sel = st.selectbox("Liturgical season",
            ["Ordinary Time","Advent","Christmas","Lent","Holy Week","Easter","Pentecost"])
    with c2:
        dlang = st.selectbox("Delivery language", _all_langs, key="homily_lang")
        audience = st.text_input("Congregation", value="General mixed-age parish")
    pctx = st.text_area("Parish context (optional)", height=80)
    if st.button("Generate Preparation Notes", type="primary"):
        if gospel_ref.strip():
            lc = [k for k, v in SUPPORTED_LANGUAGES.items() if v == dlang][0]
            with st.spinner("Preparing notes…"):
                r = homily_helper(gospel_ref, season_sel, pctx, lc, audience)
            if r["success"]:
                st.info(r["disclaimer"])
                st.markdown(r["content"])
                st.caption(f"Model: {r.get('model','gemini')}")
            else:
                st.error(f"Error: {r['error']}")
        else:
            st.warning("Please enter a reading reference.")

with tab4:
    st.subheader("Parish Data Insights")
    st.caption("Paste parish activity data for a plain-language report.")
    _labels = {
        "community_summary": "Community Summary (coordinator view)",
        "action_brief": "Action Brief (what needs attention this week)",
        "monthly_report": "Monthly Report (for parish priest)",
    }
    lbl = st.selectbox("Report type", list(_labels.values()))
    itype = {v: k for k, v in _labels.items()}[lbl]
    pdata = st.text_area("Parish data", height=200,
        placeholder="- Sunday attendance: 240 adults\n- Giving this month: KES 42,000\n- Baptisms: 3")
    if st.button("Generate Insights", type="primary"):
        if pdata.strip():
            with st.spinner("Generating insights…"):
                r = generate_parish_insights(pdata, itype)
            if r["success"]:
                st.success("Insights ready")
                st.markdown(r["insights"])
                st.caption(f"Model: {r.get('model','gemini')}")
            else:
                st.error(f"Error: {r['error']}")
        else:
            st.warning("Please enter parish data.")
    st.divider()
    st.caption("🔒 Data is sent to Gemini (Google) for analysis and is not stored. Do not enter personally identifiable parishioner data.")
