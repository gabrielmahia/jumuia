"""
WhatsApp Bot Service — Catholic Network Tools

STATUS: FRAMEWORK ONLY — NOT LIVE

Two path options (see docs/WHATSAPP_BOT_GUIDE.md):
  A) Africa's Talking WhatsApp Business API (preferred — already in stack)
     Sandbox: available immediately at account.africastalking.com
     Live:    requires Meta WhatsApp Business Account verification

  B) Twilio WhatsApp Sandbox (alternative)
     Sandbox: available in minutes
     Live:    requires Meta Business verification (same requirement)

ARCHITECTURE:
  This module provides:
  1. Inbound message handler  — parse AT/Twilio webhook payload
  2. AI response pipeline     — routes to ai_service.bot_respond()
  3. Outbound sender          — sends reply via AT or Twilio
  4. Conversation store       — SQLite for multi-turn context

DEPLOYMENT NOTE (read before activating):
  WhatsApp bots require a PUBLIC HTTPS webhook endpoint.
  Streamlit Cloud cannot receive inbound webhooks.
  You need a companion service:
    - FastAPI on Render/Railway (free tier)
    - Flask on Heroku
    - Cloudflare Worker
  See docs/WHATSAPP_BOT_GUIDE.md — Section 3: Deployment Architecture.

TO ACTIVATE AFRICA'S TALKING SANDBOX:
  1. Create account at account.africastalking.com
  2. Enable WhatsApp sandbox channel
  3. Set AFRICASTALKING_API_KEY and AFRICASTALKING_USERNAME in .env
  4. Set WHATSAPP_PROVIDER=africas_talking
  5. Deploy FastAPI webhook app (template in docs/webhook_app_template.py)
  6. Register webhook URL in AT dashboard
"""

import os
import sqlite3
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

WHATSAPP_PROVIDER   = os.getenv("WHATSAPP_PROVIDER", "africas_talking")
AT_API_KEY          = os.getenv("AFRICASTALKING_API_KEY", "")
AT_USERNAME         = os.getenv("AFRICASTALKING_USERNAME", "sandbox")
TWILIO_SID          = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN   = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUM = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

DB_PATH = Path(os.getenv("CNT_DB_PATH", "data/parishes.db"))


# ─────────────────────────────────────────────
# CONVERSATION STORE
# ─────────────────────────────────────────────

def init_whatsapp_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS whatsapp_conversations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            phone       TEXT NOT NULL,
            role        TEXT NOT NULL,         -- 'user' | 'assistant'
            content     TEXT NOT NULL,
            language    TEXT DEFAULT 'en',
            created_at  TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_wa_phone_time
        ON whatsapp_conversations(phone, created_at DESC)
    """)
    conn.commit()
    conn.close()


def get_conversation_history(phone: str, limit: int = 10) -> list[dict]:
    """Return last N turns for a given phone number (for multi-turn context)."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        """SELECT role, content FROM whatsapp_conversations
           WHERE phone = ?
           ORDER BY created_at DESC, id DESC
           LIMIT ?""",
        (phone, limit),
    ).fetchall()
    conn.close()
    # Reverse so oldest first (correct order for Claude messages)
    return [{"role": r[0], "content": r[1]} for r in reversed(rows)]


def save_turn(phone: str, role: str, content: str, language: str = "en") -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO whatsapp_conversations (phone, role, content, language)
           VALUES (?,?,?,?)""",
        (phone, role, content, language),
    )
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
# INBOUND WEBHOOK PARSERS
# ─────────────────────────────────────────────

def parse_at_inbound(payload: dict) -> Optional[dict]:
    """
    Parse Africa's Talking inbound WhatsApp webhook payload.

    AT payload shape (WhatsApp Business channel):
    {
        "from": "2547XXXXXXXX",
        "to":   "shortcode",
        "text": "Hello",
        "id":   "ATxxxxxx",
        "date": "2024-01-01 12:00:00"
    }
    """
    try:
        return {
            "phone":      payload.get("from", ""),
            "message":    payload.get("text", ""),
            "message_id": payload.get("id", ""),
            "provider":   "africas_talking",
        }
    except Exception as e:
        logger.error("AT parse error: %s", e)
        return None


def parse_twilio_inbound(form_data: dict) -> Optional[dict]:
    """
    Parse Twilio WhatsApp inbound webhook (application/x-www-form-urlencoded).

    Key fields: From, Body, MessageSid
    """
    try:
        phone = form_data.get("From", "").replace("whatsapp:", "").lstrip("+")
        return {
            "phone":      phone,
            "message":    form_data.get("Body", ""),
            "message_id": form_data.get("MessageSid", ""),
            "provider":   "twilio",
        }
    except Exception as e:
        logger.error("Twilio parse error: %s", e)
        return None


# ─────────────────────────────────────────────
# OUTBOUND SENDERS
# ─────────────────────────────────────────────

def send_whatsapp_at(to_phone: str, message: str) -> dict:
    """
    Send WhatsApp message via Africa's Talking.
    SANDBOX: messages route to AT sandbox — no real delivery.
    """
    if not AT_API_KEY:
        return {"success": False, "error": "AFRICASTALKING_API_KEY not set"}

    try:
        import africastalking
        africastalking.initialize(AT_USERNAME, AT_API_KEY)
        # WhatsApp channel — AT SDK method
        # NOTE: AT WhatsApp API may vary; check latest SDK docs
        sms = africastalking.SMS
        response = sms.send(message, [f"+{to_phone}"])  # placeholder until WhatsApp SDK stable
        return {"success": True, "provider": "africas_talking", "response": response}
    except ImportError:
        return {
            "success": False,
            "error": "africastalking package not installed. Run: pip install africastalking"
        }
    except Exception as e:
        logger.error("AT send error: %s", e)
        return {"success": False, "error": str(e)}


def send_whatsapp_twilio(to_phone: str, message: str) -> dict:
    """
    Send WhatsApp message via Twilio.
    SANDBOX: use Twilio sandbox number.
    """
    if not TWILIO_SID or not TWILIO_AUTH_TOKEN:
        return {"success": False, "error": "Twilio credentials not set"}

    try:
        from twilio.rest import Client
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUM,
            to=f"whatsapp:+{to_phone}",
            body=message,
        )
        return {"success": True, "provider": "twilio", "sid": msg.sid}
    except ImportError:
        return {
            "success": False,
            "error": "twilio package not installed. Run: pip install twilio"
        }
    except Exception as e:
        logger.error("Twilio send error: %s", e)
        return {"success": False, "error": str(e)}


def send_reply(to_phone: str, message: str) -> dict:
    """Route to configured provider."""
    if WHATSAPP_PROVIDER == "twilio":
        return send_whatsapp_twilio(to_phone, message)
    return send_whatsapp_at(to_phone, message)


# ─────────────────────────────────────────────
# MAIN BOT PIPELINE
# ─────────────────────────────────────────────

def handle_inbound_message(parsed: dict) -> dict:
    """
    Full pipeline: parse → AI response → store → send reply.

    Call this from your FastAPI/Flask webhook endpoint.
    The Streamlit app cannot receive webhooks directly.
    """
    from services.ai_service import bot_respond

    phone   = parsed["phone"]
    message = parsed["message"]

    # Detect language (basic heuristic — Haiku call)
    lang = _detect_language_simple(message)

    # Load conversation history
    history = get_conversation_history(phone, limit=10)

    # Get AI response
    result = bot_respond(message, history, language_code=lang)
    reply  = result.get("reply", "Sorry, I could not process that.")

    # Store both turns
    save_turn(phone, "user",      message, lang)
    save_turn(phone, "assistant", reply,   lang)

    # Send reply
    send_result = send_reply(phone, reply)

    return {
        "phone":       phone,
        "message":     message,
        "reply":       reply,
        "sent":        send_result.get("success", False),
        "provider":    WHATSAPP_PROVIDER,
        "language":    lang,
    }


def _detect_language_simple(text: str) -> str:
    """
    Minimal keyword-based language detection before AI call.
    Avoids an extra API call for obvious cases.
    """
    kiswahili_markers = ["habari", "karibu", "asante", "sawa", "ndiyo"]
    french_markers    = ["bonjour", "merci", "messe", "eglise", "paroisse"]
    spanish_markers   = ["hola", "gracias", "iglesia", "parroquia", "misa"]
    portuguese_markers= ["olá", "obrigado", "missa", "igreja", "paróquia"]
    luganda_markers   = ["webale", "ssebo", "nnyabo"]

    lowered = text.lower()
    for marker in french_markers:
        if marker in lowered:
            return "fr"
    for marker in spanish_markers:
        if marker in lowered:
            return "es"
    for marker in portuguese_markers:
        if marker in lowered:
            return "pt"
    for marker in kiswahili_markers:
        if marker in lowered:
            return "sw"
    for marker in luganda_markers:
        if marker in lowered:
            return "lg"
    return "en"


# ─────────────────────────────────────────────
# STATUS + ACTIVATION GUIDE
# ─────────────────────────────────────────────

def activation_status() -> dict:
    """
    Display this on the admin panel to communicate WhatsApp bot readiness.
    """
    at_configured    = bool(AT_API_KEY and AT_USERNAME != "sandbox")
    twilio_configured = bool(TWILIO_SID and TWILIO_AUTH_TOKEN)

    return {
        "framework_status": "READY",
        "live_status":       "PENDING_ACTIVATION",
        "current_provider":  WHATSAPP_PROVIDER,
        "africas_talking": {
            "configured":    at_configured,
            "sandbox_url":   "https://account.africastalking.com",
            "next_step":     "Set AFRICASTALKING_API_KEY in .env" if not at_configured
                             else "Deploy webhook endpoint (see docs/)",
        },
        "twilio": {
            "configured":    twilio_configured,
            "sandbox_url":   "https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn",
            "next_step":     "Set TWILIO_ACCOUNT_SID + TWILIO_AUTH_TOKEN" if not twilio_configured
                             else "Deploy webhook endpoint",
        },
        "webhook_requirement": (
            "WhatsApp bots require a public HTTPS endpoint. "
            "Streamlit Cloud cannot receive inbound webhooks. "
            "Deploy a companion FastAPI service. "
            "See docs/WHATSAPP_BOT_GUIDE.md — Section 3."
        ),
        "guide": "docs/WHATSAPP_BOT_GUIDE.md",
    }
