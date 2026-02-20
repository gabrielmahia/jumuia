"""
WhatsApp Business API Webhook — Catholic Parish Steward
========================================================
Receives WhatsApp messages via Meta Cloud API and responds
using the same parish logic as the USSD service.

Menu flow mirrors USSD but conversational:
- User sends any message → gets main menu
- User sends 1-6 → gets response
- User sends city name after choosing "Find Parish" → gets results
- Bilingual: send "sw" or "kiswahili" for Swahili mode
"""

import os
import json
import logging
import hashlib
import hmac
from fastapi import FastAPI, Request, Response, HTTPException
import httpx

logger = logging.getLogger(__name__)

app = FastAPI(title="CPS WhatsApp Webhook")

# ── Config ────────────────────────────────────────────────────────────────────
WA_TOKEN        = os.getenv("WHATSAPP_TOKEN", "")
WA_PHONE_ID     = os.getenv("WHATSAPP_PHONE_ID", "")
WA_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "cps_webhook_2026")
WA_APP_SECRET   = os.getenv("WHATSAPP_APP_SECRET", "")

API_URL = f"https://graph.facebook.com/v19.0/{WA_PHONE_ID}/messages"

# ── Session state (in-memory, resets on cold start — fine for USSD-style) ────
# Structure: {phone: {"step": "root"|"find_parish", "lang": "en"|"sw"}}
sessions: dict = {}

# ── Menu text ─────────────────────────────────────────────────────────────────
MENU_EN = """✝️ *Catholic Parish Steward*

Reply with a number:
1️⃣ Find a Church
2️⃣ Mass Times
3️⃣ Give via M-Pesa
4️⃣ Today's Reading
5️⃣ Emergency Contacts
6️⃣ Kiswahili 🇰🇪

Type *menu* anytime to return here."""

MENU_SW = """✝️ *Mwenyekiti wa Parokia*

Jibu na namba:
1️⃣ Tafuta Kanisa
2️⃣ Ratiba ya Misa
3️⃣ Toa kwa M-Pesa
4️⃣ Somo la Leo
5️⃣ Namba za Dharura
6️⃣ English 🇬🇧

Andika *menyu* kurudi hapa."""

MASS_TIMES_EN = """⛪ *Nairobi Mass Times*

Holy Family Basilica: 7am · 9am · 11am · 6pm
Consolata Shrine: 7:30am · 10am · 12pm · 6pm
St Paul's University: 8am · 10am
Christ the King: 7am · 9am · 11am

_All times Sunday. Weekday check parish notice board._"""

MASS_TIMES_SW = """⛪ *Ratiba ya Misa Nairobi*

Holy Family: 7am · 9am · 11am · 6pm
Consolata Shrine: 7:30am · 10am · 12pm · 6pm
St Paul's: 8am · 10am
Kristo Mfalme: 7am · 9am · 11am

_Jumapili zote. Wiki angalia bodi ya parokia._"""

EMERGENCY_EN = """🆘 *Parish Emergency Contacts*

Holy Family Basilica: 0202228959
Diocese of Nairobi: 0722205176
Caritas Kenya: 0202714188
Kenya Catholic Secretariat: 0202714188

_For life-threatening emergencies call 999._"""

EMERGENCY_SW = """🆘 *Namba za Dharura za Parokia*

Holy Family Basilica: 0202228959
Diocese ya Nairobi: 0722205176
Caritas Kenya: 0202714188

_Dharura ya maisha piga simu 999._"""

GIVING_EN = """💰 *Parish Giving via M-Pesa*

Paybill: *123456*
Account: Your parish name

Or send money directly to your parish M-Pesa till.

_Contact your coordinator to set up direct giving._"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_reading() -> str:
    try:
        from services.lectionary import get_reading as _get
        r = _get()
        feast = f"🎉 *{r['feast']}*\n" if r["feast"] else ""
        refs  = " · ".join(r["readings"])
        return (f"📖 *Today's Reading*\n\n"
                f"{feast}"
                f"_{r['season']} Week {r['week']} · Year {r['cycle']}_\n\n"
                f"{refs}\n\n"
                f"Full text: usccb.org/bible/readings")
    except Exception:
        return "📖 Today's reading: see usccb.org/bible/readings"


def search_parishes(city: str) -> str:
    try:
        import urllib.request
        import urllib.parse
        import json as _json
        q   = urllib.parse.quote(f"Catholic church {city} Kenya")
        url = (f"https://nominatim.openstreetmap.org/search"
               f"?q={q}&format=json&limit=5&addressdetails=1")
        req = urllib.request.Request(url, headers={"User-Agent": "CatholicParishSteward/1.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = _json.loads(resp.read())
        if not data:
            return"No churches found near *{city}*. Try a nearby larger town."
        results = []
        for place in data[:4]:
            name = place.get("display_name", "").split(",")[0]
            addr = place.get("address", {})
            area = addr.get("suburb") or addr.get("city") or addr.get("town") or ""
            results.append(f"• {name}" + (f" — {area}" if area else ""))
        return"⛪ *Churches near {city}*\n\n" + "\n".join(results) + \
               "\n\n_Data: OpenStreetMap_"
    except Exception:
        return"Search unavailable right now. Try: catholicparishsteward.streamlit.app"


async def send_message(phone: str, text: str):
    """Send a WhatsApp text message via Cloud API."""
    if not WA_TOKEN or not WA_PHONE_ID:
        logger.warning("WhatsApp credentials not configured")
        return
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": text, "preview_url": False},
    }
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(API_URL, json=payload, headers=headers)
        if r.status_code != 200:
            logger.error("WA send failed: %s %s", r.status_code, r.text)


def handle_message(phone: str, body: str) -> str:
    """Process incoming message and return reply text."""
    sess  = sessions.setdefault(phone, {"step": "root", "lang": "en"})
    lang  = sess["lang"]
    text  = body.strip().lower()

    # ── Reset to menu ──────────────────────────────────────────────────────
    if text in ("menu", "menyu", "0", "start", "hi", "hello", "habari", "hujambo"):
        sess["step"] = "root"
        return MENU_SW if lang == "sw" else MENU_EN

    # ── Mid-flow: waiting for city input ──────────────────────────────────
    if sess["step"] == "find_parish":
        sess["step"] = "root"
        return search_parishes(body.strip())

    # ── Root menu choices ─────────────────────────────────────────────────
    if text in ("1", "find", "tafuta"):
        sess["step"] = "find_parish"
        if lang == "sw":
            return "🗺️ Ingiza mji wako:\n(mfano: Nairobi, Nakuru, Kisumu, Mombasa)"
        return "🗺️ Enter your city or town:\n(e.g. Nairobi, Nakuru, Kisumu, Mombasa)"

    if text in ("2", "mass", "misa"):
        return MASS_TIMES_SW if lang == "sw" else MASS_TIMES_EN

    if text == "3":
        return GIVING_EN

    if text in ("4", "reading", "somo"):
        return get_reading()

    if text in ("5", "emergency", "dharura"):
        return EMERGENCY_SW if lang == "sw" else EMERGENCY_EN

    if text in ("6", "kiswahili", "swahili", "sw"):
        sess["lang"] = "sw"
        return MENU_SW

    if text in ("english", "en"):
        sess["lang"] = "en"
        return MENU_EN

    # ── Unknown — show menu ───────────────────────────────────────────────
    sess["step"] = "root"
    if lang == "sw":
        return"Sijaelewea '{body[:20]}'\n\n" + MENU_SW
    return"I didn't understand '{body[:20]}'\n\n" + MENU_EN


# ── Webhook endpoints ─────────────────────────────────────────────────────────

@app.get("/whatsapp")
async def verify_webhook(request: Request):
    """Meta webhook verification handshake."""
    params = dict(request.query_params)
    mode      = params.get("hub.mode")
    token     = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    if mode == "subscribe" and token == WA_VERIFY_TOKEN:
        logger.info("WhatsApp webhook verified")
        return Response(content=challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/whatsapp")
async def receive_message(request: Request):
    """Receive and process incoming WhatsApp messages."""
    # Verify Meta signature
    if WA_APP_SECRET:
        sig = request.headers.get("x-hub-signature-256", "")
        body_bytes = await request.body()
        expected = "sha256=" + hmac.new(
            WA_APP_SECRET.encode(), body_bytes, hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(sig, expected):
            raise HTTPException(status_code=403, detail="Invalid signature")
        data = json.loads(body_bytes)
    else:
        data = await request.json()

    try:
        entry   = data["entry"][0]
        changes = entry["changes"][0]["value"]

        # Skip status updates (delivered, read receipts)
        if "statuses" in changes and "messages" not in changes:
            return {"status": "ok"}

        msg   = changes["messages"][0]
        phone = msg["from"]
        mtype = msg.get("type", "")

        if mtype == "text":
            body = msg["text"]["body"]
        elif mtype == "interactive":
            # Button/list replies
            body = (msg["interactive"].get("button_reply", {}).get("id") or
                    msg["interactive"].get("list_reply", {}).get("id") or "menu")
        else:
            body = "menu"

        reply = handle_message(phone, body)
        await send_message(phone, reply)

    except (KeyError, IndexError):
        pass  # Non-message webhook event — ignore silently

    return {"status": "ok"}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "cnt-whatsapp"}
