"""AI Assistant — Translation, Homily Helper, Parish Insights, Chat"""
import streamlit as st
import sys
sys.path.insert(0, ".")

from services.ai_service import (
    translate_text,
    homily_helper,
    generate_parish_insights,
    bot_respond,
    SUPPORTED_LANGUAGES,
)

st.set_page_config(page_title="AI Assistant — CNT", page_icon="🤖", layout="wide")
st.title("🤖 AI Assistant")
st.caption("Powered by Claude (Anthropic). Haiku for summaries/translation · Sonnet for homily and insights.")

tab1, tab2, tab3, tab4 = st.tabs(
    ["💬 Chat Bot", "🌍 Translation", "📖 Homily Helper", "📊 Parish Insights"]
)


# ─────────────────────────────────────────────
# TAB 1 — CHAT BOT
# ─────────────────────────────────────────────
with tab1:
    st.subheader("Parish Assistant Chat")
    st.caption(
        "Ask about Mass times, sacraments, the liturgical calendar, or parish services. "
        "For pastoral counseling, please speak with your priest."
    )

    lang_options = {v: k for k, v in SUPPORTED_LANGUAGES.items()}
    selected_lang_name = st.selectbox(
        "Chat language", list(lang_options.keys()), key="chat_lang"
    )
    lang_code = lang_options[selected_lang_name]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display history
    for turn in st.session_state.chat_history:
        with st.chat_message(turn["role"]):
            st.markdown(turn["content"])

    if prompt := st.chat_input("Ask anything about your parish…"):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                result = bot_respond(
                    prompt,
                    st.session_state.chat_history,
                    language_code=lang_code,
                )
            if result["success"]:
                st.markdown(result["reply"])
                st.session_state.chat_history.append({"role": "user",    "content": prompt})
                st.session_state.chat_history.append({"role": "assistant","content": result["reply"]})
            else:
                st.error(f"Error: {result['error']}")

    if st.button("Clear conversation", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()


# ─────────────────────────────────────────────
# TAB 2 — TRANSLATION
# ─────────────────────────────────────────────
with tab2:
    st.subheader("Liturgical Text Translation")
    st.caption("Translate announcements, readings, or parish communications. Preserves liturgical terminology.")

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox(
            "Source language",
            list(SUPPORTED_LANGUAGES.values()),
            key="src_lang",
        )
    with col2:
        target_lang = st.selectbox(
            "Target language",
            [v for v in SUPPORTED_LANGUAGES.values() if v != source_lang],
            key="tgt_lang",
        )

    context = st.text_input(
        "Context (optional)",
        placeholder="e.g. Sunday bulletin, Mass announcement, pastoral letter",
    )
    text_input = st.text_area(
        "Text to translate",
        height=150,
        placeholder="Enter liturgical text, announcement, or parish communication…",
    )

    if st.button("Translate", type="primary", key="translate_btn"):
        if text_input.strip():
            src_code = [k for k, v in SUPPORTED_LANGUAGES.items() if v == source_lang][0]
            tgt_code = [k for k, v in SUPPORTED_LANGUAGES.items() if v == target_lang][0]
            with st.spinner("Translating…"):
                result = translate_text(text_input, tgt_code, src_code, context or "Catholic parish communication")
            if result["success"]:
                st.success("Translation complete")
                st.text_area("Translated text", result["translated"], height=150)
                st.caption(f"Model: {result['model']}")
            else:
                st.error(f"Translation failed: {result['error']}")
        else:
            st.warning("Please enter text to translate.")


# ─────────────────────────────────────────────
# TAB 3 — HOMILY HELPER
# ─────────────────────────────────────────────
with tab3:
    st.subheader("Homily Preparation Assistant")
    st.warning(
        "⚠️ **PREPARATION AID ONLY** — This tool assists priests and deacons with homily preparation. "
        "It does not replace personal prayer, discernment, or pastoral judgment.",
        icon="⚠️",
    )

    col1, col2 = st.columns(2)
    with col1:
        gospel_ref = st.text_input(
            "Gospel / Reading reference",
            placeholder="e.g. John 6:51-58 · Mark 10:35-45",
        )
        liturgical_season = st.selectbox(
            "Liturgical season",
            ["Ordinary Time", "Advent", "Christmas", "Lent",
             "Holy Week", "Easter", "Pentecost"],
        )
    with col2:
        delivery_lang = st.selectbox(
            "Delivery language", list(SUPPORTED_LANGUAGES.values()), key="homily_lang"
        )
        audience = st.text_input(
            "Congregation description",
            placeholder="e.g. Mixed ages, rural parish, many young families",
            value="General mixed-age parish",
        )

    parish_ctx = st.text_area(
        "Parish context (optional)",
        placeholder="Any specific pastoral challenges, recent events, or community needs…",
        height=80,
    )

    if st.button("Generate Preparation Notes", type="primary", key="homily_btn"):
        if gospel_ref.strip():
            lang_code_h = [k for k, v in SUPPORTED_LANGUAGES.items() if v == delivery_lang][0]
            with st.spinner("Preparing homily notes… (Sonnet)"):
                result = homily_helper(
                    gospel_ref, liturgical_season, parish_ctx,
                    lang_code_h, audience
                )
            if result["success"]:
                st.info(result["disclaimer"])
                st.markdown(result["content"])
                st.caption(f"Model: {result['model']}")
            else:
                st.error(f"Error: {result['error']}")
        else:
            st.warning("Please enter a gospel or reading reference.")


# ─────────────────────────────────────────────
# TAB 4 — PARISH INSIGHTS
# ─────────────────────────────────────────────
with tab4:
    st.subheader("Parish Data Insights")
    st.caption(
        "Paste or enter parish activity data and get a plain-language insight report. "
        "Useful for coordinators, priests, and diocesan leaders."
    )

    insight_type = st.selectbox(
        "Report type",
        {
            "community_summary": "Community Summary (coordinator view)",
            "action_brief":      "Action Brief (what needs attention this week)",
            "monthly_report":    "Monthly Report (for parish priest)",
        }.values(),
        key="insight_type_label",
    )

    type_map = {
        "Community Summary (coordinator view)": "community_summary",
        "Action Brief (what needs attention this week)": "action_brief",
        "Monthly Report (for parish priest)": "monthly_report",
    }

    parish_data_input = st.text_area(
        "Parish data",
        height=200,
        placeholder=(
            "Paste numbers, notes, or any structured data:\n"
            "- Sunday attendance: 240 adults, 80 children\n"
            "- Giving this month: KES 42,000\n"
            "- Baptisms: 3  |  Marriages: 1\n"
            "- Youth group attendance down 20% last month\n"
            "- Catechism enrollment: 35 students"
        ),
    )

    if st.button("Generate Insights", type="primary", key="insights_btn"):
        if parish_data_input.strip():
            with st.spinner("Generating insights…"):
                result = generate_parish_insights(
                    parish_data_input, type_map[insight_type]
                )
            if result["success"]:
                st.success("Insights ready")
                st.markdown(result["insights"])
                st.caption(f"Model: {result['model']}")
            else:
                st.error(f"Error: {result['error']}")
        else:
            st.warning("Please enter some parish data.")
