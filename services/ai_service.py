"""
AI Service — Catholic Network Tools
Powered by Gemini via direct REST API (no SDK dependency issues).

Avoids SDK version/platform conflicts by calling the Gemini REST endpoint directly.
Free tier: ~1,500 req/day on gemini-2.0-flash. Falls back to gemini-1.5-flash-8b.
All errors return user-friendly messages — no raw HTTP/JSON ever surfaces.
"""

import os, time, logging, requests as _requests
logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "en": "English",
    "sw": "Kiswahili",
    "fr": "French",
    "es": "Spanish",
    "pt": "Portuguese",
    "lg": "Luganda",
}

PRIMARY_MODEL  = "gemini-2.0-flash"
FALLBACK_MODEL = "gemini-1.5-flash-8b"

_GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

# ── Simple in-memory cache (1hr TTL) ─────────────────────────────────────────
_cache: dict = {}
_CACHE_TTL = 3600

def _cached(key: str, fn):
    now = time.time()
    if key in _cache and now - _cache[key]["ts"] < _CACHE_TTL:
        return _cache[key]["val"]
    result = fn()
    _cache[key] = {"val": result, "ts": now}
    return result

# ── Error categories ──────────────────────────────────────────────────────────
class QuotaExceededError(Exception): pass
class AIUnavailableError(Exception): pass

# ── Friendly public messages (no tech jargon) ─────────────────────────────────
_MSG = {
    "quota": (
        "The AI assistant has reached its daily request limit and will be "
        "available again later today. Your priest or parish coordinator can "
        "help with any urgent questions in the meantime."
    ),
    "unavailable": (
        "The AI assistant is not available right now. "
        "Please try again in a few minutes."
    ),
    "no_key": (
        "The AI assistant has not been set up for this parish yet. "
        "Contact your parish coordinator to activate it."
    ),
    "translation_fail": "Translation is not available right now. Please try again shortly.",
    "homily_fail":      "Notes could not be generated right now. Please try again shortly.",
    "insights_fail":    "Insights could not be generated right now. Please try again shortly.",
    "chat_fail":        "I couldn't respond right now. Please try again in a moment.",
}

def _api_key() -> str:
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise AIUnavailableError("no_key")
    return key

def _call(prompt: str, model: str, api_key: str) -> str:
    """Single REST call to Gemini generateContent endpoint."""
    url = f"{_GEMINI_BASE}/{model}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        resp = _requests.post(url, json=payload, timeout=30)
    except _requests.Timeout:
        raise AIUnavailableError("timeout")
    except _requests.ConnectionError:
        raise AIUnavailableError("connection")

    if resp.status_code == 429:
        raise QuotaExceededError()
    if resp.status_code == 400:
        raise AIUnavailableError("bad_request")
    if resp.status_code == 403:
        raise AIUnavailableError("forbidden")
    if not resp.ok:
        raise AIUnavailableError(f"http_{resp.status_code}")

    data = resp.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        raise AIUnavailableError("bad_response")

def _generate(prompt: str, model: str = PRIMARY_MODEL) -> str:
    """Generate with automatic fallback on quota exhaustion."""
    key = _api_key()
    try:
        return _call(prompt, model, key)
    except QuotaExceededError:
        if model == PRIMARY_MODEL:
            logger.info("Primary model quota hit — trying fallback.")
            time.sleep(1)
            try:
                return _call(prompt, FALLBACK_MODEL, key)
            except QuotaExceededError:
                raise
            except AIUnavailableError:
                raise
        raise


# ═══ PUBLIC API ═══════════════════════════════════════════════════════════════

def translate_text(text, target_language_code, source_language_code="en",
                   context="Catholic parish communication"):
    if target_language_code not in SUPPORTED_LANGUAGES:
        return {"success": False, "translated": text, "error": "unsupported_language"}
    target = SUPPORTED_LANGUAGES[target_language_code]
    source = SUPPORTED_LANGUAGES.get(source_language_code, "English")
    prompt = (
        f"Translate from {source} to {target}. Context: {context}.\n"
        "Preserve liturgical terminology and saint names exactly. "
        "Return ONLY the translated text, no preamble.\n\nText:\n" + text
    )
    cache_key = f"tr:{source_language_code}:{target_language_code}:{hash(text)}"
    try:
        translated = _cached(cache_key, lambda: _generate(prompt))
        return {"success": True, "translated": translated, "error": None}
    except QuotaExceededError:
        return {"success": False, "translated": text,
                "error": "quota", "message": _MSG["quota"]}
    except AIUnavailableError as e:
        if "no_key" in str(e):
            return {"success": False, "translated": text,
                    "error": "no_key", "message": _MSG["no_key"]}
        return {"success": False, "translated": text,
                "error": "unavailable", "message": _MSG["translation_fail"]}
    except Exception:
        return {"success": False, "translated": text,
                "error": "unavailable", "message": _MSG["translation_fail"]}


_HOMILY_DISCLAIMER = (
    "These are preparation notes only — they do not replace personal prayer, "
    "pastoral discernment, or the priest's own preparation."
)

def homily_helper(gospel_reference, liturgical_season, parish_context="",
                  language_code="en", audience="general parish community"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    prompt = (
        "You are a Catholic homily preparation assistant for priests and deacons.\n"
        f"Reading/Gospel: {gospel_reference}\nSeason: {liturgical_season}\n"
        f"Parish context: {parish_context or 'General mixed-age parish'}\n"
        f"Audience: {audience}\nDelivery language: {lang}\n\n"
        "Provide:\n1. Core theological theme (2–3 sentences)\n"
        "2. Key pastoral message\n3. 2–3 life-application points\n"
        "4. Opening image or story angle\n5. Closing prayer prompt\n"
        "Use clear headers. Be pastoral, not academic."
    )
    cache_key = f"hom:{gospel_reference}:{liturgical_season}:{language_code}"
    try:
        content = _cached(cache_key, lambda: _generate(prompt))
        return {"success": True, "content": content,
                "disclaimer": _HOMILY_DISCLAIMER, "error": None}
    except QuotaExceededError:
        return {"success": False, "content": "", "disclaimer": _HOMILY_DISCLAIMER,
                "error": "quota", "message": _MSG["quota"]}
    except AIUnavailableError as e:
        msg = _MSG["no_key"] if "no_key" in str(e) else _MSG["homily_fail"]
        return {"success": False, "content": "", "disclaimer": _HOMILY_DISCLAIMER,
                "error": "unavailable", "message": msg}
    except Exception:
        return {"success": False, "content": "", "disclaimer": _HOMILY_DISCLAIMER,
                "error": "unavailable", "message": _MSG["homily_fail"]}


def generate_parish_insights(parish_data, insight_type="community_summary"):
    PROMPTS = {
        "community_summary": (
            "Summarize this parish data for a coordinator. Highlight 2 strengths "
            "and 2 areas needing attention. Suggest 3 concrete next steps. "
            "Plain language, no jargon. Max 250 words."
        ),
        "action_brief": (
            "List 'What Needs Attention This Week' — exactly 5 items, "
            "one sentence each. Plain language, action-oriented."
        ),
        "monthly_report": (
            "Write a concise monthly parish report for a priest. Cover community health, "
            "ministry activity, and one suggested focus area. Warm, professional. Max 300 words."
        ),
    }
    prompt = f"{PROMPTS.get(insight_type, PROMPTS['community_summary'])}\n\nParish data:\n{parish_data}"
    try:
        return {"success": True, "insights": _generate(prompt), "error": None}
    except QuotaExceededError:
        return {"success": False, "insights": "", "error": "quota", "message": _MSG["quota"]}
    except AIUnavailableError as e:
        msg = _MSG["no_key"] if "no_key" in str(e) else _MSG["insights_fail"]
        return {"success": False, "insights": "", "error": "unavailable", "message": msg}
    except Exception:
        return {"success": False, "insights": "", "error": "unavailable",
                "message": _MSG["insights_fail"]}


_BOT_SYSTEM = (
    "You are a helpful, warm assistant for a Catholic parish. "
    "Help with: Mass times, sacraments, liturgical calendar, Catholic traditions, parish services. "
    "Do NOT provide pastoral counseling or doctrinal rulings — refer those to the parish priest. "
    "Be concise: max 3 sentences unless the user asks for more detail."
)

def bot_respond(user_message, conversation_history, language_code="en"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    history = ""
    for msg in (conversation_history or [])[-6:]:
        role = "You" if msg["role"] == "user" else "Assistant"
        history += f"{role}: {msg['content']}\n"
    prompt = (
        f"{_BOT_SYSTEM}\nAlways respond in {lang}.\n\n"
        + (f"Previous messages:\n{history}\n" if history else "")
        + f"User: {user_message}\n\nAssistant:"
    )
    try:
        return {"success": True, "reply": _generate(prompt), "error": None}
    except QuotaExceededError:
        return {"success": False, "error": "quota", "message": _MSG["quota"],
                "reply": _MSG["quota"]}
    except AIUnavailableError as e:
        msg = _MSG["no_key"] if "no_key" in str(e) else _MSG["chat_fail"]
        return {"success": False, "error": "unavailable", "message": msg, "reply": msg}
    except Exception:
        return {"success": False, "error": "unavailable",
                "message": _MSG["chat_fail"], "reply": _MSG["chat_fail"]}
