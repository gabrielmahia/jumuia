"""
AI Service — Catholic Network Tools
Claude-powered: translation, homily preparation, parish insights.

Model governance (cost-tiered):
  Haiku  → translation, summary, directory search queries
  Sonnet → homily helper, theological reflection, insights
  Opus   → NOT used here
"""

import os
import logging

import anthropic

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "en": "English",
    "sw": "Kiswahili",
    "fr": "French",
    "es": "Spanish",
    "pt": "Portuguese",
    "lg": "Luganda",
}


def _client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not set. Add to .env or Streamlit secrets."
        )
    return anthropic.Anthropic(api_key=api_key)


# ─────────────────────────────────────────────
# 1. TRANSLATION
# ─────────────────────────────────────────────

def translate_text(
    text: str,
    target_language_code: str,
    source_language_code: str = "en",
    context: str = "Catholic parish communication",
) -> dict:
    """
    Translate liturgical/parish text via Claude Haiku (cost-efficient).

    Returns:
        {"success": bool, "translated": str, "model": str, "error": str|None}
    """
    if target_language_code not in SUPPORTED_LANGUAGES:
        return {"success": False, "translated": text, "model": None,
                "error": f"Unsupported language: {target_language_code}"}

    target = SUPPORTED_LANGUAGES[target_language_code]
    source = SUPPORTED_LANGUAGES.get(source_language_code, "English")

    prompt = (
        f"Translate the following text from {source} to {target}.\n"
        f"Context: {context}\n"
        "Preserve liturgical terminology, saint names, diocese names, and respectful tone.\n"
        "Return ONLY the translated text — no preamble, no explanation.\n\n"
        f"Text:\n{text}"
    )

    try:
        response = _client().messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return {
            "success": True,
            "translated": response.content[0].text.strip(),
            "model": "claude-haiku-4-5-20251001",
            "error": None,
        }
    except Exception as e:
        logger.error("Translation error: %s", e)
        return {"success": False, "translated": text, "model": None, "error": str(e)}


# ─────────────────────────────────────────────
# 2. HOMILY HELPER
# ─────────────────────────────────────────────

HOMILY_SYSTEM = """You are a Catholic homily preparation assistant for priests and deacons.
You have deep knowledge of Scripture, the Catechism, and the liturgical calendar.

CONSTRAINTS:
- This is a preparation aid only — never a finished homily.
- Ground all content in Scripture and authentic Catholic teaching.
- Be pastorally sensitive. Avoid political commentary.
- Suggest, do not prescribe. Leave space for personal discernment."""

def homily_helper(
    gospel_reference: str,
    liturgical_season: str,
    parish_context: str = "",
    language_code: str = "en",
    audience: str = "general parish community",
) -> dict:
    """
    Generate homily preparation notes (Sonnet — theological depth required).

    Returns:
        {"success": bool, "content": str, "disclaimer": str, "model": str, "error": str|None}
    """
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    context_note = parish_context or "General mixed-age parish"

    prompt = (
        f"Prepare homily notes:\n\n"
        f"Reading/Gospel: {gospel_reference}\n"
        f"Liturgical Season: {liturgical_season}\n"
        f"Parish context: {context_note}\n"
        f"Audience: {audience}\n"
        f"Delivery language: {lang}\n\n"
        "Provide:\n"
        "1. Core theological theme (2–3 sentences)\n"
        "2. Key pastoral message for this congregation\n"
        "3. 2–3 concrete life-application points\n"
        "4. A suggested opening image or story angle (not a script)\n"
        "5. A closing personal prayer prompt\n\n"
        "Use clear headers. Keep each section concise."
    )

    disclaimer = (
        "⚠️ PREPARATION AID ONLY — This content is an assistive tool for homily "
        "preparation. It does not replace prayer, personal discernment, or the "
        "priest's own pastoral judgment."
    )

    try:
        response = _client().messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            system=HOMILY_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        return {
            "success": True,
            "content": response.content[0].text.strip(),
            "disclaimer": disclaimer,
            "model": "claude-sonnet-4-5-20250929",
            "error": None,
        }
    except Exception as e:
        logger.error("Homily helper error: %s", e)
        return {"success": False, "content": "", "disclaimer": disclaimer,
                "model": None, "error": str(e)}


# ─────────────────────────────────────────────
# 3. PARISH INSIGHTS
# ─────────────────────────────────────────────

def generate_parish_insights(
    parish_data: dict,
    insight_type: str = "community_summary",
) -> dict:
    """
    Generate plain-language insights from parish activity data (Haiku — mapping/summarization).

    insight_type options:
        "community_summary" — overview for coordinator dashboard
        "action_brief"      — what needs attention this week
        "monthly_report"    — digest for parish priest

    Returns:
        {"success": bool, "insights": str, "insight_type": str, "model": str, "error": str|None}
    """
    INSIGHT_PROMPTS = {
        "community_summary": (
            "Summarize this parish data in plain language for a parish coordinator. "
            "Highlight strengths, areas needing attention, and 2–3 specific next steps. "
            "Maximum 250 words. No jargon."
        ),
        "action_brief": (
            "Review this parish data and produce a brief 'What Needs Attention This Week' "
            "list. Maximum 5 items, each with one sentence of context. Plain language."
        ),
        "monthly_report": (
            "Write a concise monthly parish report from this data suitable for a priest. "
            "Include: community health indicators, ministry activity, suggested focus areas. "
            "Tone: warm, professional. Maximum 300 words."
        ),
    }

    instruction = INSIGHT_PROMPTS.get(
        insight_type,
        INSIGHT_PROMPTS["community_summary"]
    )

    prompt = f"{instruction}\n\nParish data:\n{parish_data}"

    try:
        response = _client().messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )
        return {
            "success": True,
            "insights": response.content[0].text.strip(),
            "insight_type": insight_type,
            "model": "claude-haiku-4-5-20251001",
            "error": None,
        }
    except Exception as e:
        logger.error("Insights error: %s", e)
        return {"success": False, "insights": "", "insight_type": insight_type,
                "model": None, "error": str(e)}


# ─────────────────────────────────────────────
# 4. CONVERSATIONAL BOT HANDLER
# ─────────────────────────────────────────────

BOT_SYSTEM = """You are a helpful assistant for a Catholic parish network.
You help parishioners with:
- Finding nearby parishes and Mass times
- Understanding the liturgical calendar
- Catholic teaching and sacraments (informational only)
- Parish services: giving, events, ministries

CONSTRAINTS:
- You do not give pastoral counseling or spiritual direction.
- You do not make doctrinal rulings.
- You refer complex spiritual questions to the parish priest.
- Be warm, respectful, and concise. Max 3 sentences per response unless asked for more."""

def bot_respond(
    user_message: str,
    conversation_history: list,
    language_code: str = "en",
) -> dict:
    """
    Single-turn bot response with conversation context.
    Used by both the Streamlit chat UI and the WhatsApp webhook handler.

    conversation_history: list of {"role": "user"|"assistant", "content": str}

    Returns:
        {"success": bool, "reply": str, "model": str, "error": str|None}
    """
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    system = BOT_SYSTEM + f"\n\nRespond in {lang}."

    messages = conversation_history + [{"role": "user", "content": user_message}]

    try:
        response = _client().messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=system,
            messages=messages,
        )
        return {
            "success": True,
            "reply": response.content[0].text.strip(),
            "model": "claude-haiku-4-5-20251001",
            "error": None,
        }
    except Exception as e:
        logger.error("Bot response error: %s", e)
        return {
            "success": False,
            "reply": "Sorry, I couldn't process that. Please try again.",
            "model": None,
            "error": str(e),
        }
