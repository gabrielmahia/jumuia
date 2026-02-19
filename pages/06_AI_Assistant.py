"""
AI Parish Assistant — self-contained. No service abstraction.
Auto-discovers available models via /v1beta/models.
"""
import os, json, time, urllib.request, urllib.error
import streamlit as st

st.set_page_config(page_title="Catholic Parish Steward", page_icon="✝️", layout="wide")

try:
    from services.theme import inject, hero, section_label
    inject()
except Exception:
    pass

SUPPORTED_LANGUAGES = {
    "en": "English", "sw": "Kiswahili", "fr": "French",
    "es": "Spanish",  "pt": "Portuguese", "lg": "Luganda",
}
_BASE = "https://generativelanguage.googleapis.com"

def _get_key():
    try:
        k = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if k: return k
    except Exception:
        pass
    return os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

def _post(path, payload, api_key, timeout=30):
    url = f"{_BASE}{path}?key={api_key}"
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def _get_json(path, api_key, timeout=15):
    url = f"{_BASE}{path}?key={api_key}"
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read())

@st.cache_data(ttl=3600, show_spinner=False)
def _discover_model(api_key: str):
    """List /v1beta/models and return best available generateContent model."""
    PREFERRED = [
        "gemini-2.0-flash", "gemini-2.0-flash-lite",
        "gemini-1.5-flash", "gemini-1.5-flash-8b",
        "gemini-1.5-flash-latest", "gemini-2.0-flash-exp",
        "gemini-1.0-pro", "gemini-pro",
    ]
    try:
        data = _get_json("/v1beta/models", api_key)
        available = {
            m["name"].split("/")[-1]
            for m in data.get("models", [])
            if "generateContent" in m.get("supportedGenerationMethods", [])
        }
        for p in PREFERRED:
            if p in available:
                return p
        return sorted(available)[0] if available else None
    except Exception:
        return None

_mem_cache: dict = {}

def _generate(prompt: str, api_key: str, model: str) -> str:
    key = f"{model}:{hash(prompt)}"
    now = time.time()
    if key in _mem_cache and now - _mem_cache[key]["ts"] < 3600:
        return _mem_cache[key]["val"]
    data = _post(
        f"/v1beta/models/{model}:generateContent",
        {"contents": [{"parts": [{"text": prompt}]}],
         "generationConfig": {"maxOutputTokens": 1024, "temperature": 0.7}},
        api_key,
    )
    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    _mem_cache[key] = {"val": text, "ts": now}
    return text

def _safe_gen(prompt, api_key, primary_model):
    """Try primary model, cascade to fallbacks on quota (429). Each has separate daily pool."""
    FALLBACKS = [
        "gemini-1.5-flash-8b",
        "gemini-1.5-flash",
        "gemini-2.0-flash-lite",
    ]
    candidates = [primary_model] + [m for m in FALLBACKS if m != primary_model]
    for model in candidates:
        try:
            return True, _generate(prompt, api_key, model)
        except urllib.error.HTTPError as e:
            body = e.read()[:300].decode("utf-8", "ignore")
            if e.code == 429:
                continue  # quota hit — try next model
            try: msg = json.loads(body).get("error", {}).get("message", body[:100])
            except Exception: msg = body[:100]
            return False, msg
        except Exception as e:
            return False, str(e)[:100]
    return False, "quota"  # all models exhausted

_DEMO = [
    (["what are you","who are you"], "I'm the Catholic Parish Steward AI assistant — here to help with Mass times, sacraments, the liturgical calendar, and translating parish announcements. For pastoral counseling, please speak with your priest."),
    (["mass","misa"], "Mass times vary by parish. Use the Parish Directory to find your local church and its schedule. Most parishes in East Africa have Sunday Masses at 7am, 9am, and 11am."),
    (["rosary","rozari"], "The Rosary is prayed on five mysteries depending on the day: Joyful (Mon/Sat), Luminous (Thu), Sorrowful (Tue/Fri), Glorious (Wed/Sun). Visit the Daily Prayers page for the full guided Rosary."),
    (["sacr"], "The seven sacraments are Baptism, Confirmation, Eucharist, Reconciliation, Anointing of the Sick, Holy Orders, and Matrimony. Your parish coordinator can help you prepare for any sacrament."),
    (["hello","hi","jambo","habari"], "Hello! I'm here to help with parish questions — Mass times, sacraments, liturgical calendar, or translations. How can I help you?"),
]

def _demo(msg):
    m = msg.lower()
    for keys, reply in _DEMO:
        if any(k in m for k in keys): return reply
    return "The AI assistant is warming up. Meanwhile: use Parish Directory for churches, Daily Prayers for the Rosary and readings."

# ── Page ──────────────────────────────────────────────────────────────────────
try:
    hero("AI Parish Assistant", "Multilingual · Liturgically aware · Powered by Gemini", "AI")
except Exception:
    st.title("🤖 AI Parish Assistant")

api_key = _get_key()
if not api_key:
    st.info("The AI assistant has not been set up for this parish yet. Contact your parish coordinator to activate it.", icon="✝️")
    st.stop()

model = _discover_model(api_key)
_live = bool(model)

if not _live:
    st.warning("AI service not available right now. Demo responses shown.", icon="⚙️")

tab_chat, tab_translate, tab_homily, tab_insights = st.tabs([
    "💬 Chat", "🌍 Translation", "📖 Homily Helper", "📊 Parish Insights"
])

# ── Chat ──────────────────────────────────────────────────────────────────────
with tab_chat:
    st.markdown("**Ask your parish assistant**")
    st.caption("Mass times · Sacraments · Calendar · Ministries · For pastoral counseling, speak with your priest.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    lang_vals = list(SUPPORTED_LANGUAGES.values())
    lang_keys = list(SUPPORTED_LANGUAGES.keys())

    try: section_label("LANGUAGE / LUGHA")
    except Exception: pass
    lang_sel = st.selectbox("Language", lang_vals, label_visibility="collapsed", key="chat_lang")
    lang_code = lang_keys[lang_vals.index(lang_sel)]

    user_msg = st.text_input("Message", placeholder="Ask anything about your parish…",
                              label_visibility="collapsed", key="chat_input")

    if st.button("Send ↑", type="primary", key="chat_send") and user_msg.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_msg.strip()})
        if _live:
            lang_name = SUPPORTED_LANGUAGES.get(lang_code, "English")
            sys = (f"You are a warm Catholic parish assistant. Help with Mass times, sacraments, "
                   f"liturgical calendar, and parish services. Do NOT provide pastoral counseling — "
                   f"refer those to the priest. Always respond in {lang_name}. Max 3 sentences.")
            hist = "".join(f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}\n"
                           for m in st.session_state.chat_history[-6:])
            with st.spinner("…"):
                ok, result = _safe_gen(f"{sys}\n\n{hist}Assistant:", api_key, model)
            if ok: reply = result
            elif result == "quota": reply = "Daily request limit reached — available again later today."
            else: reply = _demo(user_msg)
        else:
            reply = _demo(user_msg)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""<div style="display:flex;gap:.75rem;margin:.6rem 0;">
  <span style="font-size:1.5rem">😊</span>
  <div style="background:rgba(11,31,58,0.06);border-radius:12px;padding:.6rem 1rem;flex:1;">{msg['content']}</div>
</div>""", unsafe_allow_html=True)
        else:
            badge = "" if _live else " <small style='color:#C9A84C;font-size:.68rem'>(demo)</small>"
            st.markdown(f"""<div style="display:flex;gap:.75rem;margin:.6rem 0;">
  <span style="font-size:1.5rem">✝️</span>
  <div style="background:rgba(201,168,76,.08);border-left:3px solid #C9A84C;border-radius:0 12px 12px 0;padding:.6rem 1rem;flex:1;">{msg['content']}{badge}</div>
</div>""", unsafe_allow_html=True)

    if st.session_state.chat_history:
        if st.button("Clear", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

# ── Translation ───────────────────────────────────────────────────────────────
with tab_translate:
    st.markdown("**Translate parish content**")
    st.caption("Announcements, liturgy, pastoral letters — into 6 languages.")
    c1, c2 = st.columns([2, 1])
    with c1:
        tr_text = st.text_area("Text", height=140, placeholder="Paste parish announcement, homily notes, or bulletin text…")
    with c2:
        src_sel = st.selectbox("From", lang_vals, key="tr_src")
        tgt_sel = st.selectbox("To", lang_vals,
                                index=lang_vals.index("Kiswahili"), key="tr_tgt")
        ctx_sel = st.selectbox("Context", ["Catholic parish communication","Liturgical text","Pastoral letter","Youth ministry"])
    src_code = lang_keys[lang_vals.index(src_sel)]
    tgt_code = lang_keys[lang_vals.index(tgt_sel)]

    if st.button("Translate", type="primary", key="tr_btn") and tr_text.strip():
        if src_code == tgt_code:
            st.warning("Source and target language are the same.")
        elif not _live:
            st.info("Translation requires a live AI connection. Please try again shortly.")
        else:
            prompt = (f"Translate from {src_sel} to {tgt_sel}. Context: {ctx_sel}. "
                      "Preserve liturgical terms and saint names. Return ONLY the translated text.\n\nText:\n" + tr_text.strip())
            with st.spinner(f"Translating to {tgt_sel}…"):
                ok, result = _safe_gen(prompt, api_key, model)
            if ok:
                st.success(f"**{tgt_sel}:**")
                st.markdown(f"> {result}")
                st.download_button("Download", result, file_name=f"translation_{tgt_code}.txt")
            elif result == "quota":
                st.warning("Daily quota reached — available again later today.")
            else:
                st.info("Translation not available right now. Please try again shortly.")

# ── Homily Helper ─────────────────────────────────────────────────────────────
with tab_homily:
    st.markdown("**Homily preparation notes**")
    st.caption("For priests and deacons — aids, not replacements for personal prayer.")
    c1, c2 = st.columns(2)
    with c1:
        gospel_ref = st.text_input("Gospel / Reading", placeholder="John 20:1-9 · Luke 15:11-32")
        season = st.selectbox("Season", ["Ordinary Time","Advent","Christmas","Lent","Easter","Pentecost","Feast Day"])
    with c2:
        audience = st.text_input("Audience", placeholder="Mixed families · Youth · Funeral")
        context = st.text_input("Parish context", placeholder="Rural parish · City · SCC")
        hom_lang = st.selectbox("Language", lang_vals, key="hom_lang")
        hom_code = lang_keys[lang_vals.index(hom_lang)]

    if st.button("Generate notes", type="primary", key="hom_btn") and gospel_ref.strip():
        if not _live:
            st.info("Requires live AI connection. Please try again shortly.")
        else:
            prompt = (f"Catholic homily preparation assistant for priests/deacons.\n"
                      f"Reading: {gospel_ref}\nSeason: {season}\n"
                      f"Context: {context or 'General parish'}\nAudience: {audience or 'General'}\n"
                      f"Language: {hom_lang}\n\n"
                      "Provide:\n1. Core theological theme\n2. Pastoral message\n"
                      "3. 2-3 life-application points\n4. Opening image\n5. Closing prayer prompt\n"
                      "Clear headers. Pastoral not academic.")
            with st.spinner("Preparing notes…"):
                ok, result = _safe_gen(prompt, api_key, model)
            if ok:
                st.markdown(result)
                st.caption("⚠️ Preparation aid only — does not replace personal prayer or the priest's own discernment.")
                st.download_button("Download", result, file_name="homily_notes.txt")
            elif result == "quota":
                st.warning("Daily quota reached — available again later today.")
            else:
                st.info("Notes not available right now. Please try again shortly.")

# ── Parish Insights ───────────────────────────────────────────────────────────
with tab_insights:
    st.markdown("**AI-generated parish insights**")
    st.caption("Enter parish data for a plain-language summary for coordinators or priests.")
    ins_type = st.radio("Report type", ["Community summary","Action brief (this week)","Monthly report"],
                         horizontal=True, key="ins_type")
    parish_data = st.text_area("Parish data", height=170, placeholder=(
        "- Sunday attendance: 280 adults, 90 children\n"
        "- 3 upcoming baptisms, 1 marriage preparation\n"
        "- SCC participation up 15% this month\n"
        "- Youth group needs coordinator\n"
        "- Roof repair: KES 180K of 600K target"
    ))
    PROMPTS = {
        "Community summary": "Summarize this parish data. Highlight 2 strengths, 2 areas needing attention, 3 next steps. Plain language. Max 250 words.",
        "Action brief (this week)": "List 'What Needs Attention This Week' — 5 items, one sentence each. Action-oriented.",
        "Monthly report": "Write a concise monthly parish report for the priest. Community health, ministry activity, one focus area. Warm, professional. Max 300 words.",
    }
    if st.button("Generate insights", type="primary", key="ins_btn") and parish_data.strip():
        if not _live:
            st.info("Requires live AI connection. Please try again shortly.")
        else:
            with st.spinner("Analysing…"):
                ok, result = _safe_gen(f"{PROMPTS[ins_type]}\n\nData:\n{parish_data.strip()}", api_key, model)
            if ok:
                st.markdown(result)
                st.download_button("Download", result, file_name="parish_insights.txt")
            elif result == "quota":
                st.warning("Daily quota reached — available again later today.")
            else:
                st.info("Insights not available right now. Please try again shortly.")

# ── Status ────────────────────────────────────────────────────────────────────
with st.expander("🔧 Connection status", expanded=False):
    st.markdown(f"**Model:** `{model or 'none'}`")
    st.markdown(f"**Status:** {'✅ Live' if _live else '⚠️ Demo mode'}")
    if st.button("Re-discover model", key="rediscover"):
        st.cache_data.clear()
        st.rerun()
