"""
AI Service — Catholic Network Tools
Gemini-powered: translation, homily preparation, parish insights, chat bot.

Model governance:
  gemini-1.5-flash → translation, summary, chat bot  (fast + affordable)
  gemini-1.5-pro   → homily helper, theological reflection (depth required)
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

_gemini_available = False
try:
    import google.generativeai as genai
    _gemini_available = True
except ImportError:
    pass


def _configure():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set. Add to Streamlit secrets.")
    if _gemini_available:
        genai.configure(api_key=api_key)


def _flash():
    _configure()
    return genai.GenerativeModel("gemini-1.5-flash")


def _pro():
    _configure()
    return genai.GenerativeModel("gemini-1.5-pro")


def translate_text(text, target_language_code, source_language_code="en",
                   context="Catholic parish communication"):
    if target_language_code not in SUPPORTED_LANGUAGES:
        return {"success": False, "translated": text, "model": None,
                "error": f"Unsupported language: {target_language_code}"}
    target = SUPPORTED_LANGUAGES[target_language_code]
    source = SUPPORTED_LANGUAGES.get(source_language_code, "English")
    prompt = (
        f"Translate from {source} to {target}. Context: {context}.\n"
        "Preserve liturgical terminology, saint names. Return ONLY the translated text.\n\n"
        f"Text:\n{text}"
    )
    try:
        resp = _flash().generate_content(prompt)
        return {"success": True, "translated": resp.text.strip(),
                "model": "gemini-1.5-flash", "error": None}
    except Exception as e:
        logger.error("Translation error: %s", e)
        return {"success": False, "translated": text, "model": None, "error": str(e)}


HOMILY_SYSTEM = """You are a Catholic homily preparation assistant for priests and deacons.
Deep knowledge of Scripture, Catechism, liturgical calendar.
This is a preparation aid only — never a finished homily.
Ground all content in Scripture and authentic Catholic teaching.
Be pastorally sensitive. Avoid political commentary."""


def homily_helper(gospel_reference, liturgical_season, parish_context="",
                  language_code="en", audience="general parish community"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    prompt = (
        f"{HOMILY_SYSTEM}\n\nPrepare homily notes:\n"
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
        resp = _pro().generate_content(prompt)
        return {"success": True, "content": resp.text.strip(),
                "disclaimer": disclaimer, "model": "gemini-1.5-pro", "error": None}
    except Exception as e:
        logger.error("Homily error: %s", e)
        return {"success": False, "content": "", "disclaimer": disclaimer,
                "model": None, "error": str(e)}


def generate_parish_insights(parish_data, insight_type="community_summary"):
    PROMPTS = {
        "community_summary": "Summarize this parish data in plain language for a coordinator. Highlight strengths, areas needing attention, 2–3 next steps. Max 250 words. No jargon.",
        "action_brief": "Produce 'What Needs Attention This Week' — max 5 items, one sentence each. Plain language.",
        "monthly_report": "Write a concise monthly parish report for a priest. Community health, ministry activity, suggested focus. Warm, professional. Max 300 words.",
    }
    prompt = f"{PROMPTS.get(insight_type, PROMPTS['community_summary'])}\n\nParish data:\n{parish_data}"
    try:
        resp = _flash().generate_content(prompt)
        return {"success": True, "insights": resp.text.strip(),
                "insight_type": insight_type, "model": "gemini-1.5-flash", "error": None}
    except Exception as e:
        return {"success": False, "insights": "", "insight_type": insight_type,
                "model": None, "error": str(e)}


BOT_SYSTEM = """You are a helpful assistant for a Catholic parish network.
Help parishioners with: finding parishes, Mass times, liturgical calendar, Catholic teaching (informational), parish services.
Do not give pastoral counseling, doctrinal rulings. Refer complex spiritual questions to the parish priest.
Be warm, respectful, concise. Max 3 sentences unless asked for more."""


def bot_respond(user_message, conversation_history, language_code="en"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    history = ""
    for msg in conversation_history[-6:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history += f"{role}: {msg['content']}\n"
    prompt = (
        f"{BOT_SYSTEM}\nRespond in {lang}.\n\n"
        f"Conversation:\n{history}\nUser: {user_message}\n\nAssistant:"
    )
    try:
        resp = _flash().generate_content(prompt)
        return {"success": True, "reply": resp.text.strip(),
                "model": "gemini-1.5-flash", "error": None}
    except Exception as e:
        return {"success": False, "reply": "Sorry, couldn't process that. Please try again.",
                "model": None, "error": str(e)}
