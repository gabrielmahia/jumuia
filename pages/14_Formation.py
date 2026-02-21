"""Formation & Spiritual Education — Programmes, enrolment, curriculum, progress tracking."""

import streamlit as st
try:
    from services.save_indicator import show_save_status, trust_banner
except Exception:
    def show_save_status(x, y=None): pass
    def trust_banner(x=""): pass
from datetime import date

st.set_page_config(page_title="Formation", page_icon="🎓", layout="wide")
try:
    from services.roles import require_role as _require_role
    _require_role("catechist", "Formation & RCIA")
except Exception:
    pass

st.title("🎓 Formation & Spiritual Education")
st.caption("RCIA · Adult faith · Youth · Bible study · Retreats · Vocations")

try:
    trust_banner("formation")
except Exception:
    pass

# ── Session state ─────────────────────────────────────────────────────────────
if "formation_programmes" not in st.session_state:
    try:
        from services.sheets import fetch as _fetch_sheets
        _saved = _fetch_sheets("formation_programme")
        st.session_state.formation_programmes = _saved if _saved else []
    except Exception:
        st.session_state.formation_programmes = []

if "formation_participants" not in st.session_state:
    try:
        from services.sheets import fetch as _fetch_sheets
        _saved = _fetch_sheets("formation_participant")
        st.session_state.formation_participants = _saved if _saved else []
    except Exception:
        st.session_state.formation_participants = []

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["📋 Programmes", "👤 Participants", "📅 Schedule", "📊 Progress"]
)

PROGRAMME_TYPES = [
    "RCIA (Rite of Christian Initiation)",
    "Adult Faith Formation",
    "Youth Catechesis (12–17)",
    "Children's Catechesis (7–11)",
    "First Communion Preparation",
    "Confirmation Preparation",
    "Marriage Preparation (Pre-Cana)",
    "Bible Study",
    "Retreat / Recollection",
    "RENEW / Small Faith Group",
    "Leadership Formation",
    "Diaconate Preparation",
    "Other",
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
STATUS_OPTIONS = ["Active", "Completed", "Paused", "Planned"]

# ══ TAB 1: PROGRAMMES ════════════════════════════════════════════════════════
with tab1:
    st.subheader("Formation Programmes")

    progs = st.session_state.formation_programmes
    if progs:
        import pandas as pd
        df = pd.DataFrame(progs)
        show_cols = [c for c in ["name", "type", "facilitator", "start_date", "status", "enrolled"] if c in df.columns]
        st.dataframe(df[show_cols] if show_cols else df, use_container_width=True, hide_index=True)
    else:
        st.info("No programmes yet. Add one below.", icon="📋")

    with st.expander("➕ Add a Formation Programme", expanded=not progs):
        with st.form("formation_prog_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            prog_name      = c1.text_input("Programme Name *", placeholder="RCIA 2026 · Youth Confirmation")
            prog_type      = c1.selectbox("Type", PROGRAMME_TYPES)
            facilitator    = c1.text_input("Facilitator / Catechist", placeholder="Name")
            start_date     = c1.date_input("Start Date", value=date.today())
            end_date       = c2.date_input("End Date (approx.)")
            meeting_day    = c2.selectbox("Meeting Day", DAYS)
            meeting_time   = c2.text_input("Meeting Time", placeholder="6:30 PM")
            location       = c2.text_input("Location", placeholder="Parish hall · Room 3")
            capacity       = c2.number_input("Max participants", 1, 200, 20)
            prog_status    = c2.selectbox("Status", STATUS_OPTIONS)
            description    = st.text_area("Description / Notes", height=70,
                placeholder="Curriculum overview, prerequisites, materials needed…")
            if st.form_submit_button("Save Programme", type="primary"):
                if not prog_name.strip():
                    st.warning("Programme name is required.")
                else:
                    record = {
                        "name": prog_name.strip(), "type": prog_type,
                        "facilitator": facilitator, "start_date": str(start_date),
                        "end_date": str(end_date), "meeting_day": meeting_day,
                        "meeting_time": meeting_time, "location": location,
                        "capacity": capacity, "status": prog_status,
                        "description": description, "enrolled": 0,
                        "added": str(date.today()),
                    }
                    st.session_state.formation_programmes.append(record)
                    try:
                        from services.sheets import _save
                        _ok = _save("formation_programme", record)
                        show_save_status("formation_programme", _ok)
                    except Exception:
                        pass
                    st.success(f"✅ **{prog_name.strip()}** added.")
                    st.rerun()

# ══ TAB 2: PARTICIPANTS ═══════════════════════════════════════════════════════
with tab2:
    st.subheader("Participant Enrolment")

    participants = st.session_state.formation_participants
    if participants:
        import pandas as pd
        df = pd.DataFrame(participants)
        show_cols = [c for c in ["name", "programme", "status", "contact", "enrolled_date"] if c in df.columns]
        st.dataframe(df[show_cols] if show_cols else df, use_container_width=True, hide_index=True)
    else:
        st.info("No participants enrolled yet. Enrol one below.", icon="👤")

    prog_names = [p["name"] for p in st.session_state.formation_programmes] or ["(No programmes yet)"]

    with st.expander("➕ Enrol a Participant", expanded=not participants):
        with st.form("formation_participant_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            p_name         = c1.text_input("Full Name *", placeholder="Jane Mwangi")
            p_programme    = c1.selectbox("Programme", prog_names)
            p_contact      = c1.text_input("Phone / Email", placeholder="+254 7…")
            p_dob          = c1.date_input("Date of Birth (optional)", value=None)
            p_sponsor      = c2.text_input("Sponsor / Godparent", placeholder="For RCIA/Confirmation")
            p_baptized     = c2.selectbox("Baptised?", ["Yes", "No", "Unknown"])
            p_status       = c2.selectbox("Status", ["Active", "Completed", "Withdrawn", "On hold"])
            p_notes        = st.text_area("Notes", height=60, placeholder="Accessibility needs, special circumstances…")
            if st.form_submit_button("Enrol Participant", type="primary"):
                if not p_name.strip():
                    st.warning("Name is required.")
                else:
                    record = {
                        "name": p_name.strip(), "programme": p_programme,
                        "contact": p_contact,
                        "dob": str(p_dob) if p_dob else "",
                        "sponsor": p_sponsor, "baptized": p_baptized,
                        "status": p_status, "notes": p_notes,
                        "enrolled_date": str(date.today()),
                    }
                    st.session_state.formation_participants.append(record)
                    # Update enrolled count on parent programme
                    for prog in st.session_state.formation_programmes:
                        if prog["name"] == p_programme:
                            prog["enrolled"] = prog.get("enrolled", 0) + 1
                    try:
                        from services.sheets import _save
                        _ok = _save("formation_participant", record)
                        show_save_status("formation_participant", _ok)
                    except Exception:
                        pass
                    st.success(f"✅ **{p_name.strip()}** enrolled in {p_programme}.")
                    st.rerun()

# ══ TAB 3: SCHEDULE ══════════════════════════════════════════════════════════
with tab3:
    st.subheader("Programme Schedule")
    progs = st.session_state.formation_programmes
    if not progs:
        st.info("Add programmes in the Programmes tab to see the schedule.", icon="📅")
    else:
        for prog in progs:
            status_icon = {"Active": "🟢", "Completed": "✅", "Paused": "🟡", "Planned": "🔵"}.get(prog.get("status",""), "⚪")
            enrolled = prog.get("enrolled", 0)
            capacity = prog.get("capacity", "?")
            with st.container():
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                c1.markdown(f"**{prog['name']}** — {prog.get('type','')}")
                c1.caption(f"📅 {prog.get('meeting_day','')} {prog.get('meeting_time','')} · 📍 {prog.get('location','')}")
                c2.markdown(f"{status_icon} {prog.get('status','')}")
                c3.metric("Enrolled", f"{enrolled}/{capacity}")
                c4.markdown(f"👤 {prog.get('facilitator','—')}")
                st.divider()

# ══ TAB 4: PROGRESS ══════════════════════════════════════════════════════════
with tab4:
    st.subheader("Formation Overview")
    progs = st.session_state.formation_programmes
    participants = st.session_state.formation_participants

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Programmes", len(progs))
    c2.metric("Total Enrolled", len(participants))
    c3.metric("Active Programmes", sum(1 for p in progs if p.get("status") == "Active"))
    c4.metric("Completed", sum(1 for p in participants if p.get("status") == "Completed"))

    if participants:
        import pandas as pd
        st.markdown("**Status breakdown**")
        by_status = {}
        for part in participants:
            s = part.get("status", "Unknown")
            by_status[s] = by_status.get(s, 0) + 1
        status_df = pd.DataFrame(list(by_status.items()), columns=["Status", "Count"])
        st.dataframe(status_df, use_container_width=True, hide_index=True)

    if progs and participants:
        st.markdown("**Enrolment by programme**")
        by_prog = {}
        for part in participants:
            prog = part.get("programme", "Unknown")
            by_prog[prog] = by_prog.get(prog, 0) + 1
        prog_df = pd.DataFrame(list(by_prog.items()), columns=["Programme", "Participants"])
        st.dataframe(prog_df, use_container_width=True, hide_index=True)

st.divider()
st.caption("💾 Records are stored for this session. Connect Google Sheets in Admin → Data Management for persistence.")
