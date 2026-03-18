"""Parish Giving — M-Pesa (Kenya/East Africa) + international guidance"""
import streamlit as st

# ── Mobile CSS ──────────────────────────────────────────────────────────────
import sys as _sys
_sys.path.insert(0, ".")
try:
    from services.mobile_ux import inject_mobile_css as _inj; _inj()
except Exception:
    pass

try:
    from services.save_indicator import mark_saved, show_save_status
except Exception:
    def mark_saved(x): pass
    def show_save_status(x, y=None): pass
import sys
sys.path.insert(0, ".")

try:
    from services.mpesa_service import (
        init_giving_db,
        initiate_stk_push,
        get_giving_summary,
        live_activation_checklist,
        MPESA_ENV,
    )
    _MPESA_OK = True
except Exception as _mpesa_err:
    def init_giving_db(): pass
    def initiate_stk_push(*a, **k): return {"success": False, "message": "M-Pesa not configured"}
    def get_giving_summary(sandbox_only=True): return {"total_kes": 0, "transaction_count": 0, "label": "[No data]", "sandbox": sandbox_only}
    def live_activation_checklist(): return []
    MPESA_ENV = "sandbox"
    _MPESA_OK = False

st.set_page_config(page_title="Parish Giving — CNT", page_icon="🤝", layout="centered")

try:
    init_giving_db()
except Exception:
    pass

# ── Location / Currency detection (non-blocking) ──────────────────────────────
if "user_location" not in st.session_state:
    try:
        from services.location_service import detect_location
        st.session_state.user_location = detect_location()
    except Exception:
        st.session_state.user_location = {
            "country": "Kenya", "currency": "KES", "detected": False,
            "mpesa_relevant": True, "is_vpn": False, "city": "Unknown",
        }

loc = st.session_state.user_location

if loc.get("detected"):
    if loc.get("is_vpn"):
        st.caption(f"📍 {loc['city']}, {loc['country']} · Currency: {loc['currency']}")
    else:
        st.caption(f"📍 Detected: {loc['city']}, {loc['country']} · Currency: {loc['currency']}")
    if not loc.get("mpesa_relevant") and st.session_state.get("mpesa_warning_shown") is not True:
        st.info(
            f"ℹ️ You appear to be outside the M-Pesa coverage area ({loc['country']}). "
            "M-Pesa giving is available in Kenya, Tanzania, Ghana, and other Safaricom markets. "
            "International giving options (card, bank transfer) are on our roadmap.",
            icon="🌍",
        )
        st.session_state.mpesa_warning_shown = True


st.title("🤝 Parish Giving")

tab_give, tab_funds = st.tabs(["💳 Give Now", "📊 Fund Transparency"])

with tab_give:

    is_sandbox = MPESA_ENV == "sandbox"
    if is_sandbox:
        st.warning(
            "**M-Pesa Giving is being set up.** You can explore how it works — no real transactions are processed yet.",
            icon="🧪",
        )
    else:
        st.success("**[LIVE MODE]** — Real M-Pesa transactions are enabled.", icon="✅")

    st.divider()

    # ─────────────────────────────────────────────
    # GIVING FORM
    # ─────────────────────────────────────────────
    st.subheader("Make a Contribution")

    giving_purposes = [
        "General Parish Fund",
        "Building & Maintenance",
        "Youth Ministry",
        "Outreach & Charitable Works",
        "AMECEA / Diocesan Levy",
        "Liturgical Supplies",
        "Other",
    ]

    col1, col2 = st.columns(2)
    with col1:
        phone = st.text_input(
            "M-Pesa Phone Number",
            placeholder="2547XXXXXXXX",
            help="Format: 2547XXXXXXXX (no + or spaces)",
        )
        amount = st.number_input(
            "Amount (KES)",
            min_value=10,
            max_value=150000,
            value=100,
            step=50,
        )

    with col2:
        purpose = st.selectbox("Giving purpose", giving_purposes)
        donor_name = st.text_input("Name (optional)", placeholder="For receipt reference")

    description = f"Parish Giving: {purpose}"
    if donor_name:
        description += f" — {donor_name}"

    st.info(
        f"📱 An M-Pesa prompt will appear on **{phone or 'your phone'}** for **KES {amount:,}**.",
        icon="📲",
    )

    if st.button("Send M-Pesa Prompt", type="primary", use_container_width=True):
        if not phone or len(phone) < 10:
            st.warning("Please enter your M-Pesa phone number in the format 2547XXXXXXXX (e.g. 254712345678).")
        else:
            with st.spinner("Sending STK push…"):
                result = initiate_stk_push(
                    phone_number=phone,
                    amount=int(amount),
                    account_ref=purpose[:12].replace(" ", ""),
                    description=description[:50],
                )

            if result["success"]:
                st.success(result["message"])
                if is_sandbox:
                    st.info(
                        "**Test tip:** To simulate a completed payment, log into "
                        "developer.safaricom.co.ke → Simulate → STK Push callback.",
                        icon="💡",
                    )
            else:
                st.warning("The payment request could not be completed. Please try again or contact your parish.")

    st.divider()

    # ─────────────────────────────────────────────
    # GIVING SUMMARY
    # ─────────────────────────────────────────────
    st.subheader("Giving Summary")

    summary = get_giving_summary(sandbox_only=is_sandbox)
    c1, c2 = st.columns(2)
    c1.metric(f"Total Received {summary['label']}", f"KES {summary['total_kes']:,}")
    c2.metric("Transactions", summary["transaction_count"])

    st.divider()

    # ─────────────────────────────────────────────
    # LIVE ACTIVATION GUIDE
    # ─────────────────────────────────────────────
    if is_sandbox:
        with st.expander("📋 Activate Live M-Pesa Giving"):
            checklist = live_activation_checklist()
            st.markdown(f"**Status:** {checklist['status']}")
            st.markdown(f"**Estimated approval time:** {checklist['estimated_time']}")
            for step in checklist["live_requirements"]:
                st.markdown(f"- {step}")
            st.caption(f"Need help? Contact your parish coordinator or see the guide at {checklist['guide']}")

# ══ TRANSPARENCY TAB ════════════════════════════════════════════════════════
with tab_funds:
    st.subheader("Parish Fund Transparency")
    st.caption(
        "Every shilling designated to a purpose, tracked here. "
        "Giving grows where trust grows."
    )

    # Load fund goals from session state (set by coordinator) or show defaults
    if "parish_fund_goals" not in st.session_state:
        st.session_state.parish_fund_goals = [
            {"name": "General Parish Fund",       "goal": 0, "raised": 0, "update": ""},
            {"name": "Building & Maintenance",    "goal": 0, "raised": 0, "update": ""},
            {"name": "Youth Ministry",            "goal": 0, "raised": 0, "update": ""},
            {"name": "Outreach & Charitable Works","goal": 0, "raised": 0, "update": ""},
            {"name": "Liturgical Supplies",       "goal": 0, "raised": 0, "update": ""},
        ]

    funds = st.session_state.parish_fund_goals

    # ── Public view — fund progress ───────────────────────────────────────────
    any_active = any(f["goal"] > 0 or f["raised"] > 0 for f in funds)

    if not any_active:
        st.info(
            "No fund goals set yet. "
            "Parish coordinators can set goals and narrative updates below.",
            icon="📋",
        )
    else:
        for fund in funds:
            goal = fund.get("goal", 0)
            raised = fund.get("raised", 0)
            update = fund.get("update", "")
            if goal == 0 and raised == 0:
                continue
            progress = min(raised / goal, 1.0) if goal > 0 else 0.0
            pct = int(progress * 100)

            with st.container():
                c1, c2 = st.columns([3, 1])
                c1.markdown(f"**{fund['name']}**")
                if update:
                    c1.caption(f"📝 {update}")
                if goal > 0:
                    c2.metric("Progress", f"{pct}%", delta=f"KES {raised:,} of {goal:,}")
                    st.progress(progress)
                else:
                    c2.metric("Raised", f"KES {raised:,}")
                st.divider()

    # ── Coordinator update panel ──────────────────────────────────────────────
    try:
        from services.roles import is_at_least as _ial
        _can_edit = _ial("coordinator")
    except Exception:
        _can_edit = True  # graceful fallback

    if _can_edit:
        with st.expander("🔧 Update Fund Goals & Narratives (Coordinators)", expanded=not any_active):
            for i, fund in enumerate(funds):
                st.markdown(f"**{fund['name']}**")
                c1, c2, c3 = st.columns(3)
                new_goal   = c1.number_input("Goal (KES)", min_value=0, value=int(fund.get("goal", 0)),
                                              step=1000, key=f"fg_{i}_goal")
                new_raised = c2.number_input("Raised (KES)", min_value=0, value=int(fund.get("raised", 0)),
                                              step=500, key=f"fg_{i}_raised")
                new_upd    = c3.text_input("Narrative update", value=fund.get("update", ""),
                                            placeholder="e.g. Roof repairs underway — 60% complete",
                                            key=f"fg_{i}_upd")
                fund["goal"]   = new_goal
                fund["raised"] = new_raised
                fund["update"] = new_upd

            if st.button("💾 Save Fund Updates", type="primary", key="fund_save"):
                try:
                    from services.sheets import _save
                    from datetime import date
                    for fund in funds:
                        _save("parish_fund", {**fund, "updated": str(date.today())})
                    st.success("Fund goals saved to Google Sheets.", icon=None)
                except Exception:
                    st.success("Fund goals updated for this session.", icon=None)
                st.rerun()

    st.caption(
        "Fund data is updated by parish coordinators. "
        "For questions, speak with your parish treasurer or coordinator."
    )
