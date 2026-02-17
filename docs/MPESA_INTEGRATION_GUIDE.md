# M-Pesa Integration Guide
## Catholic Network Tools — Parish Giving

---

## Current Status: SANDBOX ACTIVE

The full Daraja API integration is implemented. Sandbox works immediately with
credentials from developer.safaricom.co.ke. Live giving requires Safaricom
business registration approval.

---

## Sandbox Testing (Works Now)

1. Register at developer.safaricom.co.ke
2. Create an app — get Consumer Key + Consumer Secret
3. Add to `.env`:
   ```
   MPESA_CONSUMER_KEY=your_key
   MPESA_CONSUMER_SECRET=your_secret
   MPESA_SHORTCODE=174379
   MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
   MPESA_ENV=sandbox
   ```
4. Use Daraja simulator at developer.safaricom.co.ke to trigger callbacks

---

## Live Activation Requirements

### Business Registration Documents Needed

For a **parish / church organization:**
- Certificate of Registration (Registrar of Societies)
- Church letterhead with official contact
- Director/Authorized Official ID (national ID or passport)
- KRA PIN certificate

For an **NGO:**
- NGO Registration certificate
- NGO Bureau compliance certificate

### Safaricom Approval Process

1. Go to: developer.safaricom.co.ke → Go Live
2. Submit business documents
3. Specify use case: "Parish donation collection"
4. Safaricom reviews: **3–10 business days**
5. Receive live Paybill/Till shortcode
6. Update `.env`:
   ```
   MPESA_ENV=live
   MPESA_SHORTCODE=your_live_shortcode
   MPESA_PASSKEY=your_live_passkey
   ```

---

## Callback URL Requirement

M-Pesa requires a **publicly reachable HTTPS endpoint** to confirm transactions.
Streamlit Cloud cannot receive callbacks directly.

**Solutions (same options as WhatsApp webhook):**
- FastAPI on Render (free tier) — recommended
- Any HTTPS endpoint that accepts POST requests

**Callback endpoint:**
```python
@app.post("/mpesa/callback")
async def mpesa_callback(request: Request):
    from services.mpesa_service import handle_callback
    payload = await request.json()
    result  = handle_callback(payload)
    return {"ResultCode": 0, "ResultDesc": "Accepted"}
```

---

## Giving Record Architecture

All transactions stored in SQLite with:
- `sandbox` flag (1/0) — prevents mixing test and real data
- `status`: PENDING → COMPLETE / FAILED
- `mpesa_receipt`: M-Pesa transaction reference
- Dashboard shows only `sandbox=0` records in live mode

---

## Parish Giving Best Practices

- Display M-Pesa Paybill number prominently for manual giving fallback
- Send SMS confirmation after successful transaction (Africa's Talking)
- Weekly giving summary email to parish finance coordinator
- Annual giving statement for major donors (tax purposes)
