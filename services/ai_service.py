"""
AI Service — Catholic Network Tools
Powered by Gemini via google-genai SDK.

Free tier limits (per key per day):
  gemini-2.0-flash     → 1,500 req/day, 15 RPM
  gemini-1.5-flash-8b  → separate quota pool (fallback)

On quota exhaustion: returns user-friendly message, never raw JSON errors.
Responses cached 1hr to conserve quota.
"""

import os, time, logging, functools
logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "en": "English",
    "sw": "Kiswahili",
    "fr": "French",
    "es": "Spanish",
    "pt": "Portuguese",
    "lg": "Luganda",
}

# Model cascade — try primary first, fall back on 429
PRIMARY_MODEL   = "gemini-2.0-flash"
FALLBACK_MODEL  = "gemini-1.5-flash-8b"  # separate free-tier quota pool

_genai_available = False
try:
    from google import genai as _genai
    _genai_available = True
except ImportError:
    logger.warning("google-genai not installed. AI features offline.")


def _api_key():
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise EnvironmentError(
            "GEMINI_API_KEY not set. Add it to Streamlit secrets → Settings → Secrets."
        )
    return key


def _generate(prompt: str, model: str = PRIMARY_MODEL, retry: bool = True) -> str:
    """Generate with automatic fallback on 429 (quota exhausted)."""
    if not _genai_available:
        raise EnvironmentError("google-genai package not installed.")

    client = _genai.Client(api_key=_api_key())
    try:
        r = client.models.generate_content(model=model, contents=prompt)
        return r.text.strip()
    except Exception as e:
        err_str = str(e)
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
            if model != FALLBACK_MODEL and retry:
                # Try the fallback model (different quota pool)
                logger.info("Primary model quota hit — trying fallback model.")
                time.sleep(2)
                return _generate(prompt, model=FALLBACK_MODEL, retry=False)
            raise QuotaExceededError()
        raise


class QuotaExceededError(Exception):
    """Raised when all models have hit their free-tier quota."""
    pass


def _quota_response():
    return {
        "success": False,
        "model": None,
        "error": "quota_exceeded",
        "message": (
            "The AI assistant has reached its daily limit for free requests. "
            "It resets automatically at midnight (Pacific Time). "
            "For uninterrupted access, your parish can enable a paid Gemini plan at aistudio.google.com."
        ),
    }


# ─── Simple in-memory cache (reduces repeated identical queries) ──────────────

_cache: dict = {}
CACHE_TTL = 3600  # 1 hour

def _cached(key: str, fn):
    now = time.time()
    if key in _cache and now - _cache[key]["ts"] < CACHE_TTL:
        return _cache[key]["val"]
    result = fn()
    _cache[key] = {"val": result, "ts": now}
    return result


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
        "Preserve liturgical terminology and saint names exactly. "
        "Return ONLY the translated text, no preamble.\n\nText:\n{text}"
    ).format(text=text)

    cache_key = f"translate:{source_language_code}:{target_language_code}:{hash(text)}"
    try:
        translated = _cached(cache_key, lambda: _generate(prompt))
        return {"success": True, "translated": translated, "model": PRIMARY_MODEL, "error": None}
    except QuotaExceededError:
        r = _quota_response()
        r["translated"] = text
        return r
    except Exception as e:
        logger.error("Translation error: %s", e)
        return {"success": False, "translated": text, "model": None,
                "error": "Translation unavailable. Please try again shortly."}


# ─── 2. HOMILY HELPER ─────────────────────────────────────────────────────────

_HOMILY_SYSTEM = (
    "You are a Catholic homily preparation assistant for priests and deacons. "
    "Deep knowledge of Scripture, Catechism of the Catholic Church, and the liturgical calendar. "
    "This is a PREPARATION AID only — never a finished homily. "
    "Ground content in Scripture and authentic Catholic teaching. Be pastorally sensitive."
)

def homily_helper(gospel_reference, liturgical_season, parish_context="",
                  language_code="en", audience="general parish community"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    prompt = (
        f"{_HOMILY_SYSTEM}\n\nPrepare homily notes for:\n"
        f"• Reading/Gospel: {gospel_reference}\n"
        f"• Liturgical season: {liturgical_season}\n"
        f"• Parish context: {parish_context or 'General mixed-age parish'}\n"
        f"• Audience: {audience}\n• Delivery language: {lang}\n\n"
        "Provide structured notes:\n"
        "1. Core theological theme (2–3 sentences)\n"
        "2. Key pastoral message for this congregation\n"
        "3. 2–3 concrete life-application points\n"
        "4. Opening image or story angle\n"
        "5. Closing prayer prompt\n\n"
        "Use clear headers. Concise. Pastoral, not academic."
    )
    disclaimer = (
        "⚠️ Preparation aid only — does not replace prayer, "
        "personal discernment, or the priest's own pastoral judgment."
    )
    cache_key = f"homily:{gospel_reference}:{liturgical_season}:{language_code}"
    try:
        content = _cached(cache_key, lambda: _generate(prompt))
        return {"success": True, "content": content, "disclaimer": disclaimer,
                "model": PRIMARY_MODEL, "error": None}
    except QuotaExceededError:
        r = _quota_response()
        r.update({"content": "", "disclaimer": disclaimer})
        return r
    except Exception as e:
        return {"success": False, "content": "", "disclaimer": disclaimer,
                "model": None, "error": str(e)}


# ─── 3. PARISH INSIGHTS ───────────────────────────────────────────────────────

def generate_parish_insights(parish_data, insight_type="community_summary"):
    PROMPTS = {
        "community_summary": (
            "Summarize this parish data for a coordinator. "
            "Highlight 2 strengths and 2 areas needing attention. "
            "Suggest 3 concrete next steps. Plain language. Max 250 words."
        ),
        "action_brief": (
            "List 'What Needs Attention This Week' — exactly 5 items, "
            "one sentence each. Plain language, action-oriented."
        ),
        "monthly_report": (
            "Write a concise monthly parish report for a priest. "
            "Cover community health, ministry activity, and one suggested focus area. "
            "Warm, professional tone. Max 300 words."
        ),
    }
    prompt = f"{PROMPTS.get(insight_type, PROMPTS['community_summary'])}\n\nParish data:\n{parish_data}"
    try:
        insights = _generate(prompt)
        return {"success": True, "insights": insights, "model": PRIMARY_MODEL, "error": None}
    except QuotaExceededError:
        r = _quota_response()
        r["insights"] = ""
        return r
    except Exception as e:
        return {"success": False, "insights": "", "model": None, "error": str(e)}


# ─── 4. CHAT BOT ─────────────────────────────────────────────────────────────

_BOT_SYSTEM = (
    "You are a helpful assistant for a Catholic parish. "
    "Help with: finding parishes, Mass times, liturgical calendar, Catholic teaching (informational only), "
    "parish services, sacraments, and Catholic traditions. "
    "Do NOT give pastoral counseling or doctrinal rulings. "
    "Refer personal spiritual questions to the parish priest. "
    "Be warm, respectful, and concise. Respond in max 3 sentences unless asked for more."
)

def bot_respond(user_message, conversation_history, language_code="en"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    history = ""
    for msg in (conversation_history or [])[-6:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history += f"{role}: {msg['content']}\n"

    prompt = (
        f"{_BOT_SYSTEM}\nAlways respond in {lang}.\n\n"
        f"{'Conversation so far:' + chr(10) + history if history else ''}"
        f"User: {user_message}\n\nAssistant:"
    )
    try:
        reply = _generate(prompt)
        return {"success": True, "reply": reply, "model": PRIMARY_MODEL, "error": None}
    except QuotaExceededError:
        r = _quota_response()
        r["reply"] = (
            "The AI assistant has reached its daily limit. "
            "It resets at midnight Pacific Time. "
            "Your priest or parish coordinator can help with your question in the meantime."
        )
        return r
    except Exception as e:
        return {"success": False,
                "reply": "Sorry, I couldn't process that right now. Please try again.",
                "model": None, "error": str(e)}
