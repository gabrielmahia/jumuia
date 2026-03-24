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
- `pastoral_homebound`, `pastoral_grief`, `pastoral_visit`, `pastoral_mentorship`, `pastoral_new_member`
- `sacrament_reconciliation`
- `parish_submission`

## One-time setup (~5 minutes)

### Step 1 — Create your Google Sheet
1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new spreadsheet: **"Jumuia — Parish Directory"**

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

## Enabling read-back (optional — allows records to reload after refresh)

To load your saved records back into the app, update your Apps Script to add a `doGet()` function:

```javascript
function doGet(e) {
  var params = e.parameter;
  var sheetName = params.sheet || "submissions";
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    return ContentService.createTextOutput(JSON.stringify({status: "not_found", rows: []}))
      .setMimeType(ContentService.MimeType.JSON);
  }
  var data = sheet.getDataRange().getValues();
  var headers = data[0];
  var rows = data.slice(1).map(function(row) {
    var obj = {};
    headers.forEach(function(h, i) { obj[h] = row[i]; });
    return obj;
  });
  return ContentService.createTextOutput(JSON.stringify({status: "ok", rows: rows}))
    .setMimeType(ContentService.MimeType.JSON);
}
```

After adding `doGet()`:
1. **Deploy → Manage deployments → Edit → New version → Deploy**
2. The app will automatically load your saved records when the page opens

> Note: read-back loads the most recent 200 records per tab to keep page load fast.

## Critical deployment setting
## Critical deployment setting

When deploying the Apps Script web app, set:
- **Execute as:** Me
- **Who has access:** Anyone  ← must be "Anyone", NOT "Anyone with Google account"

Without this, the POST from Streamlit Cloud will receive a 403 and data will not save.

## Verifying the connection

Run this in your browser console or from Cloud Shell to test:

```bash
curl -L -X POST "YOUR_ENDPOINT_URL" \
  -H "Content-Type: application/json" \
  -d '{"form_type":"test","message":"connection check","timestamp":"2026-02-20"}'
```

Expected response: `{"status":"ok"}`
