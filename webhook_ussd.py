"""
Catholic Parish Steward — USSD Webhook
=======================================
Minimal FastAPI app for Cloud Run deployment.
Handles ONLY the USSD endpoint from Africa's Talking.

Why separate from webhook_app.py:
  - No WhatsApp/M-Pesa dependencies needed for USSD
  - Faster cold start (fewer imports)
  - Clear single responsibility

Deploy to Cloud Run:
  gcloud run deploy cnt-ussd \
    --source . \
    --region africa-south1 \
    --allow-unauthenticated \
    --set-env-vars AFRICASTALKING_API_KEY=xxx,AFRICASTALKING_USERNAME=xxx

Africa's Talking callback URL:
  https://YOUR-SERVICE-URL/ussd
"""
import os
import json
import logging
import hmac as _hmac
from fastapi import HTTPException
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s"
)
logger = logging.getLogger("ussd")

app = FastAPI(
    title="Catholic Parish Steward — USSD",
    version="1.0.0",
    docs_url=None,   # disable Swagger in production
    redoc_url=None,
)


# ── Health check (Cloud Run uses this) ───────────────────────────────────────
@app.get("/")
@app.get("/health")
async def health():
    return {"status": "ok", "service": "cnt-ussd"}


# ── USSD webhook ──────────────────────────────────────────────────────────────
@app.post("/ussd")
async def ussd(request: Request):
    """
    Africa's Talking calls this on every keypress.
    Returns plain text starting with CON (continue) or END (terminate).
    Must respond within 5 seconds or AT kills the session.
    """
    try:
        form = dict(await request.form())
        session_id   = form.get("sessionId", "")
        service_code = form.get("serviceCode", "")
        phone        = form.get("phoneNumber", "")
        text         = form.get("text", "")

        logger.info("USSD | phone=%s | text='%s'", phone, text)

        from services.ussd_service import handle_ussd_session, log_ussd_session
        response = handle_ussd_session(session_id, service_code, phone, text)
        log_ussd_session(session_id, phone, text, response)

        logger.info("USSD | response='%s'", response[:60])
        return PlainTextResponse(content=response)

    except Exception as e:
        logger.error("USSD error: %s", e, exc_info=True)
        return PlainTextResponse(
            content="END Service unavailable. Please try again. / Huduma haipo. Tafadhali jaribu tena."
        )


# ── WhatsApp — Meta Cloud API ──────────────────────────────────────────────────

import hashlib


WA_TOKEN        = os.getenv("WHATSAPP_TOKEN", "")
WA_PHONE_ID     = os.getenv("WHATSAPP_PHONE_ID", "")
WA_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "cps_webhook_2026")
WA_APP_SECRET   = os.getenv("WHATSAPP_APP_SECRET", "")

# In-memory sessions: {phone: {"step": "root"|"find_parish", "lang": "en"|"sw"}}
_wa_sessions: dict = {}

MENU_EN = (
    "\u271d\ufe0f *Catholic Parish Steward*\n\n"
    "Reply with a number:\n"
    "1\ufe0f\u20e3 Find a Church\n"
    "2\ufe0f\u20e3 Mass Times\n"
    "3\ufe0f\u20e3 Give via M-Pesa\n"
    "4\ufe0f\u20e3 Today's Reading\n"
    "5\ufe0f\u20e3 Emergency Contacts\n"
    "6\ufe0f\u20e3 Kiswahili \U0001f1f0\U0001f1ea\n\n"
    "Type *menu* anytime to return here."
)

MENU_SW = (
    "\u271d\ufe0f *Mwenyekiti wa Parokia*\n\n"
    "Jibu na namba:\n"
    "1\ufe0f\u20e3 Tafuta Kanisa\n"
    "2\ufe0f\u20e3 Ratiba ya Misa\n"
    "3\ufe0f\u20e3 Toa kwa M-Pesa\n"
    "4\ufe0f\u20e3 Somo la Leo\n"
    "5\ufe0f\u20e3 Namba za Dharura\n"
    "6\ufe0f\u20e3 English \U0001f1ec\U0001f1e7\n\n"
    "Andika *menyu* kurudi hapa."
)


def _wa_search_parishes(city: str) -> str:
    import urllib.request
    import urllib.parse
    import json as _json
    try:
        q   = urllib.parse.quote(f"Catholic church {city} Kenya")
        url = (f"https://nominatim.openstreetmap.org/search"
               f"?q={q}&format=json&limit=4&addressdetails=1")
        req = urllib.request.Request(url, headers={"User-Agent": "CatholicParishSteward/1.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = _json.loads(resp.read())
        if not data:
            return"No churches found near *{city}*. Try a nearby larger town."
        lines = []
        for place in data[:4]:
            name = place.get("display_name", "").split(",")[0]
            addr = place.get("address", {})
            area = addr.get("suburb") or addr.get("city") or addr.get("town") or ""
            lines.append(f"\u2022 {name}" + (f" \u2014 {area}" if area else ""))
        return"\u26ea *Churches near {city}*\n\n" + "\n".join(lines) + "\n\n_Data: OpenStreetMap_"
    except Exception:
        return "Search unavailable. Try: catholicparishsteward.streamlit.app"


def _wa_get_reading() -> str:
    try:
        from services.lectionary import get_reading as _gr
        r = _gr()
        feast = f"\U0001f389 *{r['feast']}*\n" if r["feast"] else ""
        refs  = " \u00b7 ".join(r["readings"])
        return (f"\U0001f4d6 *Today's Reading*\n\n{feast}"
                f"_{r['season']} Week {r['week']} \u00b7 Year {r['cycle']}_\n\n"
                f"{refs}\n\nFull text: usccb.org/bible/readings")
    except Exception:
        return "\U0001f4d6 Today's reading: see usccb.org/bible/readings"


def _wa_handle(phone: str, body: str) -> str:
    sess = _wa_sessions.setdefault(phone, {"step": "root", "lang": "en"})
    lang = sess["lang"]
    text = body.strip().lower()

    if text in ("menu", "menyu", "0", "start", "hi", "hello", "habari", "hujambo", ""):
        sess["step"] = "root"
        return MENU_SW if lang == "sw" else MENU_EN

    if sess["step"] == "find_parish":
        sess["step"] = "root"
        return _wa_search_parishes(body.strip())

    if text in ("1",):
        sess["step"] = "find_parish"
        if lang == "sw":
            return "\U0001f5fa\ufe0f Ingiza mji wako:\n(mfano: Nairobi, Nakuru, Kisumu, Mombasa)"
        return "\U0001f5fa\ufe0f Enter your city or town:\n(e.g. Nairobi, Nakuru, Kisumu, Mombasa)"

    if text in ("2",):
        if lang == "sw":
            return "\u26ea *Ratiba ya Misa Nairobi*\n\nHoly Family: 7am 9am 11am 6pm\nConsolata: 7:30am 10am 12pm 6pm\nSt Paul's: 8am 10am\nKristo Mfalme: 7am 9am 11am\n\n_Jumapili zote._"
        return "\u26ea *Nairobi Mass Times*\n\nHoly Family Basilica: 7am 9am 11am 6pm\nConsolata Shrine: 7:30am 10am 12pm 6pm\nSt Paul's University: 8am 10am\nChrist the King: 7am 9am 11am\n\n_All times Sunday._"

    if text in ("3",):
        return "\U0001f4b0 *Parish Giving via M-Pesa*\n\nContact your parish coordinator for the Paybill number.\n\nFull giving page: catholicparishsteward.streamlit.app"

    if text in ("4",):
        return _wa_get_reading()

    if text in ("5",):
        if lang == "sw":
            return "\U0001f198 *Dharura*\n\nHoly Family: 0202228959\nDiocesi Nairobi: 0722205176\nCaritas Kenya: 0202714188\n\n_Dharura ya maisha piga 999._"
        return "\U0001f198 *Emergency Contacts*\n\nHoly Family Basilica: 0202228959\nDiocese of Nairobi: 0722205176\nCaritas Kenya: 0202714188\n\n_Life emergencies: call 999._"

    if text in ("6", "kiswahili", "swahili", "sw"):
        sess["lang"] = "sw"
        return MENU_SW

    if text in ("english", "en"):
        sess["lang"] = "en"
        return MENU_EN

    sess["step"] = "root"
    return (f"Sijaelewea '{body[:20]}'\n\n" + MENU_SW) if lang == "sw" else (f"I didn't understand '{body[:20]}'\n\n" + MENU_EN)


async def _wa_send(phone: str, text: str):
    if not WA_TOKEN or not WA_PHONE_ID:
        logger.warning("WhatsApp credentials not set — skipping send")
        return
    import httpx
    url = f"https://graph.facebook.com/v19.0/{WA_PHONE_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": text, "preview_url": False},
    }
    headers = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, json=payload, headers=headers)
        if r.status_code != 200:
            logger.error("WA send failed %s: %s", r.status_code, r.text[:200])


@app.get("/whatsapp")
async def wa_verify(request: Request):
    """Meta webhook verification."""
    p = dict(request.query_params)
    if p.get("hub.mode") == "subscribe" and p.get("hub.verify_token") == WA_VERIFY_TOKEN:
        logger.info("WhatsApp webhook verified by Meta")
        return PlainTextResponse(p.get("hub.challenge", ""))
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/whatsapp")
async def wa_receive(request: Request):
    """Receive WhatsApp messages from Meta Cloud API."""
    body_bytes = await request.body()

    if WA_APP_SECRET:
        sig = request.headers.get("x-hub-signature-256", "")
        expected = "sha256=" + _hmac.new(
            WA_APP_SECRET.encode(), body_bytes, hashlib.sha256
        ).hexdigest()
        if not _hmac.compare_digest(sig, expected):
            raise HTTPException(status_code=403, detail="Bad signature")

    try:
        data    = json.loads(body_bytes)
        changes = data["entry"][0]["changes"][0]["value"]
        if "statuses" in changes and "messages" not in changes:
            return {"status": "ok"}
        msg   = changes["messages"][0]
        phone = msg["from"]
        mtype = msg.get("type", "")
        if mtype == "text":
            body = msg["text"]["body"]
        elif mtype == "interactive":
            body = (msg["interactive"].get("button_reply", {}).get("id") or
                    msg["interactive"].get("list_reply", {}).get("id") or "menu")
        else:
            body = "menu"
        reply = _wa_handle(phone, body)
        await _wa_send(phone, reply)
    except (KeyError, IndexError, json.JSONDecodeError):
        pass

    return {"status": "ok"}
