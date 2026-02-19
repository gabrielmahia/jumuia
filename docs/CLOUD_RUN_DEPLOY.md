# USSD Webhook — Cloud Run Deployment Guide

## What you need before starting
- Google account (you have this — same one with Gemini key)
- Africa's Talking account (you have this — AFRICASTALKING_API_KEY in secrets)
- 20 minutes

---

## PART 1 — Google Cloud Setup (5 min)

### 1.1 Install gcloud CLI
Download from: https://cloud.google.com/sdk/docs/install

**On Mac:**
```bash
brew install google-cloud-sdk
```
**On Windows:** Download the installer from the link above.

### 1.2 Authenticate and set project
```bash
gcloud auth login
gcloud config set project gen-lang-client-0500961286
```
> That project ID is already visible in your AI Studio — same project as your Gemini key.

### 1.3 Enable Cloud Run (one-time)
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

## PART 2 — Deploy (3 commands)

From inside the `catholic-network-tools` repo folder:

```bash
# Clone if not local
git clone https://github.com/gabrielmahia/catholic-network-tools
cd catholic-network-tools

# Deploy (builds Docker image, pushes, deploys — all in one)
gcloud run deploy cnt-ussd \
  --source . \
  --region africa-south1 \
  --allow-unauthenticated \
  --set-env-vars AFRICASTALKING_API_KEY=YOUR_AT_KEY,AFRICASTALKING_USERNAME=YOUR_AT_USERNAME \
  --memory 256Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 3 \
  --timeout 10
```

Replace:
- `YOUR_AT_KEY` → your Africa's Talking API key (from Streamlit secrets)
- `YOUR_AT_USERNAME` → your AT username (shown in AT dashboard, e.g. `gabrielmahia`)

### What happens:
1. Cloud Build compiles your Docker image (~2 min)
2. Image is pushed to Google Container Registry
3. Cloud Run service is created and given a URL
4. You'll see: `Service URL: https://cnt-ussd-XXXX-ew.a.run.app`

**Copy that URL — you need it in Part 3.**

### Verify it's running:
```bash
curl https://cnt-ussd-XXXX-ew.a.run.app/health
# Should return: {"status":"ok","service":"cnt-ussd"}
```

---

## PART 3 — Africa's Talking USSD Channel (10 min)

### 3.1 Create USSD channel (sandbox first)
1. Go to https://account.africastalking.com
2. In the top dropdown, make sure you're in **Sandbox** (not Live)
3. Click **USSD** in the left sidebar
4. Click **Create Channel**
5. Fill in:
   - **Service Code:** `*384#` (shared — free, no approval needed)
   - **Name:** `Catholic Parish Steward`
   - **Callback URL:** `https://cnt-ussd-XXXX-ew.a.run.app/ussd`
     *(your Cloud Run URL + `/ussd`)*
6. Click **Create**

### 3.2 Test in the AT Simulator (no phone needed)
1. Still in sandbox — click **Launch Simulator** (top right of USSD page)
2. A phone simulator appears
3. Dial: `*384#`
4. You should see:
   ```
   Parish Steward
   1. Find Parish
   2. Mass Times
   3. Give via M-Pesa
   4. Today's Reading
   5. Emergency Contacts
   ```
5. Press **1** → enter a city → see results
6. Press **4** → see today's reading
7. **It's live.**

---

## PART 4 — Go Live (when ready)

### 4.1 Switch to Live environment
1. In AT dashboard, switch dropdown from **Sandbox** to **Live**
2. Create the same channel in Live
3. Shared `*384#` in Live is free and available immediately
4. Real phones in Kenya can now dial it

### 4.2 Your permanent dial code
```
*384*YOUR_CHANNEL_NUMBER#
```
AT assigns a channel number (e.g. `*384*1234#`) — this is your permanent code.
Put it on parish bulletins, WhatsApp groups, church notice boards.

---

## Cost summary
| Service | Free tier | Your usage | Cost |
|---------|-----------|------------|------|
| Cloud Run | 2M req/month, 360K GB-sec | ~100 sessions/day = 3,000/month | **$0** |
| AT USSD (sandbox) | Unlimited | Testing | **$0** |
| AT USSD (live) | Pay per session | ~KES 0.50/session | ~**$3/month** at 1,000 sessions |

---

## Troubleshooting

**Simulator shows nothing / error:**
- Check Cloud Run logs: `gcloud run logs read cnt-ussd --region africa-south1`
- Verify health: `curl YOUR_URL/health`

**"Session expired" immediately:**
- Your webhook is taking >5s — check Cloud Run logs for slow imports

**Wrong response format:**
- AT requires plain text starting with `CON ` or `END `
- Never return JSON to AT

**Re-deploy after code changes:**
```bash
gcloud run deploy cnt-ussd --source . --region africa-south1
```
