/**
 * Jumuia — Parish Community · Google Sheets Backend
 * ==================================================
 * Version: 1.0
 *
 * WHAT THIS DOES:
 *   Receives JSON form submissions from the Jumuia Streamlit app
 *   and routes them to dedicated tabs in this spreadsheet.
 *   Each form_type gets its own tab, auto-created on first submission.
 *
 * ONE-TIME SETUP:
 *   1. Open this Sheet → Extensions → Apps Script
 *   2. Paste this entire file, replacing any existing code
 *   3. Click Deploy → New deployment
 *        Type: Web app
 *        Execute as: Me
 *        Who has access: Anyone   ← MUST be "Anyone", not "Anyone with Google account"
 *   4. Click Deploy → Authorize → Copy the web app URL
 *   5. In Streamlit Cloud → your app → Settings → Secrets, add:
 *        SHEETS_ENDPOINT = "https://script.google.com/macros/s/YOUR_ID/exec"
 *   6. Done. Submissions land here automatically.
 *
 * TABS CREATED AUTOMATICALLY (on first submission of each type):
 *   parish_submission      — church directory additions from Find a Church
 *   sacrament_baptism      — baptism records
 *   sacrament_confirmation — confirmation records
 *   sacrament_marriage     — marriage records
 *   sacrament_anointing    — anointing of the sick
 *   sacrament_eucharist    — first communion records
 *   sacrament_holy_orders  — ordination records
 *   sacrament_reconciliation — reconciliation records
 *   scc_registration       — Small Christian Community registrations
 *   scc_meeting            — SCC meeting records
 *   catechist_registration — catechist sign-ups
 *   catechist_training     — training session records
 *   pastoral_homebound     — homebound ministry records
 *   pastoral_grief         — grief ministry records
 *   pastoral_new_member    — new parishioner welcome records
 *   pastoral_visit         — pastoral visit logs
 *   pastoral_mentorship    — mentorship matches
 *   formation_programme    — formation programme records
 *   formation_participant  — formation participant records
 *   feedback               — general feedback
 */

// ── doPost — receives form submissions ──────────────────────────────────────
function doPost(e) {
  try {
    var payload = JSON.parse(e.postData.contents);
    var formType = payload.form_type || "submissions";
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = _getOrCreateSheet(ss, formType);

    // Build row from payload keys (consistent column order)
    var headers = _ensureHeaders(sheet, payload);
    var row = headers.map(function(h) {
      var val = payload[h];
      if (val === undefined || val === null) return "";
      if (typeof val === "object") return JSON.stringify(val);
      return val;
    });

    sheet.appendRow(row);

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok", tab: formType }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ── doGet — read back rows for a given tab ───────────────────────────────────
function doGet(e) {
  try {
    var params = e.parameter || {};
    var sheetName = params.sheet || "submissions";
    var maxRows   = parseInt(params.max_rows || "200", 10);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(sheetName);

    if (!sheet) {
      return ContentService
        .createTextOutput(JSON.stringify({ status: "not_found", rows: [], sheet: sheetName }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    var data = sheet.getDataRange().getValues();
    if (data.length < 2) {
      return ContentService
        .createTextOutput(JSON.stringify({ status: "ok", rows: [], sheet: sheetName }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    var headers = data[0];
    var rows = data.slice(1).slice(-maxRows).map(function(row) {
      var obj = {};
      headers.forEach(function(h, i) {
        obj[h] = row[i] !== undefined ? row[i] : "";
      });
      return obj;
    });

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok", rows: rows, sheet: sheetName, count: rows.length }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function _getOrCreateSheet(ss, name) {
  var sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
  }
  return sheet;
}

function _ensureHeaders(sheet, payload) {
  var lastCol = sheet.getLastColumn();
  var existingHeaders = lastCol > 0
    ? sheet.getRange(1, 1, 1, lastCol).getValues()[0]
    : [];

  // Add any new keys from this payload as new header columns
  var newKeys = Object.keys(payload).filter(function(k) {
    return existingHeaders.indexOf(k) === -1;
  });

  if (newKeys.length > 0) {
    var startCol = existingHeaders.length + 1;
    newKeys.forEach(function(k, i) {
      sheet.getRange(1, startCol + i).setValue(k);
    });
    existingHeaders = existingHeaders.concat(newKeys);
  }

  return existingHeaders;
}

// ── Optional: test function ───────────────────────────────────────────────────
// Run this once from the Apps Script editor to verify everything works.
function testDoPost() {
  var mockEvent = {
    postData: {
      contents: JSON.stringify({
        form_type: "test_connection",
        message: "Jumuia connection test",
        timestamp: new Date().toISOString(),
        parish: "Test Parish, Nairobi"
      })
    }
  };
  var result = doPost(mockEvent);
  Logger.log(result.getContent());
}
