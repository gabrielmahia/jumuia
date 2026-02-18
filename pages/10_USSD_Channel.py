"""
USSD Channel — Catholic Network Tools
Dial *384*[CHANNEL]# from any Kenyan phone. No internet required.
"""
import streamlit as st
import sys
sys.path.insert(0, ".")

from services.ussd_service import handle_ussd_session, channel_setup_guide

st.set_page_config(page_title="USSD Channel — CNT", page_icon="📞", layout="wide")
st.title("📞 USSD Channel")
st.caption("Works on ANY phone — no smartphone, no internet, no WhatsApp needed.")

st.success(
    "**Why USSD matters:** A parishioner in rural Kenya with a KES 1,500 feature phone "
    "can dial *384*1# and find their nearest parish, check Mass times, and give via M-Pesa "
    "— all without data. This is the most inclusive access channel available.",
    icon="🌍"
)

tab1, tab2, tab3 = st.tabs(["📋 Setup Guide", "🧪 Test Simulator", "📊 Menu Tree"])


# ─────────────────────────────────────────────
# TAB 1 — SETUP GUIDE
# ─────────────────────────────────────────────
with tab1:
    guide = channel_setup_guide()

    st.subheader("Create Your USSD Channel")

    st.info(
        "You're already on the right page in Africa's Talking. "
        "Here's exactly what to fill in:",
        icon="👆"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### What to enter on the AT form")
        st.markdown("""
| Field | Value |
|-------|-------|
| **Service Code** | `*384#` (shared — already selected) |
| **Channel** | `1` (or any number you like) |
| **Callback URL** | Your Render webhook URL |

**Your full dial code will be:** `*384*1#`

> 💡 **Sandbox tip:** For testing, the Callback URL field accepts *any* URL.
> Use your Render webhook URL once deployed, or `https://httpbin.org/post`
> as a placeholder to get the channel created now.
> Then test using the **Launch Simulator** — no real URL needed for sandbox testing.
        """)

    with col2:
        st.markdown("### Step-by-step")
        for step in guide["steps"]:
            st.markdown(f"- {step}")

        st.divider()
        st.markdown("### After channel is created")
        st.markdown("""
1. Click **Launch Simulator** in the AT left sidebar
2. Enter `*384*1#` in the simulator phone
3. Navigate the menus — this is exactly what users experience
4. No real phone or URL needed for sandbox testing
        """)

    st.divider()
    st.subheader("Live Deployment")
    st.markdown("**Callback URL format for your Render service:**")
    st.code("https://cnt-whatsapp-webhook.onrender.com/webhook/ussd", language="text")

    with st.expander("Live vs Sandbox — what changes"):
        st.markdown("""
| | Sandbox | Live |
|--|---------|------|
| Dial code | *384*1# | *384*1# (shared) or dedicated code |
| Real phones | ❌ Simulator only | ✅ Any Kenyan number |
| Cost | Free | Free for shared *384# |
| Callback URL | Any URL works | Must be public HTTPS |
| M-Pesa | Sandbox STK only | Real transactions |

**Good news:** The shared `*384#` code works in production at no extra charge.
You only need a dedicated shortcode if you want a custom number like `*123#`.
        """)


# ─────────────────────────────────────────────
# TAB 2 — LOCAL SIMULATOR
# ─────────────────────────────────────────────
with tab2:
    st.subheader("USSD Simulator — Test Without a Phone")
    st.caption(
        "This replicates exactly what happens when someone dials *384*1#. "
        "Each button press sends the cumulative input to the handler."
    )

    if "ussd_text" not in st.session_state:
        st.session_state.ussd_text = ""
    if "ussd_history" not in st.session_state:
        st.session_state.ussd_history = []
    if "ussd_ended" not in st.session_state:
        st.session_state.ussd_ended = False

    # Simulate phone display
    current_response = handle_ussd_session(
        session_id="simulator-001",
        service_code="*384*1#",
        phone_number="+254700000000",
        text=st.session_state.ussd_text,
    )

    is_end = current_response.startswith("END")
    display_text = current_response[4:] if current_response.startswith(("CON ", "END ")) else current_response

    # Phone screen mockup
    st.markdown("**Phone screen:**")
    screen_style = "background:#1a1a1a;color:#00ff00;padding:16px;border-radius:8px;font-family:monospace;min-height:120px;white-space:pre-wrap"
    st.markdown(
        f'<div style="{screen_style}">{display_text}</div>',
        unsafe_allow_html=True
    )

    if is_end:
        st.info("Session ended. Press Reset to start again.")
        if st.button("🔄 Reset Session"):
            st.session_state.ussd_text = ""
            st.session_state.ussd_history = []
            st.rerun()
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            keypress = st.text_input(
                "Enter your response",
                placeholder="e.g. 1 or Nairobi or 500",
                key="ussd_input",
            )
        with col2:
            st.write("")
            st.write("")
            send = st.button("Send ▶", type="primary", use_container_width=True)

        if send and keypress.strip():
            if st.session_state.ussd_text == "":
                st.session_state.ussd_text = keypress.strip()
            else:
                st.session_state.ussd_text += f"*{keypress.strip()}"
            st.session_state.ussd_history.append(keypress.strip())
            st.rerun()

        col3, col4 = st.columns(2)
        with col3:
            if st.button("⬅ Back"):
                parts = st.session_state.ussd_text.rsplit("*", 1)
                st.session_state.ussd_text = parts[0] if len(parts) > 1 else ""
                st.rerun()
        with col4:
            if st.button("🔄 Reset"):
                st.session_state.ussd_text = ""
                st.session_state.ussd_history = []
                st.rerun()

    if st.session_state.ussd_text:
        st.caption(f"Cumulative input: `{st.session_state.ussd_text}`")


# ─────────────────────────────────────────────
# TAB 3 — MENU TREE
# ─────────────────────────────────────────────
with tab3:
    st.subheader("USSD Menu Structure")
    st.markdown("""
```
*384*1#  → Main Menu
│
├── 1. Find Parish
│   └── [Type city name] → Lists nearest 3 parishes with phone numbers
│
├── 2. Mass Times (Nairobi)
│   └── END — Shows Holy Family, St Paul's, Christ the King times
│
├── 3. Give via M-Pesa
│   └── [Type amount in KES] → Triggers M-Pesa STK Push to caller's number
│
├── 4. Today's Reading
│   └── END — Liturgical reading reference for today's day of week
│
└── 5. Emergency Contacts
    └── END — Parish office and diocese phone numbers
```

**Design principles:**
- Every path resolves in ≤ 2 keypresses (AT sessions time out at 3 minutes)
- No screen exceeds 160 characters (feature phone display limit)
- M-Pesa giving directly from USSD — no app, no browser needed
- Parish search uses the same SQLite directory as the web app
    """)

    st.divider()
    st.markdown("**Expanding the menu:**")
    st.markdown("""
    To add more options, edit `services/ussd_service.py`:
    - Add a new `elif choice == "6":` block
    - Keep responses under 160 chars
    - Use `end()` for final responses, `con()` for navigation screens
    - Test immediately in the simulator tab above
    """)
