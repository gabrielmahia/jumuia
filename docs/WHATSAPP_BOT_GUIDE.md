# WhatsApp Bot Integration Guide
## Catholic Network Tools

---

## Status: FRAMEWORK READY — Activation Required

The bot logic, conversation store, language detection, and AI pipeline are fully
implemented. What's needed is a **public HTTPS webhook endpoint** and provider
credentials.

---

## Section 1 — Why Streamlit Can't Receive Webhooks

Streamlit apps are request-response: they wait for a browser to open them.
WhatsApp (via Africa's Talking or Twilio) sends **inbound POST requests** when a
user messages your number. There's no persistent listener in Streamlit to receive these.

**Solution:** Deploy a lightweight FastAPI companion service. Total additional
infrastructure: ~30 lines of Python on Render's free tier.

---

## Section 2 — Provider Comparison

| Provider | Sandbox | Live requirement | Cost | Notes |
|----------|---------|-----------------|------|-------|
| **Africa's Talking** | ✅ Free | Meta Business verification | Pay-per-message | Already in stack (SMS) |
| **Twilio** | ✅ Free | Meta Business verification | Pay-per-message | Well-documented |
| **360dialog** | ✅ | Meta partner | Monthly fee | Direct WhatsApp API |

**Recommendation:** Africa's Talking — already integrated for SMS, single vendor.

---

## Section 3 — Deployment Architecture

```
WhatsApp User
      │
      ▼
Africa's Talking / Twilio
      │  POST /webhook  (JSON)
      ▼
FastAPI App  ─── Render / Railway (free tier)
      │
      ├── parse_at_inbound(payload)
      ├── handle_inbound_message(parsed)
      │       ├── ai_service.bot_respond()       [Claude Haiku]
      │       ├── whatsapp_service.save_turn()   [SQLite]
      │       └── whatsapp_service.send_reply()  [AT API]
      └── return 200 OK to provider
```

---

## Section 4 — Implementation Steps

### Step 1: Create webhook_app.py in project root

```python
"""
Companion webhook service — deploy separately from Streamlit app.
"""
import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from services.whatsapp_service import parse_at_inbound, handle_inbound_message

load_dotenv()
app = FastAPI(title="CNT WhatsApp Webhook")

@app.get("/health")
def health():
    return {"status": "ok", "service": "cnt-whatsapp-webhook"}

@app.post("/webhook/at")
async def at_webhook(request: Request):
    """Africa's Talking inbound handler."""
    payload = await request.json()
    parsed  = parse_at_inbound(payload)
    if not parsed or not parsed.get("message"):
        return {"status": "ignored"}
    result = handle_inbound_message(parsed)
    return {
        "status": "processed",
        "reply_sent": result.get("sent", False),
        "language": result.get("language", "en"),
    }

@app.post("/webhook/twilio")
async def twilio_webhook(request: Request):
    """Twilio inbound handler (form-encoded)."""
    from services.whatsapp_service import parse_twilio_inbound
    form = await request.form()
    parsed = parse_twilio_inbound(dict(form))
    if not parsed:
        return {"status": "ignored"}
    result = handle_inbound_message(parsed)
    return {"status": "processed"}
```

### Step 2: render.yaml for free-tier deployment

```yaml
services:
  - type: web
    name: cnt-whatsapp-webhook
    env: python
    plan: free
    buildCommand: pip install fastapi uvicorn anthropic africastalking python-dotenv
    startCommand: uvicorn webhook_app:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: AFRICASTALKING_API_KEY
        sync: false
      - key: AFRICASTALKING_USERNAME
        value: sandbox
      - key: CNT_DB_PATH
        value: /tmp/cnt_whatsapp.db
```

### Step 3: Register webhook URL with Africa's Talking

1. Log in at account.africastalking.com
2. Go to: WhatsApp → Sandbox → Webhook URL
3. Enter: `https://cnt-whatsapp-webhook.onrender.com/webhook/at`
4. Save and send a test message

### Step 4: Activate live sending

1. Complete Meta Business verification:
   - Go to business.facebook.com/whatsapp
   - Submit business documents
   - Approval: 2–5 business days

2. Switch `AFRICASTALKING_USERNAME` from `sandbox` to your production username
3. Update `WHATSAPP_PROVIDER=africas_talking` in `.env`

---

## Section 5 — Bot Commands & Capabilities

The bot responds to natural language in 6 languages. No commands required.

| User says | Bot does |
|-----------|----------|
| "What time is Mass on Sunday?" | Searches parish directory, returns times |
| "Habari za Misa" (Kiswahili) | Detects Swahili, responds in Swahili |
| "Where is the nearest Catholic church?" | Asks for location, searches directory |
| "What is the Liturgical calendar today?" | Provides current season + feast days |
| "How do I get baptized?" | Explains process, refers to parish priest |
| "Merci" | Detects French, continues in French |

---

## Section 6 — Multi-Language Support

Language detection flow:
1. Keyword heuristic (instant, no API cost) → `_detect_language_simple()`
2. If ambiguous → Claude Haiku detects language (< 0.01 USD per message)

Supported: English, Kiswahili, French, Spanish, Portuguese, Luganda

---

## Estimated Activation Time

| Task | Time |
|------|------|
| Deploy FastAPI to Render | 15 minutes |
| Register AT sandbox webhook | 5 minutes |
| Test end-to-end in sandbox | 30 minutes |
| Meta Business verification | 2–5 business days |
| **Total to sandbox-live** | **~1 hour** |
| **Total to WhatsApp-live** | **~1 week** |
