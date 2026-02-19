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
import logging
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
