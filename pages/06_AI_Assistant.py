"""AI Parish Assistant — Chat, Translation, Homily Helper, Parish Insights."""

import streamlit as st

st.set_page_config(page_title="Catholic Parish Steward", page_icon="✝️", layout="wide")

try:
    from services.theme import inject, hero, section_label
    inject()
except Exception:
    pass

try:
    from services.ai_service import (
        bot_respond, translate_text, homily_helper, generate_parish_insights,
        SUPPORTED_LANGUAGES, diagnose, _last_error_type
    )
    _ai_loaded = True
except Exception as e:
    _ai_loaded = False
    _ai_load_err = str(e)

# ── Page header ───────────────────────────────────────────────────────────────
try:
    hero("AI Parish Assistant", "Multilingual · Liturgically aware · Powered by Gemini", "AI")
except Exception:
    st.title("🤖 AI Parish Assistant")

# ── API key check + diagnostic banner ─────────────────────────────────────────
if not _ai_loaded:
    st.error(f"AI service could not be loaded: {_ai_load_err}")
    st.stop()

key_present = bool(__import__("os").getenv("GEMINI_API_KEY") or __import__("os").getenv("GOOGLE_API_KEY"))

if not key_present:
    st.info(
        "The AI assistant has not been set up for this parish yet. "
        "Contact your parish coordinator to activate it.",
        icon="✝️",
    )
    st.stop()

# ── Run diagnostic (cached 10 min per session) ────────────────────────────────
if "ai_diag" not in st.session_state:
    with st.spinner("Checking AI connection…"):
        st.session_state.ai_diag = diagnose()

diag = st.session_state.ai_diag

if diag["status"] == "ip_restricted":
    st.markdown("""
<div style="background:#FFF3CD;border-left:5px solid #C9A84C;border-radius:8px;
padding:1rem 1.25rem;margin-bottom:1.5rem;">
<strong>⚙️ One quick fix needed</strong><br>
The AI key is configured but Google Cloud Console is blocking requests from external servers.
This is a <strong>30-second fix</strong> — no code change required.
</div>
""", unsafe_allow_html=True)

    with st.expander("📋 Fix instructions (30 seconds)", expanded=True):
        for i, step in enumerate(diag["fix_steps"], 1):
            st.markdown(f"**{i}.** {step}")
        st.markdown("""
---
**Why this happens:** Keys created in Google Cloud Console have 'Application restrictions'
set to 'HTTP referrers' or 'IP addresses' by default, which blocks server-to-server calls.
AI Studio keys are unrestricted by default — creating a fresh one there is the fastest fix.

**Fastest path:** [Open AI Studio → Get API key](https://aistudio.google.com/app/apikey) →
Create API key in existing project → copy it → paste into Streamlit secrets as
`GOOGLE_API_KEY = "..."` → Save.
""")

    st.caption("While the fix is applied, demo responses are shown below.")
    st.divider()

elif diag["status"] == "quota":
    st.warning("Daily AI quota reached — resets at midnight Pacific Time. Demo responses shown.", icon="⏳")
    st.divider()

elif diag["status"] != "ok":
    st.info(diag.get("detail", "AI unavailable. Demo responses shown below."), icon="ℹ️")
    st.divider()


# ── Helper: show errors ────────────────────────────────────────────────────────
def _show_error(result: dict):
    err = result.get("error")
    msg = result.get("message", "")
    if err == "quota":
        st.markdown(f"""
<div style="background:#FFF8E7;border-left:4px solid #C9A84C;border-radius:8px;
padding:1rem 1.25rem;color:#5C4A1E;margin:.5rem 0;">
⏳ {msg}
</div>""", unsafe_allow_html=True)
    elif err == "ip_restricted":
        st.info("Demo response shown — see fix instructions above.", icon="⚙️")
    else:
        st.info(msg or "Not available right now. Please try again shortly.")


# ── Tab layout ─────────────────────────────────────────────────────────────────
tab_chat, tab_translate, tab_homily, tab_insights = st.tabs([
    "💬 Chat", "🌍 Translation", "📖 Homily Helper", "📊 Parish Insights"
])


# ══ CHAT ══════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("**Ask your parish assistant**")
    st.caption("Mass times · Sacraments · Calendar · Ministries · For pastoral counseling, speak with your priest.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    lang_options = list(SUPPORTED_LANGUAGES.items())
    lang_display = [v for _, v in lang_options]
    lang_codes   = [k for k, _ in lang_options]

    try:
        section_label("LANGUAGE / LUGHA")
    except Exception:
        st.markdown("**Language / Lugha**")

    lang_sel = st.selectbox("Language", lang_display, label_visibility="collapsed", key="chat_lang")
    lang_code = lang_codes[lang_display.index(lang_sel)]

    # Chat input
    user_msg = st.text_input(
        "Message",
        placeholder="Ask anything about your parish…",
        label_visibility="collapsed",
        key="chat_input",
    )

    if st.button("Send", type="primary", key="chat_send") and user_msg.strip():
        with st.spinner("…"):
            result = bot_respond(user_msg.strip(), st.session_state.chat_history, lang_code)

        st.session_state.chat_history.append({"role": "user", "content": user_msg.strip()})

        if result.get("success") or result.get("use_demo"):
            reply = result.get("reply", "")
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        else:
            _show_error(result)

    # Display history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
<div style="display:flex;align-items:flex-start;gap:.75rem;margin:.75rem 0;">
  <span style="font-size:1.6rem">😊</span>
  <div style="background:rgba(11,31,58,0.06);border-radius:12px;
  padding:.65rem 1rem;flex:1;">{msg['content']}</div>
</div>""", unsafe_allow_html=True)
        else:
            is_demo = (diag["status"] != "ok")
            badge = " <small style='color:#C9A84C;font-size:0.7rem'>(demo)</small>" if is_demo else ""
            st.markdown(f"""
<div style="display:flex;align-items:flex-start;gap:.75rem;margin:.75rem 0;">
  <span style="font-size:1.6rem">✝️</span>
  <div style="background:rgba(201,168,76,0.08);border-left:3px solid #C9A84C;
  border-radius:0 12px 12px 0;padding:.65rem 1rem;flex:1;">
  {msg['content']}{badge}</div>
</div>""", unsafe_allow_html=True)

    if st.session_state.chat_history:
        if st.button("Clear conversation", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()


# ══ TRANSLATION ══════════════════════════════════════════════════════════════
with tab_translate:
    st.markdown("**Translate parish content**")
    st.caption("Announcements, liturgy, pastoral letters — into 6 African and global languages.")

    c1, c2 = st.columns([2, 1])
    with c1:
        text_input = st.text_area("Text to translate", height=150,
                                   placeholder="Paste parish announcement, homily notes, or bulletin text here…")
    with c2:
        src_sel = st.selectbox("From", list(SUPPORTED_LANGUAGES.values()), key="tr_src")
        tgt_sel = st.selectbox("To",   list(SUPPORTED_LANGUAGES.values()),
                                index=list(SUPPORTED_LANGUAGES.values()).index("Kiswahili"), key="tr_tgt")
        ctx_sel = st.selectbox("Context",
            ["Catholic parish communication","Liturgical text","Pastoral letter",
             "Youth ministry","Community announcement"])

    src_code = [k for k,v in SUPPORTED_LANGUAGES.items() if v == src_sel][0]
    tgt_code = [k for k,v in SUPPORTED_LANGUAGES.items() if v == tgt_sel][0]

    if st.button("Translate", type="primary", key="tr_btn") and text_input.strip():
        if src_code == tgt_code:
            st.warning("Source and target language are the same.")
        else:
            with st.spinner(f"Translating to {tgt_sel}…"):
                result = translate_text(text_input.strip(), tgt_code, src_code, ctx_sel)
            if result["success"]:
                st.success(f"**{tgt_sel} translation:**")
                st.markdown(f"> {result['translated']}")
                st.download_button("Download translation", result["translated"],
                                   file_name=f"translation_{tgt_code}.txt", mime="text/plain")
            else:
                _show_error(result)


# ══ HOMILY HELPER ════════════════════════════════════════════════════════════
with tab_homily:
    st.markdown("**Homily preparation notes**")
    st.caption("For priests and deacons — preparation aids, not replacements for personal prayer.")

    c1, c2 = st.columns(2)
    with c1:
        gospel_ref = st.text_input("Gospel / Reading reference",
                                    placeholder="John 20:1-9 · Luke 15:11-32")
        season     = st.selectbox("Liturgical season",
            ["Ordinary Time","Advent","Christmas","Lent","Easter","Pentecost",
             "Feast Day","Special occasion"])
    with c2:
        audience   = st.text_input("Audience",
                                    placeholder="Mixed families · Youth Mass · Funeral")
        context    = st.text_input("Parish context (optional)",
                                    placeholder="Rural parish · City centre · SCC gathering")
        hom_lang   = st.selectbox("Language",
            list(SUPPORTED_LANGUAGES.values()), key="hom_lang")
        hom_code   = [k for k,v in SUPPORTED_LANGUAGES.items() if v == hom_lang][0]

    if st.button("Generate preparation notes", type="primary", key="hom_btn") and gospel_ref.strip():
        with st.spinner("Preparing notes…"):
            result = homily_helper(gospel_ref.strip(), season,
                                   context.strip(), hom_code,
                                   audience.strip() or "general parish community")
        if result["success"]:
            st.markdown(result["content"])
            st.caption(f"⚠️ {result['disclaimer']}")
            st.download_button("Download notes", result["content"],
                               file_name="homily_notes.txt", mime="text/plain")
        else:
            _show_error(result)


# ══ PARISH INSIGHTS ══════════════════════════════════════════════════════════
with tab_insights:
    st.markdown("**AI-generated parish insights**")
    st.caption("Enter parish data and get a plain-language summary for coordinators or priests.")

    insight_type = st.radio("Report type",
        ["Community summary","Action brief (this week)","Monthly report"],
        horizontal=True, key="ins_type")

    type_map = {
        "Community summary": "community_summary",
        "Action brief (this week)": "action_brief",
        "Monthly report": "monthly_report",
    }

    parish_data = st.text_area("Parish data or notes", height=200,
        placeholder=(
            "Examples:\n"
            "- Sunday attendance: 280 adults, 90 children\n"
            "- 3 upcoming baptisms, 1 marriage preparation\n"
            "- SCC participation up 15% this month\n"
            "- Youth group needs a new coordinator\n"
            "- Roof repair fund: KES 180,000 of KES 600,000 target"
        ))

    if st.button("Generate insights", type="primary", key="ins_btn") and parish_data.strip():
        with st.spinner("Analysing…"):
            result = generate_parish_insights(parish_data.strip(), type_map[insight_type])
        if result["success"]:
            st.markdown(result["insights"])
            st.download_button("Download report", result["insights"],
                               file_name="parish_insights.txt", mime="text/plain")
        else:
            _show_error(result)

# ── Diagnostic refresh ────────────────────────────────────────────────────────
with st.expander("🔧 AI connection status"):
    st.json(diag)
    if st.button("Re-run diagnostic", key="rediag"):
        del st.session_state["ai_diag"]
        st.rerun()
