"""
AI Service — Catholic Network Tools
Direct REST calls using Python stdlib urllib only. Zero extra dependencies.

Model cascade (all free-tier compatible):
  1. gemini-1.5-flash   via v1beta
  2. gemini-1.5-flash   via v1
  3. gemini-1.5-flash-8b via v1beta

All exceptions → user-friendly strings. No raw HTTP/JSON ever surfaces.
"""

import os, time, logging, json
import urllib.request, urllib.error

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "en": "English", "sw": "Kiswahili", "fr": "French",
    "es": "Spanish",  "pt": "Portuguese", "lg": "Luganda",
}

_MODELS = [
    ("gemini-1.5-flash",    "v1beta"),
    ("gemini-1.5-flash",    "v1"),
    ("gemini-1.5-flash-8b", "v1beta"),
]

class QuotaExceededError(Exception): pass
class AIUnavailableError(Exception): pass

_MSG = {
    "quota":            ("The AI assistant has reached its daily request limit and will be "
                         "available again later today. Your priest or parish coordinator can "
                         "help with any urgent questions in the meantime."),
    "unavailable":      "The AI assistant is not available right now. Please try again in a few minutes.",
    "no_key":           ("The AI assistant has not been set up for this parish yet. "
                         "Contact your parish coordinator to activate it."),
    "translation_fail": "Translation is not available right now. Please try again shortly.",
    "homily_fail":      "Notes could not be generated right now. Please try again shortly.",
    "insights_fail":    "Insights could not be generated right now. Please try again shortly.",
    "chat_fail":        "I couldn't respond right now. Please try again in a moment.",
}

_cache: dict = {}
_CACHE_TTL = 3600

def _cached(key, fn):
    now = time.time()
    if key in _cache and now - _cache[key]["ts"] < _CACHE_TTL:
        return _cache[key]["val"]
    val = fn()
    _cache[key] = {"val": val, "ts": now}
    return val

def _api_key() -> str:
    k = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not k:
        raise AIUnavailableError("no_key")
    return k.strip()

def _call_once(prompt: str, model: str, version: str, api_key: str) -> str:
    url = (f"https://generativelanguage.googleapis.com"
           f"/{version}/models/{model}:generateContent?key={api_key}")
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 1024, "temperature": 0.7}
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        code = e.code
        snippet = e.read()[:300].decode("utf-8", errors="ignore")
        logger.debug("HTTP %s on %s/%s: %s", code, version, model, snippet[:80])
        if code == 429:
            raise QuotaExceededError()
        raise AIUnavailableError(f"http_{code}")
    except urllib.error.URLError as e:
        raise AIUnavailableError(f"url_error: {e.reason}")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise AIUnavailableError(f"bad_response: {e}")

def _generate(prompt: str) -> str:
    key = _api_key()
    quota_hit = False
    last_err = None
    for model, version in _MODELS:
        try:
            return _call_once(prompt, model, version, key)
        except QuotaExceededError:
            quota_hit = True
            logger.info("Quota hit on %s/%s", version, model)
            time.sleep(0.5)
        except AIUnavailableError as e:
            last_err = e
            logger.debug("Failed %s/%s: %s", version, model, e)
    if quota_hit:
        raise QuotaExceededError()
    raise AIUnavailableError(str(last_err or "all_failed"))


# ═══ PUBLIC API ══════════════════════════════════════════════════════════════

def translate_text(text, target_language_code, source_language_code="en",
                   context="Catholic parish communication"):
    if target_language_code not in SUPPORTED_LANGUAGES:
        return {"success": False, "translated": text, "error": "unsupported"}
    target = SUPPORTED_LANGUAGES[target_language_code]
    source = SUPPORTED_LANGUAGES.get(source_language_code, "English")
    prompt = (f"Translate from {source} to {target}. Context: {context}.\n"
              "Preserve liturgical terminology and saint names exactly. "
              "Return ONLY the translated text.\n\nText:\n" + text)
    try:
        t = _cached(f"tr:{source_language_code}:{target_language_code}:{hash(text)}",
                    lambda: _generate(prompt))
        return {"success": True, "translated": t, "error": None}
    except QuotaExceededError:
        return {"success": False, "translated": text, "error": "quota", "message": _MSG["quota"]}
    except AIUnavailableError as e:
        msg = _MSG["no_key"] if "no_key" in str(e) else _MSG["translation_fail"]
        return {"success": False, "translated": text, "error": "unavailable", "message": msg}
    except Exception:
        return {"success": False, "translated": text, "error": "unavailable",
                "message": _MSG["translation_fail"]}

_HOMILY_DISCLAIMER = ("These notes are a preparation aid only — they do not replace personal "
                       "prayer, pastoral discernment, or the priest's own preparation.")

def homily_helper(gospel_reference, liturgical_season, parish_context="",
                  language_code="en", audience="general parish community"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    prompt = (
        "You are a Catholic homily preparation assistant for priests and deacons.\n"
        f"Reading/Gospel: {gospel_reference}\nSeason: {liturgical_season}\n"
        f"Parish context: {parish_context or 'General mixed-age parish'}\n"
        f"Audience: {audience}\nDelivery language: {lang}\n\n"
        "Provide:\n1. Core theological theme (2-3 sentences)\n"
        "2. Key pastoral message\n3. 2-3 life-application points\n"
        "4. Opening image or story angle\n5. Closing prayer prompt\n"
        "Use clear headers. Pastoral not academic."
    )
    try:
        c = _cached(f"hom:{gospel_reference}:{liturgical_season}:{language_code}",
                    lambda: _generate(prompt))
        return {"success": True, "content": c, "disclaimer": _HOMILY_DISCLAIMER, "error": None}
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
        "community_summary": ("Summarize this parish data for a coordinator. Highlight 2 strengths "
                              "and 2 areas needing attention. Suggest 3 next steps. Plain language. Max 250 words."),
        "action_brief":      ("List 'What Needs Attention This Week' — 5 items, one sentence each. Action-oriented."),
        "monthly_report":    ("Write a concise monthly parish report for a priest. Community health, "
                              "ministry activity, one suggested focus. Warm, professional. Max 300 words."),
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
    "Max 3 sentences unless asked for more."
)

def bot_respond(user_message, conversation_history, language_code="en"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    history = "".join(
        f"{'You' if m['role']=='user' else 'Assistant'}: {m['content']}\n"
        for m in (conversation_history or [])[-6:]
    )
    prompt = (f"{_BOT_SYSTEM}\nAlways respond in {lang}.\n\n"
              + (f"Previous messages:\n{history}\n" if history else "")
              + f"User: {user_message}\n\nAssistant:")
    try:
        reply = _generate(prompt)
        return {"success": True, "reply": reply, "error": None}
    except QuotaExceededError:
        return {"success": False, "error": "quota", "message": _MSG["quota"],
                "reply": _MSG["quota"]}
    except AIUnavailableError as e:
        msg = _MSG["no_key"] if "no_key" in str(e) else _MSG["chat_fail"]
        return {"success": False, "error": "unavailable", "message": msg, "reply": msg}
    except Exception:
        return {"success": False, "error": "unavailable",
                "message": _MSG["chat_fail"], "reply": _MSG["chat_fail"]}
