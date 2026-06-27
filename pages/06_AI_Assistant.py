"""
AI Parish Assistant — self-contained. No service abstraction.
Auto-discovers available models via /v1beta/models.
"""
import os
import json
import time
import urllib.request
import urllib.error
import streamlit as st

# ── Mobile CSS ──────────────────────────────────────────────────────────────
import sys as _sys
_sys.path.insert(0, ".")
try:
    from services.mobile_ux import inject_mobile_css as _inj; _inj()
except Exception:
    pass


st.set_page_config(page_title="Jumuia — Parish Community", page_icon="✝️", layout="wide")

try:
    from services.theme import inject, hero, section_label
    inject()
except Exception:
    pass

try:
    from services.parish_identity import ai_context as _parish_context
except Exception:
    def _parish_context(): return ""

try:
    from services.magisterial import classify_query as _classify, log_sensitive as _log_sensitive
except Exception:
    def _classify(t): return {"sensitive": False}
    def _log_sensitive(*a): pass

SUPPORTED_LANGUAGES = {
    "en": "English",
    "sw": "Kiswahili",
    "fr": "Français",
    "es": "Español",
    "pt": "Português",
    "lg": "Luganda",
    "ig": "Igbo",
    "tl": "Tagalog",
    "pl": "Polski",
    "it": "Italiano",
    "de": "Deutsch",
    "ar": "العربية",
    "hi": "हिन्दी",
}

from datetime import date as _date

def _current_catholic_facts() -> str:
    """Return time-sensitive Catholic facts for injection into every system prompt.
    Keeps the AI grounded in the actual present, not its training-data snapshot.
    Update this block whenever significant Church facts change.
    """
    today = _date.today()
    # Liturgical year 2025-26 = Year A (Matthew); cycle restarts 1st Sunday of Advent ~Nov 30
    liturigcal_year = "A" if today < _date(today.year, 11, 30) else "B"
    return (
        f"TODAY'S DATE: {today.strftime('%B %d, %Y')}. "
        f"CURRENT POPE: Pope Leo XIV (Robert Francis Prevost), elected May 8, 2025 — "
        f"he succeeded Pope Francis, who died April 21, 2025. "
        f"Pope Leo XIV is the 267th pope, the first American-born pope, and the first from the Order of Saint Augustine. "
        f"His episcopal motto is 'In Illo uno unum' (In the One, we are one). "
        f"LITURGICAL YEAR: {today.year}-{today.year+1 if today.month >= 9 else today.year}, Year {liturigcal_year} of the three-year Sunday cycle. "
        f"Do NOT refer to Pope Francis as the current pope — he has passed away. "
        f"Do NOT fabricate papal statements, encyclicals, or magisterial documents — only cite ones you are certain exist."
    )

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

def _search_tool_for(model: str) -> list:
    """Return the correct Google Search grounding tool block for a given model.
    - gemini-2.0-*: uses the new {google_search: {}} format
    - gemini-1.5-*: uses google_search_retrieval with dynamic mode
    - others / unknown: no tool (safe fallback)
    Search grounding lets the model query Google in real-time when it needs
    current information — current pope, today's readings, recent Vatican news, etc.
    Cached responses skip grounding (ttl=3600) so we don't burn quota on repeats.
    """
    if model.startswith("gemini-2."):
        return [{"google_search": {}}]
    if model.startswith("gemini-1.5"):
        return [{"google_search_retrieval": {
            "dynamic_retrieval_config": {
                "mode": "MODE_DYNAMIC",
                "dynamic_threshold": 0.4,  # only search when model judges it necessary
            }
        }}]
    return []  # older models: no tool


def _extract_text(data: dict) -> tuple[str, bool]:
    """Extract (text, was_grounded) from a generateContent response.
    was_grounded=True means the model used Google Search to answer.
    """
    candidate = data["candidates"][0]
    parts = candidate["content"]["parts"]
    text = " ".join(p["text"] for p in parts if "text" in p).strip()
    # groundingMetadata present = model actually queried Google
    grounded = bool(candidate.get("groundingMetadata", {}).get("webSearchQueries"))
    return text, grounded


def _generate(prompt: str, api_key: str, model: str, use_search: bool = True) -> str:
    """Call Gemini generateContent. Enables Google Search grounding by default.

    Search grounding gives the model real-time access to Google Search results,
    which keeps answers current (today's pope, Vatican news, daily readings, etc.)
    without any scraping or manual data maintenance.

    Responses with search enabled are NOT cached (grounding = live data = don't cache).
    Responses without search (fallback models) ARE cached for 1 hour.
    """
    tools = _search_tool_for(model) if use_search else []
    cache_key = f"{model}:{hash(prompt)}" if not tools else None  # no cache for live searches
    now = time.time()
    if cache_key and cache_key in _mem_cache and now - _mem_cache[cache_key]["ts"] < 3600:
        return _mem_cache[cache_key]["val"], False  # cached — grounded=False

    payload: dict = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 1024, "temperature": 0.7},
    }
    if tools:
        payload["tools"] = tools

    data = _post(f"/v1beta/models/{model}:generateContent", payload, api_key)
    text, grounded = _extract_text(data)

    if cache_key:
        _mem_cache[cache_key] = {"val": text, "ts": now}
    return text, grounded

def _safe_gen(prompt, api_key, primary_model):
    """Try primary model with Google Search grounding, cascade to fallbacks on quota (429).

    Attempt order for each model:
    1. With search grounding (real-time Google access)
    2. Without grounding (if model rejects the tool block with 400)
    3. Next model in fallback list (on 429 quota exhaustion)
    """
    FALLBACKS = [
        "gemini-1.5-flash-8b",
        "gemini-1.5-flash",
        "gemini-2.0-flash-lite",
    ]
    candidates = [primary_model] + [m for m in FALLBACKS if m != primary_model]
    for model in candidates:
        # --- Attempt 1: with search grounding ---
        try:
            text, grounded = _generate(prompt, api_key, model, use_search=True)
            return True, text, grounded
        except urllib.error.HTTPError as e:
            body = e.read()[:300].decode("utf-8", "ignore")
            if e.code == 429:
                continue  # quota — try next model
            if e.code == 400:
                # Model may not support the tool block — retry without grounding
                pass
            else:
                try: msg = json.loads(body).get("error", {}).get("message", body[:100])
                except Exception: msg = body[:100]
                return False, msg, False
        except Exception as e:
            return False, str(e)[:100], False

        # --- Attempt 2: without grounding (graceful degradation) ---
        try:
            text, _ = _generate(prompt, api_key, model, use_search=False)
            return True, text, False
        except urllib.error.HTTPError as e:
            body = e.read()[:300].decode("utf-8", "ignore")
            if e.code == 429:
                continue
            try: msg = json.loads(body).get("error", {}).get("message", body[:100])
            except Exception: msg = body[:100]
            return False, msg, False
        except Exception as e:
            return False, str(e)[:100], False

    return False, "quota", False  # all models exhausted

_DEMO = [
    (["what are you","who are you"], "I'm the Jumuia — Parish Community assistant — here to help with Mass times, sacraments, the liturgical calendar, prayers, and parish questions in any language. For pastoral counseling, please speak with your priest or deacon."),
    (["mass","misa","messe","misa","mass time","when is mass"], "Mass times vary by parish. Use the Find a Church page to locate your nearest church and its schedule. Mass schedules vary widely by parish — use the Find a Church page to locate your nearest church and its times."),
    (["rosary","rozari","chapelet","rosário"], "The Rosary is prayed on five mysteries depending on the day: Joyful (Mon/Sat), Luminous (Thu), Sorrowful (Tue/Fri), Glorious (Wed/Sun). Visit the Daily Prayers page for the full guided Rosary."),
    (["sacr","bapti","confirm","euchar","reconcil","confession","anointing","marriage"], "The seven sacraments are Baptism, Confirmation, Eucharist, Reconciliation, Anointing of the Sick, Holy Orders, and Matrimony. Your parish coordinator can help you prepare for any sacrament."),
    (["lent","advent","easter","christmas","season","liturgi"], "The liturgical year moves through Advent, Christmas, Ordinary Time, Lent, and Easter. The Daily Prayers page shows today's season and scripture readings."),
    (["pray","prayer","petition","intercession"], "The Daily Prayers page has the Rosary, Divine Mercy Chaplet, Stations of the Cross, and daily scripture readings. Prayer intentions can also be shared with your SCC or parish community."),
    (["hello","hi","jambo","habari","hola","bonjour","ciao","oi","kumusta"], "Hello! I'm here to help with parish questions — Mass times, sacraments, liturgical calendar, prayers, or translations. How can I help you today?"),
    (["thank","asante","gracias","merci","obrigado"], "You are welcome. May God bless you and your parish community."),
    (["pope","pontiff","papa","holy father","baba mtakatifu","pape","papa"], "The current Pope is Pope Leo XIV (Robert Francis Prevost), elected May 8, 2025. He is the 267th pope, the first American-born pope, and the first from the Order of Saint Augustine. He succeeded Pope Francis, who passed away on April 21, 2025."),
    (["francis","bergoglio"], "Pope Francis (Jorge Mario Bergoglio) served as the 266th pope from 2013 until his passing on April 21, 2025. He was succeeded by Pope Leo XIV (Robert Francis Prevost), elected May 8, 2025."),
]

def _demo(msg):
    m = msg.lower()
    for keys, reply in _DEMO:
        if any(k in m for k in keys): return reply
    return "The assistant is getting ready. In the meantime, you can find Mass times in the Parish Directory, or join the Daily Prayers page. ✝️"

# ── Page ──────────────────────────────────────────────────────────────────────
try:
    hero("AI Parish Assistant", "Multilingual · Liturgically aware · Powered by Gemini", "AI")
except Exception:
    st.title("🤖 AI Parish Assistant")

api_key = _get_key()
_live = False
model = None

if api_key:
    model = _discover_model(api_key)
    _live = bool(model)
    if not _live:
        st.warning(
            "AI service temporarily unavailable — responding with suggested answers. "
            "All other parish tools are working normally.",
            icon="✝️"
        )
else:
    st.info(
        "✝️ The parish assistant is warming up — showing suggested answers while we finalise setup. "
        "Full multilingual responses will be available shortly.",
        icon=None
    )


# ── Admin diagnostic gate ─────────────────────────────────────────────────────
# ?admin=true in URL → visible diagnostics for parish tech coordinator
# Never shown to public users
_is_admin_view = str(st.query_params.get("admin", "")).lower() == "true"
if _is_admin_view:
    st.warning("⚙️ Admin diagnostic mode — not visible to parishioners")
    _has_key = bool(api_key)
    try:
        from services.sheets import is_configured as _sc; _sheets_ok = _sc()
    except Exception: _sheets_ok = False
    _dc1, _dc2 = st.columns(2)
    with _dc1:
        st.markdown("**AI status**")
        st.code(
            f"GOOGLE_API_KEY: {('set ✅' if _has_key else 'MISSING ❌')}\n"
            f"Active model:   {model or 'none — check key'}\n"
            f"Live:           {_live}\n"
            f"SHEETS_ENDPOINT:{(' set ✅' if _sheets_ok else ' not set')}",
            language="text"
        )
    with _dc2:
        st.markdown("**Last error**")
        _last_err = st.session_state.get("_ai_last_error", "None")
        st.code(str(_last_err), language="text")
    st.divider()

tab_chat, tab_translate, tab_homily, tab_insights, tab_comms = st.tabs([
    # tabs intentionally kept simple
    "💬 Chat", "🌍 Translation", "📖 Homily Helper", "📊 Parish Insights", "📣 Announcements"
])

# ── Chat ──────────────────────────────────────────────────────────────────────
with tab_chat:
    st.markdown("**Ask your parish assistant**")
    st.caption("Mass times · Sacraments · Calendar · Ministries · For pastoral counseling, speak with your priest.")

    if "_ai_last_error" not in st.session_state:
        st.session_state["_ai_last_error"] = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_input_counter" not in st.session_state:
        st.session_state.chat_input_counter = 0

    lang_vals = list(SUPPORTED_LANGUAGES.values())
    lang_keys = list(SUPPORTED_LANGUAGES.keys())

    try: section_label("LANGUAGE / LUGHA")
    except Exception: pass
    lang_sel = st.selectbox("Language", lang_vals, label_visibility="collapsed", key="chat_lang")
    lang_code = lang_keys[lang_vals.index(lang_sel)]

    # ── History ABOVE input (natural chat flow) ───────────────────────────────
    if not st.session_state.chat_history:
        st.markdown(
            "<div style='text-align:center;padding:2rem 0;color:#9CA3AF;font-size:0.9rem;'>"
            "✝️ Ask about Mass times, sacraments, prayers, or your parish…</div>",
            unsafe_allow_html=True,
        )

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""<div style="display:flex;gap:.75rem;margin:.6rem 0;">
  <span style="font-size:1.4rem">😊</span>
  <div style="background:rgba(11,31,58,0.06);border-radius:12px;padding:.6rem 1rem;flex:1;font-size:0.95rem;">{msg['content']}</div>
</div>""", unsafe_allow_html=True)
        else:
            badge = "" if _live else " <small style='color:#C9A84C;font-size:.68rem'>(demo)</small>"
            st.markdown(f"""<div style="display:flex;gap:.75rem;margin:.6rem 0;">
  <span style="font-size:1.4rem">✝️</span>
  <div style="background:rgba(201,168,76,.08);border-left:3px solid #C9A84C;border-radius:0 12px 12px 0;padding:.6rem 1rem;flex:1;font-size:0.95rem;">{msg['content']}{badge}</div>
</div>""", unsafe_allow_html=True)

    if st.session_state.chat_history:
        st.markdown("<div style='text-align:right;margin-top:0.25rem;'>", unsafe_allow_html=True)
        if st.button("Clear conversation", key="clear_chat"):
            st.session_state.chat_history = []
            st.session_state.chat_input_counter += 1
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    # ── Input at bottom ───────────────────────────────────────────────────────
    col_input, col_btn = st.columns([6, 1])
    with col_input:
        user_msg = st.text_input("Message", placeholder="Ask anything about your parish…",
                                  label_visibility="collapsed",
                                  key=f"chat_input_{st.session_state.chat_input_counter}")
    with col_btn:
        send_pressed = st.button("Send ↑", type="primary", key="chat_send", use_container_width=True)

    if send_pressed and user_msg.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_msg.strip()})
        _cls = _classify(user_msg.strip())
        if _cls.get("sensitive"):
            _log_sensitive(user_msg.strip()[:30] + "...", _cls)
        if _live:
            lang_name = SUPPORTED_LANGUAGES.get(lang_code, "English")
            sys = (f"You are a Catholic parish assistant serving parishioners worldwide. "
                   f"{_parish_context()} "
                   f"CURRENT FACTS (take these as ground truth, they override your training data): "
                   f"{_current_catholic_facts()} "
                   f"MAGISTERIAL BOUNDARY: "
                   f"1. Never speculate on doctrine — cite the Catechism (CCC) when answering theological questions. "
                   f"2. Never endorse political positions, parties, or candidates. "
                   f"3. Never improvise on moral teaching — defer controversial questions to a priest. "
                   f"4. Never impersonate clergy or claim sacramental authority. "
                   f"5. Use non-authoritative language: 'The Church teaches...' not 'You must...' "
                   f"SCOPE: Help with Mass times, sacraments, liturgical seasons, Catholic traditions, "
                   f"prayer guidance, scripture references, and parish questions. "
                   f"When you don't know specific local details, say so and suggest the person contact "
                   f"their parish directly — never invent names, times, or details. "
                   f"Do not provide pastoral counseling or spiritual direction — refer to a priest or deacon. "
                   f"Always respond in {lang_name}. Keep answers concise — 2-3 sentences unless more is clearly needed.")
            hist = "".join(f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}\n"
                           for m in st.session_state.chat_history[-6:])
            with st.spinner("…"):
                ok, result, was_grounded = _safe_gen(f"{sys}\n\n{hist}Assistant:", api_key, model)
            if ok:
                reply = result
                if was_grounded:
                    reply += "\n\n<small style='color:#9CA3AF;'>🔍 Live search used</small>"
            elif result == "quota": reply = "The assistant is taking a short break. Please try again in a few minutes, or speak with your priest or parish coordinator for any urgent questions."
            else: reply = _demo(user_msg)
        else:
            reply = _demo(user_msg)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.session_state.chat_input_counter += 1
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
            st.info("Translation is being set up — please try again in a few minutes. ✝️", icon=None)
        else:
            prompt = (f"Translate from {src_sel} to {tgt_sel}. Context: {ctx_sel}. "
                      "Preserve liturgical terms and saint names. Return ONLY the translated text.\n\nText:\n" + tr_text.strip())
            with st.spinner(f"Translating to {tgt_sel}…"):
                ok, result, _ = _safe_gen(prompt, api_key, model)
            if ok:
                st.success(f"**{tgt_sel}:**")
                st.markdown(f"> {result}")
                st.download_button("Download", result, file_name=f"translation_{tgt_code}.txt")
            elif result == "quota":
                st.info("Translation is taking a short break — please try again in a few minutes. ✝️", icon=None)
            else:
                st.info("Translation is taking a short break — please try again in a few minutes. ✝️", icon=None)

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
            st.info("Insights are being set up — please try again in a few minutes. ✝️", icon=None)
        else:
            prompt = (f"Catholic homily preparation assistant for priests/deacons.\n"
                      f"Reading: {gospel_ref}\nSeason: {season}\n"
                      f"Context: {context or 'General parish'}\nAudience: {audience or 'General'}\n"
                      f"Language: {hom_lang}\n\n"
                      "Provide:\n1. Core theological theme\n2. Pastoral message\n"
                      "3. 2-3 life-application points\n4. Opening image\n5. Closing prayer prompt\n"
                      "Clear headers. Pastoral not academic.")
            with st.spinner("Preparing notes…"):
                ok, result, _ = _safe_gen(prompt, api_key, model)
            if ok:
                st.markdown(result)
                st.caption("⚠️ Preparation aid only — does not replace personal prayer or the priest's own discernment.")
                st.download_button("Download", result, file_name="homily_notes.txt")
            elif result == "quota":
                st.info("The assistant is resting — please try again in a little while. ✝️", icon=None)
            else:
                st.info("Homily notes are temporarily unavailable. Please try again shortly. ✝️", icon=None)

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
                ok, result, _ = _safe_gen(f"{PROMPTS[ins_type]}\n\nData:\n{parish_data.strip()}", api_key, model)
            if ok:
                st.markdown(result)
                st.download_button("Download", result, file_name="parish_insights.txt")
            elif result == "quota":
                st.info("The assistant is resting — please try again in a little while. ✝️", icon=None)
            else:
                st.info("Parish insights are temporarily unavailable. Please try again shortly. ✝️", icon=None)

# ── Announcements & Crisis Composer ──────────────────────────────────────────
with tab_comms:
    st.markdown("**Parish Announcements & Crisis Drafts**")
    st.caption(
        "Template-based drafts only — always reviewed and signed by parish leadership before sending. "
        "No announcement is issued directly from this tool."
    )
    st.info(
        "⚠️ **DRAFT MODE** — All output is a starting draft. "
        "Final language, facts, and approval rest with the priest or coordinator.",
        icon="✏️",
    )

    ANNOUNCEMENT_TEMPLATES = {
        "Mass cancellation / reschedule": {
            "icon": "⛪",
            "fields": ["Date/time cancelled", "Reason (optional)", "Alternative arrangement"],
            "prompt": (
                "Write a brief, clear parish announcement that Mass on [Date/time cancelled] is cancelled. "
                "Reason: [Reason]. Alternative: [Alternative arrangement]. "
                "Warm, pastoral tone. 60–90 words. Include a closing blessing. "
                "Start with 'Dear Parishioners,' — no subject line needed here."
            ),
        },
        "Priest transfer / departure": {
            "icon": "✝️",
            "fields": ["Priest name", "Effective date", "Successor (if known)"],
            "prompt": (
                "Write a warm, grateful parish announcement that Fr. [Priest name] will be transferring "
                "effective [Effective date]. Acknowledge their ministry without being effusive. "
                "[Successor]. 80–120 words. Pastoral and dignified."
            ),
        },
        "Emergency appeal": {
            "icon": "🚨",
            "fields": ["Nature of emergency", "Amount needed / goal", "How to give"],
            "prompt": (
                "Write an urgent but calm parish appeal. Emergency: [Nature of emergency]. "
                "Goal: [Amount needed / goal]. How to give: [How to give]. "
                "Urgent but not alarmist. Trust-building. 80–100 words. Include gratitude."
            ),
        },
        "Public clarification": {
            "icon": "📋",
            "fields": ["Topic being clarified", "The correct position", "Who to contact with questions"],
            "prompt": (
                "Write a calm, clear parish clarification on [Topic being clarified]. "
                "Correct position: [The correct position]. Contact: [Who to contact with questions]. "
                "Non-defensive, factual, brief. 60–80 words. No apologies, no defensiveness."
            ),
        },
        "Event postponement": {
            "icon": "📅",
            "fields": ["Event name", "Original date", "New date / TBD", "Reason (optional)"],
            "prompt": (
                "Write a short announcement that [Event name], originally scheduled for [Original date], "
                "has been postponed to [New date / TBD]. Reason: [Reason]. "
                "Clear, brief, friendly. 50–70 words."
            ),
        },
        "New parish programme": {
            "icon": "🌱",
            "fields": ["Programme name", "Who it's for", "Start date and time", "How to join"],
            "prompt": (
                "Write an inviting parish announcement for a new programme: [Programme name]. "
                "For: [Who it's for]. Starts: [Start date and time]. Join: [How to join]. "
                "Enthusiastic but not hyperbolic. 70–90 words. Welcoming tone."
            ),
        },
    }

    template_name = st.selectbox(
        "Announcement type",
        list(ANNOUNCEMENT_TEMPLATES.keys()),
        format_func=lambda k: f"{ANNOUNCEMENT_TEMPLATES[k]['icon']} {k}",
        key="comms_template",
    )

    tmpl = ANNOUNCEMENT_TEMPLATES[template_name]
    st.markdown("**Fill in the details below — the AI will draft from these:**")

    field_values = {}
    for field in tmpl["fields"]:
        field_values[field] = st.text_input(field, key=f"comms_{field}", placeholder=f"Enter {field.lower()}")

    col_lang, col_btn = st.columns([2, 1])
    comms_lang = col_lang.selectbox(
        "Draft in",
        ["English", "Kiswahili", "French", "Spanish", "Portuguese", "Luganda", "Igbo"],
        key="comms_lang",
    )

    if col_btn.button("✏️ Generate Draft", type="primary", key="comms_gen"):
        if not any(field_values.values()):
            st.warning("Fill in at least one field to generate a draft.")
        else:
            prompt_text = tmpl["prompt"]
            for field, val in field_values.items():
                prompt_text = prompt_text.replace(f"[{field}]", val or f"[{field}]")

            lang_instruction = "" if comms_lang == "English" else f" Write the draft in {comms_lang}."
            full_prompt = (
                "You are a parish communications assistant. Produce a single draft only — "
                "clear, pastoral, dignified. No preamble, no options, no commentary after. "
                "Mark the top line as: DRAFT - FOR REVIEW BY PARISH LEADERSHIP\n\n"
                + prompt_text + lang_instruction
            )

            if not _live:
                st.info("This feature is being set up — please try again in a few minutes. ✝️", icon=None)
            else:
                with st.spinner("Drafting…"):
                    ok, result, _ = _safe_gen(full_prompt, api_key, model)
                if ok:
                    st.markdown("---")
                    st.markdown(result)
                    st.download_button(
                        "📥 Download draft",
                        result,
                        file_name=f"draft_{template_name.replace(' ', '_').lower()}.txt",
                        key="comms_dl",
                    )
                    st.caption(
                        "This is a draft only. Verify all facts, dates, and names before publishing. "
                        "All parish communications require approval from the priest or coordinator."
                    )
                elif result == "quota":
                    st.info("The assistant is resting — please try again in a little while. ✝️", icon=None)
                else:
                    st.info("The draft assistant is temporarily unavailable. Please try again shortly. ✝️", icon=None)

# ── Admin-only status (hidden unless ?admin=1 in URL) ─────────────────────────
_params = st.query_params
if _params.get("admin") == "1":
    with st.expander("🔧 Technical status (admin)", expanded=True):
        st.markdown(f"**Model:** `{model or 'none'}`")
        st.markdown(f"**Status:** {'✅ Live' if _live else '⚠️ Demo mode'}")
        if st.button("Re-discover model", key="rediscover"):
            st.cache_data.clear()
            st.rerun()
