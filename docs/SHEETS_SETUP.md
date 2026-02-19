# Google Sheets Integration — Setup Guide

## What this does
Every form submission in the app (parish additions, sacrament records,
SCC meetings, catechist registrations, pastoral care entries) is
automatically saved to a dedicated tab in your Google Sheet.

Each `form_type` gets its own tab, auto-created on first submission:
- `parish_submission` — church directory additions
- `sacrament_baptism`, `sacrament_confirmation`, `sacrament_eucharist`,
  `sacrament_marriage`, `sacrament_anointing`, `sacrament_holy_orders`
- `scc_registration`, `scc_meeting`
- `catechist_registration`, `catechist_training`
- `formation_programme`, `formation_participant`
- `pastoral_homebound`, `pastoral_grief`

## One-time setup (~5 minutes)

### Step 1 — Create your Google Sheet
1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new spreadsheet: **"Catholic Parish Steward — Submissions"**

### Step 2 — Deploy the Apps Script
1. In your sheet: **Extensions → Apps Script**
2. Delete the default `myFunction()` code
3. Paste the `doPost()` function (already deployed in your project)
4. Click **Deploy → New deployment**
   - Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Click **Deploy** → copy the web app URL

### Step 3 — Add to Streamlit secrets
1. Go to your Streamlit app → ⋮ menu → **Settings → Secrets**
2. Add this line (paste your URL):
   ```
   SHEETS_ENDPOINT = "https://script.google.com/macros/s/YOUR_ID/exec"
   ```
3. Click **Save** — takes ~1 minute to propagate

### Step 4 — Test it
1. Go to the Parish Directory → Add a Parish → Submit
2. Check your Google Sheet — a new tab `parish_submission` should appear
   with your submission as the first data row

## Notes
- No API keys needed — the Apps Script endpoint is public POST only
- Data flows one-way: app → sheet (not the reverse)
- Submissions also stay in the session as before — sheets is additive
- If SHEETS_ENDPOINT is not set, the app works normally; data just
  doesn't persist between sessions
