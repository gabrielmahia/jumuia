"""
AI Service — Catholic Network Tools
Gemini-powered via google-genai (current SDK).

Model tiers:
  gemini-2.0-flash      → translation, chat bot, parish insights (fast, affordable)
  gemini-2.0-flash      → homily helper (sufficient depth; pro has quota limits on free tier)
"""

import os, logging
logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "en": "English",
    "sw": "Kiswahili",
    "fr": "French",
    "es": "Spanish",
    "pt": "Portuguese",
    "lg": "Luganda",
}

_genai_available = False
try:
    from google import genai as _genai
    _genai_available = True
except ImportError:
    try:
        import google.generativeai as _genai_legacy
    except ImportError:
        pass


def _client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set in Streamlit secrets.")
    if not _genai_available:
        raise EnvironmentError("google-genai package not installed.")
    return _genai.Client(api_key=api_key)


FLASH = "gemini-2.0-flash"   # fast, free tier, 15 RPM


def _generate(prompt: str, model: str = FLASH) -> str:
    client = _client()
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text.strip()


# ─── 1. TRANSLATION ───────────────────────────────────────────────────────────

def translate_text(text, target_language_code, source_language_code="en",
                   context="Catholic parish communication"):
    if target_language_code not in SUPPORTED_LANGUAGES:
        return {"success": False, "translated": text, "model": None,
                "error": f"Unsupported language: {target_language_code}"}
    target = SUPPORTED_LANGUAGES[target_language_code]
    source = SUPPORTED_LANGUAGES.get(source_language_code, "English")
    prompt = (
        f"Translate from {source} to {target}. Context: {context}.\n"
        "Preserve liturgical terminology and saint names. Return ONLY the translated text.\n\n"
        f"Text:\n{text}"
    )
    try:
        return {"success": True, "translated": _generate(prompt),
                "model": FLASH, "error": None}
    except Exception as e:
        logger.error("Translation error: %s", e)
        return {"success": False, "translated": text, "model": None, "error": str(e)}


# ─── 2. HOMILY HELPER ─────────────────────────────────────────────────────────

_HOMILY_SYSTEM = """You are a Catholic homily preparation assistant for priests and deacons.
Deep knowledge of Scripture, Catechism, liturgical calendar.
This is a preparation aid only — never a finished homily.
Ground content in Scripture and authentic Catholic teaching.
Be pastorally sensitive. Avoid political commentary."""

def homily_helper(gospel_reference, liturgical_season, parish_context="",
                  language_code="en", audience="general parish community"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    prompt = (
        f"{_HOMILY_SYSTEM}\n\nPrepare homily notes:\n"
        f"Reading/Gospel: {gospel_reference}\nSeason: {liturgical_season}\n"
        f"Parish context: {parish_context or 'General mixed-age parish'}\n"
        f"Audience: {audience}\nDelivery language: {lang}\n\n"
        "Provide:\n1. Core theological theme (2–3 sentences)\n"
        "2. Key pastoral message\n3. 2–3 concrete life-application points\n"
        "4. Suggested opening image or story angle\n5. Closing personal prayer prompt\n"
        "Use clear headers. Keep each section concise."
    )
    disclaimer = ("⚠️ PREPARATION AID ONLY — Does not replace prayer, personal "
                  "discernment, or the priest's own pastoral judgment.")
    try:
        return {"success": True, "content": _generate(prompt),
                "disclaimer": disclaimer, "model": FLASH, "error": None}
    except Exception as e:
        logger.error("Homily error: %s", e)
        return {"success": False, "content": "", "disclaimer": disclaimer,
                "model": None, "error": str(e)}


# ─── 3. PARISH INSIGHTS ───────────────────────────────────────────────────────

def generate_parish_insights(parish_data, insight_type="community_summary"):
    PROMPTS = {
        "community_summary": "Summarize this parish data in plain language for a coordinator. Highlight strengths, areas needing attention, 2–3 next steps. Max 250 words. No jargon.",
        "action_brief": "Produce 'What Needs Attention This Week' — max 5 items, one sentence each. Plain language.",
        "monthly_report": "Write a concise monthly parish report for a priest. Community health, ministry activity, suggested focus. Warm, professional. Max 300 words.",
    }
    prompt = f"{PROMPTS.get(insight_type, PROMPTS['community_summary'])}\n\nParish data:\n{parish_data}"
    try:
        return {"success": True, "insights": _generate(prompt),
                "insight_type": insight_type, "model": FLASH, "error": None}
    except Exception as e:
        return {"success": False, "insights": "", "insight_type": insight_type,
                "model": None, "error": str(e)}


# ─── 4. CHAT BOT ─────────────────────────────────────────────────────────────

_BOT_SYSTEM = """You are a helpful assistant for a Catholic parish.
Help with: finding parishes, Mass times, liturgical calendar, Catholic teaching (informational), parish services.
Do NOT give pastoral counseling, doctrinal rulings. Refer spiritual questions to the parish priest.
Be warm, respectful, concise. Max 3 sentences unless asked for more."""

def bot_respond(user_message, conversation_history, language_code="en"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    history = ""
    for msg in conversation_history[-6:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history += f"{role}: {msg['content']}\n"
    prompt = (
        f"{_BOT_SYSTEM}\nRespond in {lang}.\n\n"
        f"Conversation:\n{history}\nUser: {user_message}\n\nAssistant:"
    )
    try:
        return {"success": True, "reply": _generate(prompt),
                "model": FLASH, "error": None}
    except Exception as e:
        return {"success": False, "reply": "Sorry, couldn't process that. Please try again.",
                "model": None, "error": str(e)}
