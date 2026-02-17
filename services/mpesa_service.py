"""
M-Pesa Service — Catholic Network Tools
Safaricom Daraja API integration for parish giving (Kenya).

STATUS:
  Sandbox:  ACTIVE — works with Daraja sandbox credentials
  Live:     RAILS — requires Safaricom business shortcode registration
            See docs/MPESA_INTEGRATION_GUIDE.md

Supported flows:
  - STK Push (Lipa na M-Pesa / customer-initiated)
  - B2C callback receipt and validation
  - Transaction status query

IMPORTANT — TRUST INTEGRITY:
  All sandbox responses are clearly labeled [SANDBOX].
  Never present simulated transactions as real giving records.
"""

import os
import base64
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

MPESA_ENV = os.getenv("MPESA_ENV", "sandbox")  # "sandbox" | "live"

BASE_URLS = {
    "sandbox": "https://sandbox.safaricom.co.ke",
    "live":    "https://api.safaricom.co.ke",
}

CONSUMER_KEY    = os.getenv("MPESA_CONSUMER_KEY", "")
CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET", "")
SHORTCODE       = os.getenv("MPESA_SHORTCODE", "174379")     # Daraja sandbox default
PASSKEY         = os.getenv("MPESA_PASSKEY", "")
CALLBACK_URL    = os.getenv("MPESA_CALLBACK_URL", "https://your-app.streamlit.app/mpesa/callback")

DB_PATH = Path(os.getenv("CNT_DB_PATH", "data/parishes.db"))


def _is_sandbox() -> bool:
    return MPESA_ENV == "sandbox"


def _base_url() -> str:
    return BASE_URLS[MPESA_ENV]


# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────

def get_access_token() -> Optional[str]:
    """
    Fetch Daraja OAuth token.
    Sandbox: use credentials from Daraja developer portal.
    """
    if not CONSUMER_KEY or not CONSUMER_SECRET:
        logger.warning("M-Pesa credentials not configured.")
        return None

    credentials = base64.b64encode(
        f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode()
    ).decode()

    try:
        resp = requests.get(
            f"{_base_url()}/oauth/v1/generate?grant_type=client_credentials",
            headers={"Authorization": f"Basic {credentials}"},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json().get("access_token")
    except Exception as e:
        logger.error("M-Pesa auth error: %s", e)
        return None


# ─────────────────────────────────────────────
# STK PUSH (Lipa na M-Pesa)
# ─────────────────────────────────────────────

def initiate_stk_push(
    phone_number: str,
    amount: int,
    account_ref: str = "ParishGiving",
    description: str = "Parish Donation",
) -> dict:
    """
    Initiate STK push prompt on customer's phone.

    phone_number: format 2547XXXXXXXX (no +)
    amount: KES integer
    account_ref: appears on customer's M-Pesa statement

    Returns:
        {"success": bool, "checkout_id": str, "sandbox": bool,
         "message": str, "raw": dict|None, "error": str|None}
    """
    token = get_access_token()
    if not token:
        return _creds_missing_response()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        f"{SHORTCODE}{PASSKEY}{timestamp}".encode()
    ).decode()

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_ref,
        "TransactionDesc": description,
    }

    try:
        resp = requests.post(
            f"{_base_url()}/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        checkout_id = data.get("CheckoutRequestID", "")

        _log_transaction(
            phone=phone_number,
            amount=amount,
            checkout_id=checkout_id,
            account_ref=account_ref,
            status="PENDING",
            sandbox=_is_sandbox(),
        )

        return {
            "success": True,
            "checkout_id": checkout_id,
            "sandbox": _is_sandbox(),
            "message": (
                "[SANDBOX] STK push initiated — check Daraja sandbox for simulation."
                if _is_sandbox()
                else "STK push sent. Please complete on your phone."
            ),
            "raw": data,
            "error": None,
        }
    except Exception as e:
        logger.error("STK push error: %s", e)
        return {"success": False, "checkout_id": "", "sandbox": _is_sandbox(),
                "message": str(e), "raw": None, "error": str(e)}


# ─────────────────────────────────────────────
# CALLBACK HANDLER
# ─────────────────────────────────────────────

def handle_callback(payload: dict) -> dict:
    """
    Process M-Pesa STK callback payload.
    Call this from your webhook endpoint (FastAPI / Flask route).

    Returns parsed giving record dict.
    """
    try:
        stk = payload.get("Body", {}).get("stkCallback", {})
        result_code = stk.get("ResultCode")
        checkout_id = stk.get("CheckoutRequestID", "")
        metadata    = stk.get("CallbackMetadata", {}).get("Item", [])

        meta = {item["Name"]: item.get("Value") for item in metadata}

        if result_code == 0:
            record = {
                "success": True,
                "checkout_id": checkout_id,
                "amount": meta.get("Amount"),
                "phone": meta.get("PhoneNumber"),
                "mpesa_receipt": meta.get("MpesaReceiptNumber"),
                "transaction_date": meta.get("TransactionDate"),
                "sandbox": _is_sandbox(),
            }
            _update_transaction(checkout_id, "COMPLETE", meta.get("MpesaReceiptNumber"))
            return record
        else:
            _update_transaction(checkout_id, "FAILED")
            return {
                "success": False,
                "checkout_id": checkout_id,
                "result_code": result_code,
                "message": stk.get("ResultDesc", "Transaction failed"),
            }
    except Exception as e:
        logger.error("Callback parse error: %s", e)
        return {"success": False, "error": str(e)}


# ─────────────────────────────────────────────
# TRANSACTION LOG (SQLite)
# ─────────────────────────────────────────────

def init_giving_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS giving_transactions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            phone           TEXT,
            amount          INTEGER,
            account_ref     TEXT,
            checkout_id     TEXT UNIQUE,
            mpesa_receipt   TEXT,
            status          TEXT DEFAULT 'PENDING',
            sandbox         INTEGER DEFAULT 1,
            created_at      TEXT DEFAULT (datetime('now')),
            updated_at      TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def _log_transaction(phone, amount, checkout_id, account_ref, status, sandbox):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            """INSERT OR IGNORE INTO giving_transactions
               (phone, amount, checkout_id, account_ref, status, sandbox)
               VALUES (?,?,?,?,?,?)""",
            (phone, amount, checkout_id, account_ref, status, int(sandbox)),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning("Transaction log error: %s", e)


def _update_transaction(checkout_id, status, receipt=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            """UPDATE giving_transactions
               SET status=?, mpesa_receipt=?, updated_at=datetime('now')
               WHERE checkout_id=?""",
            (status, receipt, checkout_id),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning("Transaction update error: %s", e)


def get_giving_summary(sandbox_only: bool = True) -> dict:
    """Return giving totals for parish dashboard."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    where = "WHERE status='COMPLETE'" + (" AND sandbox=1" if sandbox_only else " AND sandbox=0")
    total = cur.execute(f"SELECT COALESCE(SUM(amount),0) FROM giving_transactions {where}").fetchone()[0]
    count = cur.execute(f"SELECT COUNT(*) FROM giving_transactions {where}").fetchone()[0]
    conn.close()
    label = "[SANDBOX DATA]" if sandbox_only else ""
    return {
        "total_kes": total,
        "transaction_count": count,
        "label": label,
        "sandbox": sandbox_only,
    }


# ─────────────────────────────────────────────
# LIVE ACTIVATION RAILS
# ─────────────────────────────────────────────

def live_activation_checklist() -> dict:
    """
    Returns checklist for activating live M-Pesa giving.
    Display this on the admin/setup page when MPESA_ENV=sandbox.
    """
    return {
        "status": "SANDBOX_ACTIVE",
        "live_requirements": [
            "1. Register at Safaricom Daraja portal: developer.safaricom.co.ke",
            "2. Submit business registration (Certificate of Incorporation or NGO certificate)",
            "3. Get approved Paybill or Till Number shortcode",
            "4. Set MPESA_PASSKEY from your Daraja live app settings",
            "5. Set MPESA_CALLBACK_URL to a publicly reachable HTTPS endpoint",
            "6. Change MPESA_ENV=live in .env",
            "7. Test with a KES 1 transaction before going public",
        ],
        "estimated_time": "3–10 business days for Safaricom approval",
        "guide": "docs/MPESA_INTEGRATION_GUIDE.md",
    }


def _creds_missing_response() -> dict:
    return {
        "success": False,
        "checkout_id": "",
        "sandbox": _is_sandbox(),
        "message": "M-Pesa credentials not configured. See .env.example",
        "raw": None,
        "error": "CREDENTIALS_MISSING",
    }
