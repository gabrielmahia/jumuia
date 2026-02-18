"""WhatsApp Bot — Activation Status & Framework Guide"""
import streamlit as st
import sys
sys.path.insert(0, ".")

from services.whatsapp_service import activation_status, _detect_language_simple
from services.ai_service import bot_respond, SUPPORTED_LANGUAGES

st.set_page_config(page_title="WhatsApp Bot — CNT", page_icon="💬", layout="wide")
st.title("💬 WhatsApp Bot")

status = activation_status()

st.info(
    f"**Framework Status: {status['framework_status']}** | "
    f"**Live Status: {status['live_status']}** | "
    f"Provider: {status['current_provider']}",
    icon="🔧",
)

st.warning(
    f"⚠️ {status['webhook_requirement']}",
    icon="⚠️",
)

tab1, tab2, tab3 = st.tabs(
    ["📊 Activation Status", "🧪 Test Bot Locally", "📖 Deployment Guide"]
)


# ─────────────────────────────────────────────
# TAB 1 — STATUS
# ─────────────────────────────────────────────
with tab1:
    st.subheader("Africa's Talking")
    at = status["africas_talking"]
    st.markdown(f"**Configured:** {'✅' if at['configured'] else '❌'}")
    st.markdown(f"**Next step:** {at['next_step']}")
    st.markdown(f"[Open AT Dashboard]({at['sandbox_url']})")

    st.divider()
    st.subheader("Twilio (Alternative)")
    tw = status["twilio"]
    st.markdown(f"**Configured:** {'✅' if tw['configured'] else '❌'}")
    st.markdown(f"**Next step:** {tw['next_step']}")
    st.markdown(f"[Open Twilio Console]({tw['sandbox_url']})")

    st.divider()
    st.subheader("Activation Checklist")
    st.markdown("""
- [ ] Choose provider: Africa's Talking (recommended) or Twilio
- [ ] Set API credentials in `.env`
- [ ] Deploy FastAPI webhook companion service (see Deployment Guide tab)
- [ ] Register webhook URL in provider dashboard
- [ ] Test inbound message in provider sandbox
- [ ] Request Meta WhatsApp Business Account verification
- [ ] Go live
    """)


# ─────────────────────────────────────────────
# TAB 2 — LOCAL TEST
# ─────────────────────────────────────────────
with tab2:
    st.subheader("Test Bot Logic (No WhatsApp Required)")
    st.caption(
        "This simulates exactly what the WhatsApp bot will do when a message arrives. "
        "Useful for testing AI responses and language detection before deploying."
    )

    test_phone = st.text_input(
        "Simulated phone number", value="254700000000", help="Used to simulate conversation history"
    )
    test_message = st.text_input(
        "Test message", placeholder="e.g. What time is Mass on Sunday?"
    )

    if st.button("Send Test Message", type="primary"):
        if test_message.strip():
            detected_lang = _detect_language_simple(test_message)
            lang_name = SUPPORTED_LANGUAGES.get(detected_lang, "English")

            with st.spinner(f"Processing in {lang_name}…"):
                result = bot_respond(
                    test_message,
                    [],   # fresh conversation for test
                    language_code=detected_lang,
                )

            st.markdown("**Bot reply:**")
            if result["success"]:
                st.success(result["reply"])
                st.caption(f"Detected language: {lang_name} | Model: {result['model']}")
            else:
                st.error(f"Error: {result['error']}")
        else:
            st.warning("Enter a test message.")


# ─────────────────────────────────────────────
# TAB 3 — DEPLOYMENT GUIDE
# ─────────────────────────────────────────────
with tab3:
    st.subheader("WhatsApp Bot Deployment Architecture")
    st.markdown("""
### Why Streamlit Can't Receive Webhooks
Streamlit is a request-response app — it can't run a persistent HTTP listener.
WhatsApp (via AT or Twilio) needs to **POST inbound messages** to your endpoint.
You need a **companion webhook service** running alongside your Streamlit app.

---

### Recommended Architecture
```
WhatsApp User
     │
     ▼
AT / Twilio
     │  POST /webhook
     ▼
FastAPI App (Render / Railway — free tier)
     │  calls
     ├──► whatsapp_service.handle_inbound_message()
     │         │
     │         ├──► ai_service.bot_respond() [Claude Haiku]
     │         ├──► whatsapp_service.save_turn() [SQLite]
     │         └──► whatsapp_service.send_reply() [AT / Twilio]
     │
     └──► (same SQLite as Streamlit app if shared volume)
```

---

### Fastest Path: Africa's Talking on Render (Free)

**Step 1 — Create `webhook_app.py`:**
```python
from fastapi import FastAPI, Request
from services.whatsapp_service import parse_at_inbound, handle_inbound_message

app = FastAPI()

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    payload = await request.json()
    parsed  = parse_at_inbound(payload)
    if parsed:
        result = handle_inbound_message(parsed)
        return {"status": "ok", "reply_sent": result["sent"]}
    return {"status": "ignored"}
```

**Step 2 — Deploy to Render:**
```bash
# render.yaml (free tier)
services:
  - type: web
    name: cnt-whatsapp-webhook
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn webhook_app:app --host 0.0.0.0 --port $PORT
```

**Step 3 — Register webhook URL in AT Dashboard:**
```
https://cnt-whatsapp-webhook.onrender.com/webhook
```

**Step 4 — Meta Business Verification (for live):**
- Apply at: business.facebook.com/whatsapp
- Requires: business registration document
- Timeline: 2–5 business days

---

### Full guide: `docs/WHATSAPP_BOT_GUIDE.md`
    """)
