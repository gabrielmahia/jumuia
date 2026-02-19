"""
USSD Service — Catholic Network Tools
======================================
Dial: *384*[CHANNEL]# (Africa's Talking sandbox)
      e.g. *384*1# if your channel number is 1

WHY USSD MATTERS HERE:
  - Works on ANY phone — no smartphone, no internet, no WhatsApp needed
  - Perfect for rural Kenyan parishioners with basic Safaricom feature phones
  - Sessions are stateful — user navigates a menu by pressing numbers
  - Response must arrive in < 5 seconds and be < 182 characters per screen

ARCHITECTURE:
  AT calls your webhook with each keypress.
  You return "CON <text>" to continue the session (show next menu)
  You return "END <text>" to close the session (final response)

MENU TREE:
  *384*1#
  └── 1. Find Parish
  │   └── [Enter city name] → top 3 parishes listed
  ├── 2. Mass Times (Nairobi)
  │   └── Lists Holy Family, St Paul's, Christ the King times
  ├── 3. Give (M-Pesa)
  │   └── [Enter amount] → STK push sent to their number
  ├── 4. Daily Reading
  │   └── Today's liturgical reading reference
  └── 5. Emergency Contacts
      └── Parish office numbers

CALLBACK FORMAT (Africa's Talking sends this to your webhook):
  sessionId   — unique per session
  serviceCode — *384*1#
  phoneNumber — +254XXXXXXXXX
  text        — cumulative keypresses e.g. "" / "1" / "1*Nairobi"
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# USSD RESPONSE HELPERS
# ─────────────────────────────────────────────

def con(text: str) -> str:
    """Continue session — user can respond."""
    return f"CON {text[:180]}"  # AT hard limit


def end(text: str) -> str:
    """End session — final message, no response needed."""
    return f"END {text[:180]}"


# ─────────────────────────────────────────────
# MENU SCREENS (keep each under 160 chars for readability on small screens)
# ─────────────────────────────────────────────

MAIN_MENU = """Parish Steward
1. Find Parish
2. Mass Times
3. Give via M-Pesa
4. Today's Reading
5. Emergency Contacts
6. Kiswahili"""

MAIN_MENU_SW = """Mwenyekiti wa Parokia
1. Tafuta Kanisa
2. Ratiba ya Misa
3. Toa kwa M-Pesa
4. Somo la Leo
5. Namba za Dharura
6. English"""

FIND_PARISH_PROMPT = "Enter your city or town:\n(e.g. Nairobi, Nakuru, Kisumu)"

MASS_TIMES_NAIROBI = """Nairobi Mass Times:
Holy Family: 7am 9am 11am 6pm
St Paul's: 8am 10am
Christ the King: 7am 9am 11am
All: Sunday"""

# Readings now served from lectionary service (real cycle-aware)
def _get_reading_text() -> str:
    try:
        from services.lectionary import ussd_reading
        return ussd_reading()
    except Exception:
        from datetime import date
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        return f"{days[date.today().weekday()]} reading\nSee: usccb.org/bible/readings"

EMERGENCY_CONTACTS = """Parish Emergency:
Holy Family: 0202228959
Diocese Nairobi: 0722205176
Caritas Kenya: 0202714188
Reply 0 for main menu"""


# ─────────────────────────────────────────────
# PARISH SEARCH (lightweight, no Claude API needed for USSD)
# ─────────────────────────────────────────────

def _search_parish_ussd(city: str) -> str:
    """Search parishes via OSM Nominatim — no local DB needed."""
    import urllib.request, urllib.parse, json as _json
    try:
        q = urllib.parse.quote(f"Catholic church {city}")
        url = (f"https://nominatim.openstreetmap.org/search"
               f"?q={q}&format=json&limit=3&addressdetails=0")
        req = urllib.request.Request(
            url, headers={"User-Agent": "CatholicParishSteward/1.0"}
        )
        with urllib.request.urlopen(req, timeout=4) as r:
            results = _json.loads(r.read())
        if not results:
            return end(f"No parishes found near {city}.\nTry: Nairobi, Nakuru, Kisumu")
        lines = [f"Churches near {city[:15]}:"]
        for item in results[:3]:
            name = item.get("display_name","Church").split(",")[0][:22]
            lines.append(name)
        return end("\n".join(lines[:4]))  # keep under 182 chars
    except Exception as e:
        logger.error("USSD parish search error: %s", e)
        return end(f"Search unavailable.\nVisit catholicparishsteward.streamlit.app")


# ─────────────────────────────────────────────
# M-PESA GIVING VIA USSD
# ─────────────────────────────────────────────

def _initiate_ussd_giving(phone: str, amount_str: str) -> str:
    """Trigger M-Pesa STK push from USSD session."""
    try:
        amount = int(amount_str.strip())
        if amount < 10:
            return end("Minimum giving amount is KES 10.")
        if amount > 150000:
            return end("Maximum single giving is KES 150,000.")

        from services.mpesa_service import initiate_stk_push
        result = initiate_stk_push(
            phone_number=phone.lstrip("+"),
            amount=amount,
            account_ref="USSDGiving",
            description=f"Parish Giving KES {amount}",
        )
        if result["success"]:
            env = "[SANDBOX] " if result.get("sandbox") else ""
            return end(f"{env}M-Pesa prompt sent!\nCheck your phone for KES {amount} request.\nThank you. God bless you.")
        else:
            return end("Giving failed. Please try via the Streamlit app or visit your parish.")
    except ValueError:
        return end("Invalid amount. Please enter numbers only e.g. 500")
    except Exception as e:
        logger.error("USSD giving error: %s", e)
        return end("Service temporarily unavailable. Try again later.")


# ─────────────────────────────────────────────
# MAIN SESSION HANDLER
# ─────────────────────────────────────────────

def handle_ussd_session(
    session_id: str,
    service_code: str,
    phone_number: str,
    text: str,
) -> str:
    """
    Main USSD session handler.
    Called by your FastAPI webhook on every keypress.

    text is the CUMULATIVE input so far, separated by *.
    e.g. "" → main menu
         "1" → Find Parish
         "1*Nairobi" → search parishes in Nairobi
         "3" → Give menu
         "3*500" → trigger STK push for KES 500

    Returns: "CON <screen>" or "END <message>"
    """
    logger.info("USSD session=%s phone=%s text='%s'", session_id, phone_number, text)

    # Parse cumulative input into navigation steps
    parts = text.split("*") if text else [""]

    # ── ROOT ──────────────────────────────────
    if text == "":
        return con(MAIN_MENU)

    choice = parts[0]

    # ── 1. FIND PARISH ────────────────────────
    if choice == "1":
        if len(parts) == 1:
            return con(FIND_PARISH_PROMPT)
        city = "*".join(parts[1:])  # handle city names with spaces/stars
        if not city.strip():
            return con(FIND_PARISH_PROMPT)
        return _search_parish_ussd(city.strip())

    # ── 2. MASS TIMES ─────────────────────────
    elif choice == "2":
        return end(MASS_TIMES_NAIROBI)

    # ── 3. M-PESA GIVING ─────────────────────
    elif choice == "3":
        if len(parts) == 1:
            return con("Parish Giving\nEnter amount in KES:\n(e.g. 100, 500, 1000)\nMinimum: KES 10")
        amount_input = parts[1]
        if not amount_input.strip():
            return con("Enter giving amount (KES):\nMin KES 10, Max KES 150,000")
        return _initiate_ussd_giving(phone_number, amount_input)

    # ── 4. DAILY READING ──────────────────────
    elif choice == "4":
        reading = _get_reading_text()
        msg = f"Today's Reading\n{reading}\n\nFull: usccb.org/readings"
        return end(msg[:178])

    # ── 5. EMERGENCY CONTACTS ─────────────────
    elif choice == "5":
        return end(EMERGENCY_CONTACTS)

    # ── 6. KISWAHILI ──────────────────────────
    elif choice == "6":
        if len(parts) == 1:
            return con(MAIN_MENU_SW)
        # Kiswahili submenus: text is "6*1", "6*2" etc
        sw_choice = parts[1]
        if sw_choice == "1":
            return con("Ingiza mji wako:\n(mfano: Nairobi, Nakuru, Kisumu)")
        elif sw_choice == "2":
            return end("Ratiba ya Misa Nairobi:\nHoly Family: 7am 9am 11am 6pm\nSt Paul's: 8am 10am\nKristo Mfalme: 7am 9am 11am\nJumapili zote")
        elif sw_choice == "4":
            reading = _get_reading_text()
            return end(f"Somo la Leo\n{reading}\n\nZaidi: usccb.org/readings")[:178]
        elif sw_choice == "5":
            return end("Dharura ya Parokia:\nHoly Family: 0202228959\nDiocesi Nairobi: 0722205176\nCaritas Kenya: 0202714188\nJibu 0 kwa menyu kuu")
        elif sw_choice == "6":
            return con(MAIN_MENU)
        else:
            return con(f"Chaguo batili.\n{MAIN_MENU_SW}")

    # ── INVALID INPUT ─────────────────────────
    else:
        return con(f"Invalid option '{choice}'.\n{MAIN_MENU}")


# ─────────────────────────────────────────────
# SESSION LOGGING (SQLite)
# ─────────────────────────────────────────────

def log_ussd_session(
    session_id: str,
    phone: str,
    text: str,
    response: str,
) -> None:
    """Log USSD interactions for analytics."""
    try:
        import sqlite3
        from pathlib import Path
        db_path = Path(os.getenv("CNT_DB_PATH", "data/parishes.db"))
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ussd_sessions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT,
                phone       TEXT,
                input       TEXT,
                response    TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute(
            "INSERT INTO ussd_sessions (session_id, phone, input, response) VALUES (?,?,?,?)",
            (session_id, phone, text, response[:100])
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning("USSD log error: %s", e)


# ─────────────────────────────────────────────
# CHANNEL SETUP INFO
# ─────────────────────────────────────────────

def channel_setup_guide() -> dict:
    """Returns setup info for display on the admin page."""
    return {
        "sandbox_dial_code": "*384*[CHANNEL]#",
        "steps": [
            "1. Go to account.africastalking.com → USSD → Create Channel",
            "2. Pick shared service code: *384#",
            "3. Channel number: choose any (e.g. 1). Your code becomes *384*1#",
            "4. Callback URL: your FastAPI endpoint /webhook/ussd",
            "   Sandbox tip: use Launch Simulator — no real URL needed for testing",
            "5. Click 'Create Channel'",
            "6. Go to Launch Simulator → enter *384*1# → test your menus",
        ],
        "callback_endpoint": "/webhook/ussd",
        "sandbox_simulator": "account.africastalking.com → Launch Simulator",
        "live_requirements": [
            "Apply for dedicated shortcode at africastalking.com/ussd",
            "OR use shared *384# code in production (same as sandbox)",
            "Shared code is free — dedicated code has monthly fee",
        ],
    }
