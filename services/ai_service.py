"""
AI Service — Catholic Network Tools
Direct REST to Gemini. Zero SDK dependencies.

Diagnostic mode: _diagnose() returns the exact failure reason and fix instructions.
Demo fallback: pre-written responses serve visitors when the key is restricted.
"""

import os
import time
import logging
try:
    from services import magisterial as _mag
except Exception:
    _mag = None
import json
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "en": "English",  "sw": "Kiswahili", "fr": "French",
    "es": "Spanish",  "pt": "Portuguese", "lg": "Luganda",
    "ig": "Igbo",     "tl": "Tagalog",    "hi": "Hindi",
    "it": "Italiano", "de": "Deutsch",    "pl": "Polski",
    "ar": "Arabic",   "sv": "Svenska",
}

_MODELS = [
    ("gemini-1.5-flash",    "v1beta"),
    ("gemini-1.5-flash",    "v1"),
    ("gemini-2.0-flash",    "v1beta"),
    ("gemini-1.5-flash-8b", "v1beta"),
]

class QuotaExceededError(Exception): pass
class AIUnavailableError(Exception): pass

_MSG = {
    "quota":       ("The AI assistant has reached its daily request limit and will be "
                    "available again later today."),
    "unavailable": "The AI assistant is not available right now. Please try again shortly.",
    "no_key":      ("The AI assistant has not been set up for this parish yet. "
                    "Contact your parish coordinator to activate it."),
    "restricted":  ("The AI assistant's access key needs one setting changed in "
                    "Google Cloud Console. Your parish coordinator can fix this in about 30 seconds."),
    "chat_fail":   "I couldn't respond right now. Please try again in a moment.",
}

_cache: dict = {}
_CACHE_TTL = 3600
_last_error_type: str = ""  # track for diagnostics

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
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        code = e.code
        body_bytes = e.read()
        body_text = body_bytes[:400].decode("utf-8", errors="ignore")
        logger.debug("HTTP %s on %s/%s: %s", code, version, model, body_text[:80])
        if code == 429:
            raise QuotaExceededError()
        if code == 403:
            # Distinguish API key restriction (HTML 403) from API permission error (JSON 403)
            if body_text.strip().startswith("<"):
                raise AIUnavailableError("ip_restricted")  # IP/referrer block
            raise AIUnavailableError(f"forbidden_{code}")
        if code in (400, 404):
            raise AIUnavailableError(f"http_{code}")
        raise AIUnavailableError(f"http_{code}")
    except urllib.error.URLError as e:
        raise AIUnavailableError(f"url_error: {e.reason}")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise AIUnavailableError(f"bad_response: {e}")

def _generate(prompt: str) -> str:
    global _last_error_type
    key = _api_key()
    quota_hit = False
    last_err = None
    for model, version in _MODELS:
        try:
            result = _call_once(prompt, model, version, key)
            _last_error_type = ""
            return result
        except QuotaExceededError:
            quota_hit = True
            _last_error_type = "quota"
            time.sleep(0.5)
        except AIUnavailableError as e:
            err_str = str(e)
            if "ip_restricted" in err_str:
                _last_error_type = "ip_restricted"
            last_err = e
            logger.debug("Failed %s/%s: %s", version, model, e)
    if quota_hit:
        raise QuotaExceededError()
    raise AIUnavailableError(str(last_err or "all_failed"))


# ── Diagnostic ────────────────────────────────────────────────────────────────

def diagnose() -> dict:
    """
    Test the API key and return a diagnosis with plain-English fix instructions.
    Returns: {status, title, detail, fix_steps}
    """
    key = None
    try:
        key = _api_key()
    except AIUnavailableError:
        return {
            "status": "no_key",
            "title": "API key not configured",
            "detail": "AI assistant is not yet configured for this parish.",
            "fix_steps": [
                "Contact your parish tech coordinator or email contact@aikungfu.dev to enable the AI assistant",
                "Add: GOOGLE_API_KEY = \"your-key-here\"",
                "Save — the app restarts in ~1 minute",
                "Get a free key at aistudio.google.com → Get API key",
            ]
        }

    # Try a minimal call
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    body = json.dumps({"contents":[{"parts":[{"text":"hi"}]}]}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            text = data["candidates"][0]["content"]["parts"][0]["text"][:20]
            return {
                "status": "ok",
                "title": "AI assistant is working",
                "detail": f"Connection successful. Model responded: '{text}'",
                "fix_steps": []
            }
    except urllib.error.HTTPError as e:
        code = e.code
        body_text = e.read()[:400].decode("utf-8","ignore")
        if code == 403 and body_text.strip().startswith("<"):
            return {
                "status": "ip_restricted",
                "title": "API key has IP restrictions",
                "detail": (
                    "The key is valid but Google Cloud Console is blocking requests "
                    "from external servers (including Streamlit Cloud). "
                    "This is a single setting change."
                ),
                "fix_steps": [
                    "Go to console.cloud.google.com",
                    "Navigate to: APIs & Services → Credentials",
                    "Click on 'CatholicApp Gemini API Key'",
                    "Under 'Application restrictions' → select 'None'",
                    "Click Save — works immediately, no redeploy needed",
                    "Alternatively: create a new unrestricted key at aistudio.google.com → Get API key → Create API key in existing project",
                ]
            }
        if code == 429:
            return {
                "status": "quota",
                "title": "Daily quota reached",
                "detail": "The key has hit its free-tier daily limit (1,500 requests). Resets at midnight Pacific Time.",
                "fix_steps": [
                    "Wait until midnight Pacific Time for the daily quota to reset",
                    "Or enable billing at console.cloud.google.com → Billing to remove the daily cap",
                ]
            }
        if code == 400:
            return {
                "status": "invalid_key",
                "title": "API key is invalid",
                "detail": "Google returned 400 — the key may be incorrect or revoked.",
                "fix_steps": [
                    "Check the key value in Streamlit secrets matches aistudio.google.com",
                    "Create a new key if needed at aistudio.google.com → Get API key",
                ]
            }
        return {
            "status": "error",
            "title": f"Connection error (HTTP {code})",
            "detail": body_text[:200],
            "fix_steps": ["Contact your parish coordinator with this error code."]
        }
    except Exception as e:
        return {
            "status": "error",
            "title": "Connection failed",
            "detail": str(e)[:200],
            "fix_steps": ["Check your internet connection and try again."]
        }


# ── Demo fallback responses ───────────────────────────────────────────────────

_DEMO = {
    "what are you": (
        "I'm the Jumuia — Parish Community AI assistant — here to help with Mass times, "
        "sacraments, the liturgical calendar, and translating parish announcements into "
        "Kiswahili, Luganda, French, and more. For pastoral counseling, please speak with your priest."
    ),
    "mass": (
        "Mass times vary by parish. Use the Parish Directory to find your local church and its schedule. "
        "Most parishes in East Africa have Sunday Masses at 7am, 9am, and 11am."
    ),
    "rosary": (
        "The Rosary is prayed on five mysteries depending on the day: Joyful (Mon/Sat), "
        "Luminous (Thu), Sorrowful (Tue/Fri), Glorious (Wed/Sun). "
        "Visit the Daily Prayers page for the full guided Rosary."
    ),
    "sacrament": (
        "The seven sacraments are Baptism, Confirmation, Eucharist, Reconciliation, "
        "Anointing of the Sick, Holy Orders, and Matrimony. "
        "Your parish coordinator can help you prepare for any sacrament."
    ),
    "hello|hi|jambo|habari": (
        "Hello! I'm the Jumuia — Parish Community assistant. "
        "I can help you find a church, answer questions about the liturgical calendar, "
        "or translate parish announcements. How can I help you today?"
    ),
}

def _demo_reply(message: str) -> str:
    msg_lower = message.lower()
    for keywords, reply in _DEMO.items():
        if any(k in msg_lower for k in keywords.split("|")):
            return reply
    return (
        "The AI assistant is currently being set up. In the meantime: "
        "use the Parish Directory to find churches, Daily Prayers for the Rosary and readings, "
        "and the sidebar to explore all parish tools."
    )


# ═══ PUBLIC API ═══════════════════════════════════════════════════════════════

def translate_text(text, target_language_code, source_language_code="en",
                   context="Catholic parish communication"):
    if target_language_code not in SUPPORTED_LANGUAGES:
        return {
    "success": False,
    "error": "Unsupported language",
    "code": "unsupported_language",
}
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
        err = str(e)
        if "no_key" in err: msg = _MSG["no_key"]
        elif "ip_restricted" in err: msg = _MSG["restricted"]
        else: msg = _MSG["unavailable"]
        return {"success": False, "translated": text, "error": "unavailable", "message": msg}
    except Exception:
        return {"success": False, "translated": text, "error": "unavailable", "message": _MSG["unavailable"]}

_HOMILY_DISCLAIMER = ("These notes are a preparation aid only — they do not replace personal "
                       "prayer, pastoral discernment, or the priest's own preparation.")

def homily_helper(gospel_reference, liturgical_season, parish_context="",
                  language_code="en", audience="general parish community"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")
    prompt = (
        "You are a Catholic homily preparation assistant.\n"
        f"Reading/Gospel: {gospel_reference}\nSeason: {liturgical_season}\n"
        f"Parish context: {parish_context or 'General mixed-age parish'}\n"
        f"Audience: {audience}\nLanguage: {lang}\n\n"
        "Provide:\n1. Core theological theme\n2. Key pastoral message\n"
        "3. 2-3 life-application points\n4. Opening image\n5. Closing prayer prompt\n"
        "Clear headers. Pastoral not academic."
    )
    try:
        c = _cached(f"hom:{gospel_reference}:{liturgical_season}:{language_code}",
                    lambda: _generate(prompt))
        return {"success": True, "content": c, "disclaimer": _HOMILY_DISCLAIMER, "error": None}
    except QuotaExceededError:
        return {"success": False, "content": "", "disclaimer": _HOMILY_DISCLAIMER,
                "error": "quota", "message": _MSG["quota"]}
    except AIUnavailableError as e:
        err = str(e)
        msg = _MSG["no_key"] if "no_key" in err else (_MSG["restricted"] if "ip_restricted" in err else _MSG["unavailable"])
        return {"success": False, "content": "", "disclaimer": _HOMILY_DISCLAIMER,
                "error": "unavailable", "message": msg}
    except Exception:
        return {"success": False, "content": "", "disclaimer": _HOMILY_DISCLAIMER,
                "error": "unavailable", "message": _MSG["unavailable"]}

def generate_parish_insights(parish_data, insight_type="community_summary"):
    PROMPTS = {
        "community_summary": "Summarize this parish data. Highlight 2 strengths, 2 areas needing attention. Suggest 3 next steps. Plain language. Max 250 words.",
        "action_brief": "List 'What Needs Attention This Week' — 5 items, one sentence each.",
        "monthly_report": "Write a concise monthly parish report for the priest. Community health, ministry activity, one focus area. Max 300 words.",
    }
    prompt = f"{PROMPTS.get(insight_type, PROMPTS['community_summary'])}\n\nData:\n{parish_data}"
    try:
        return {"success": True, "insights": _generate(prompt), "error": None}
    except QuotaExceededError:
        return {"success": False, "insights": "", "error": "quota", "message": _MSG["quota"]}
    except AIUnavailableError as e:
        err = str(e)
        msg = _MSG["no_key"] if "no_key" in err else (_MSG["restricted"] if "ip_restricted" in err else _MSG["unavailable"])
        return {"success": False, "insights": "", "error": "unavailable", "message": msg}
    except Exception:
        return {"success": False, "insights": "", "error": "unavailable", "message": _MSG["unavailable"]}

def bot_respond(user_message, conversation_history, language_code="en"):
    lang = SUPPORTED_LANGUAGES.get(language_code, "English")

    # §3 Magisterial Boundary Layer — classify before sending to model
    try:
        from services import magisterial as _mag
        classification = _mag.classify_query(user_message)
        if classification["sensitive"]:
            _mag.log_sensitive(user_message[:30] + "...", classification)
        system = _mag.build_system_prompt(lang)
    except Exception:
        system = (
            "You are a helpful, warm assistant for a Catholic parish. "
            "Help with: Mass times, sacraments, liturgical calendar, Catholic traditions. "
            "Do NOT provide pastoral counseling — refer those to the parish priest. "
            f"Always respond in {lang}."
        )

    history = "".join(
        f"{'You' if m['role']=='user' else 'Assistant'}: {m['content']}\n"
        for m in (conversation_history or [])[-6:]
    )
    prompt = (f"{system}\n\n"
              + (f"Previous:\n{history}\n" if history else "")
              + f"User: {user_message}\n\nAssistant:")
    try:
        reply = _generate(prompt)
        return {"success": True, "reply": reply, "error": None}
    except QuotaExceededError:
        return {"success": False, "error": "quota", "message": _MSG["quota"], "reply": _MSG["quota"]}
    except AIUnavailableError as e:
        err = str(e)
        if "ip_restricted" in err:
            demo = _demo_reply(user_message)
            return {"success": False, "error": "ip_restricted",
                    "message": _MSG["restricted"], "reply": demo, "use_demo": True}
        msg = _MSG["no_key"] if "no_key" in err else _MSG["chat_fail"]
        return {"success": False, "error": "unavailable", "message": msg,
                "reply": _demo_reply(user_message), "use_demo": True}
    except Exception:
        return {"success": False, "error": "unavailable",
                "message": _MSG["chat_fail"],
                "reply": _demo_reply(user_message), "use_demo": True}
