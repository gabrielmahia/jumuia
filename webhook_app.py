"""
WhatsApp Webhook Companion Service — Catholic Network Tools
============================================================
Deploy this as a SEPARATE service alongside the Streamlit app.
Streamlit cannot receive inbound webhooks; this FastAPI app handles that.

DEPLOYMENT (Render free tier — recommended):
  1. Create new Web Service on render.com
  2. Connect to this repository
  3. Build command:  pip install -r requirements-webhook.txt
  4. Start command:  uvicorn webhook_app:app --host 0.0.0.0 --port $PORT
  5. Add environment variables (ANTHROPIC_API_KEY, AFRICASTALKING_API_KEY, etc.)
  6. Register https://your-service.onrender.com/webhook in AT/Twilio dashboard

STATUS: FRAMEWORK READY — deploy after configuring .env credentials
"""

import os
import logging
from contextlib import asynccontextmanager

# FastAPI is an optional dependency — install only for webhook deployment
try:
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.responses import JSONResponse
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

import sys
sys.path.insert(0, ".")

from services.whatsapp_service import (
    parse_at_inbound,
    parse_twilio_inbound,
    handle_inbound_message,
    init_whatsapp_db,
)
from services.mpesa_service import handle_callback, init_giving_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")  # Optional: add to AT/Twilio for verification


# ─────────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────────

if not FASTAPI_AVAILABLE:
    raise ImportError(
        "FastAPI not installed. Run: pip install fastapi uvicorn[standard]\n"
        "Or install requirements-webhook.txt"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize databases on startup."""
    init_whatsapp_db()
    init_giving_db()
    logger.info("Webhook service started. Databases initialized.")
    yield


app = FastAPI(
    title="Catholic Network Tools — Webhook Service",
    description="WhatsApp bot and M-Pesa callback receiver",
    version="1.0.0",
    lifespan=lifespan,
)


# ─────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────

@app.get("/health")
async def health():
    """Health check endpoint — use this to verify deployment."""
    return {
        "status": "ok",
        "service": "cnt-webhook",
        "whatsapp_provider": os.getenv("WHATSAPP_PROVIDER", "africas_talking"),
        "mpesa_env": os.getenv("MPESA_ENV", "sandbox"),
    }


# ─────────────────────────────────────────────
# WHATSAPP WEBHOOK — AFRICA'S TALKING
# ─────────────────────────────────────────────

@app.post("/webhook/whatsapp/at")
async def whatsapp_at_webhook(request: Request):
    """
    Africa's Talking inbound WhatsApp webhook.
    Register this URL in AT dashboard → WhatsApp → Callback URL.
    """
    try:
        payload = await request.json()
        logger.info("AT WhatsApp inbound: %s", payload)

        parsed = parse_at_inbound(payload)
        if not parsed or not parsed.get("message"):
            return JSONResponse({"status": "ignored", "reason": "empty_message"})

        result = handle_inbound_message(parsed)
        logger.info(
            "Response sent: phone=%s sent=%s lang=%s",
            result["phone"], result["sent"], result["language"]
        )

        return JSONResponse({
            "status": "ok",
            "reply_sent": result["sent"],
            "provider": result["provider"],
        })

    except Exception as e:
        logger.error("AT webhook error: %s", e)
        # Return 200 to prevent AT from retrying on error
        return JSONResponse({"status": "error", "detail": str(e)}, status_code=200)


# ─────────────────────────────────────────────
# WHATSAPP WEBHOOK — TWILIO
# ─────────────────────────────────────────────

@app.post("/webhook/whatsapp/twilio")
async def whatsapp_twilio_webhook(request: Request):
    """
    Twilio inbound WhatsApp webhook (form-encoded).
    Register this URL in Twilio Console → WhatsApp → Sandbox settings.
    """
    try:
        form_data = dict(await request.form())
        logger.info("Twilio WhatsApp inbound: %s", form_data.get("From", "unknown"))

        parsed = parse_twilio_inbound(form_data)
        if not parsed or not parsed.get("message"):
            return JSONResponse({"status": "ignored"})

        result = handle_inbound_message(parsed)

        # Twilio expects a TwiML response or empty 200
        return JSONResponse({
            "status": "ok",
            "reply_sent": result["sent"],
        })

    except Exception as e:
        logger.error("Twilio webhook error: %s", e)
        return JSONResponse({"status": "error", "detail": str(e)}, status_code=200)


# ─────────────────────────────────────────────
# M-PESA CALLBACK
# ─────────────────────────────────────────────

@app.post("/webhook/mpesa/callback")
async def mpesa_callback(request: Request):
    """
    Safaricom Daraja STK Push callback.
    Set MPESA_CALLBACK_URL=https://your-service.onrender.com/webhook/mpesa/callback
    """
    try:
        payload = await request.json()
        logger.info("M-Pesa callback received")

        result = handle_callback(payload)

        if result.get("success"):
            logger.info(
                "Payment complete: receipt=%s amount=%s",
                result.get("mpesa_receipt"), result.get("amount")
            )
        else:
            logger.info("Payment not completed: code=%s", result.get("result_code"))

        # Safaricom requires a specific acknowledgment format
        return JSONResponse({
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        })

    except Exception as e:
        logger.error("M-Pesa callback error: %s", e)
        return JSONResponse({
            "ResultCode": 0,  # Always return 0 to prevent Safaricom retries
            "ResultDesc": "Error handled"
        })


# ─────────────────────────────────────────────
# LOCAL DEV ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "webhook_app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True,
    )


# ─────────────────────────────────────────────
# USSD WEBHOOK — AFRICA'S TALKING
# ─────────────────────────────────────────────

@app.post("/webhook/ussd")
async def ussd_webhook(request: Request):
    """
    Africa's Talking USSD webhook.
    AT sends form-encoded POST on every keypress.
    Register this URL in AT dashboard → USSD → Create Channel → Callback URL.

    Sandbox: use Launch Simulator at account.africastalking.com — no real URL needed.
    Live: needs public HTTPS endpoint (this Render service).
    """
    try:
        from services.ussd_service import handle_ussd_session, log_ussd_session

        form = dict(await request.form())
        session_id   = form.get("sessionId", "")
        service_code = form.get("serviceCode", "")
        phone        = form.get("phoneNumber", "")
        text         = form.get("text", "")

        logger.info("USSD: phone=%s text='%s'", phone, text)

        response = handle_ussd_session(session_id, service_code, phone, text)
        log_ussd_session(session_id, phone, text, response)

        # AT requires plain text response with Content-Type text/plain
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(content=response)

    except Exception as e:
        logger.error("USSD webhook error: %s", e)
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(content="END Service unavailable. Please try again.")
