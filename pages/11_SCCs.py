"""Small Christian Communities (SCCs) — Register, meetings, formation, coordination."""

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

st.set_page_config(page_title="SCCs — Catholic Network Tools", page_icon="👥", layout="wide")
try:
    from services.roles import require_role as _require_role
except ImportError:
    def _require_role(r, p=""): pass
_require_role("catechist", "Small Christian Communities")


# ── Data notice ───────────────────────────────────────────────────────────────
st.caption(
    "ℹ️ **Session only** — Meeting records are saved during this session. "
    "For permanent records, set up the Google Sheets backend "
    "(see parish coordinator or contact@aikungfu.dev)."
)
# ──────────────────────────────────────────────────────────────────────────────

st.title("👥 Small Christian Communities (SCCs)")
st.caption("The backbone of African Catholicism · Est. AMECEA 1973 · 45,000+ SCCs in Kenya alone")

if "sccs" not in st.session_state:
    try:
        from services.sheets import fetch as _fetch_sheets
        _saved = _fetch_sheets("scc_registration")
        st.session_state.sccs = _saved if _saved else []
    except Exception:
        st.session_state.sccs = []
if "scc_meetings" not in st.session_state:
    st.session_state.scc_meetings = []

try:
    from services.save_indicator import trust_banner
    trust_banner("SCC")
except Exception:
    pass

tab1, tab2, tab3, tab4 = st.tabs(["📋 SCC Directory", "📅 Meeting Records", "📖 Formation Resources", "📊 Analytics"])

# ── DIRECTORY ─────────────────────────────────────────────────────────────────
with tab1:
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        search = st.text_input("🔍 Search SCCs", placeholder="Name, zone, leader…")
    with col_b:
        zone_filter = st.selectbox("Zone", ["All Zones"] + sorted(set(s["Zone"] for s in st.session_state.sccs)))
    with col_c:
        status_filter = st.selectbox("Status", ["All", "Active", "Inactive", "New"])

    sccs = st.session_state.sccs
    if search:
        q = search.lower()
        sccs = [s for s in sccs if q in s["Name"].lower() or q in s["Leader"].lower() or q in s["Zone"].lower()]
    if zone_filter != "All Zones":
        sccs = [s for s in sccs if s["Zone"] == zone_filter]
    if status_filter != "All":
        sccs = [s for s in sccs if s["Status"] == status_filter]

    st.metric("SCCs shown", len(sccs))

    for scc in sccs:
        with st.expander(f"👥 {scc['Name']} — {scc['Zone']} · {scc['Status']}"):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Leader:** {scc['Leader']}\n\n**Phone:** {scc['Phone']}")
            c2.markdown(f"**Meets:** {scc['Meeting Day']} at {scc['Meeting Time']}\n\n**Location:** {scc['Location']}")
            c3.markdown(f"**Families:** {scc['Families']}\n\n**Focus:** {scc['Focus']}")
            if scc["Notes"]:
                st.caption(scc["Notes"])

    st.divider()
    with st.expander("➕ Add New SCC", expanded=not st.session_state.sccs):
        with st.form("scc_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("SCC Name *", placeholder="St. Joseph's SCC")
                zone = st.text_input("Zone / Area", placeholder="Zone C · Westlands")
                leader_name = st.text_input("Leader Name")
                leader_phone = st.text_input("Leader Phone", placeholder="+254…")
            with c2:
                meeting_day = st.selectbox("Meeting Day",
                    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
                meeting_time = st.text_input("Meeting Time", placeholder="6:00 PM")
                location = st.text_input("Meeting Location", placeholder="Classroom / Home / Church Hall")
                families = st.number_input("Number of Families", min_value=0, value=10)

            focus = st.multiselect("Formation Focus",
                ["Bible Study", "Prayer", "Justice & Service", "Youth Support",
                 "Family Life", "Vocations", "Healing Ministry", "Evangelisation"],
                default=["Bible Study", "Prayer"])
            status = st.selectbox("Status", ["Active", "New", "Inactive"])
            notes = st.text_area("Notes / Special circumstances", height=70)

            if st.form_submit_button("➕ Add SCC", type="primary") and name:
                from services.sheets import _save
                scc_data = {
                    "Name": name, "Zone": zone, "Leader": leader_name,
                    "Phone": leader_phone, "Meeting Day": meeting_day,
                    "Meeting Time": meeting_time, "Location": location,
                    "Families": families, "Status": status,
                    "Focus": ", ".join(focus), "Notes": notes,
                }
                st.session_state.sccs.append(scc_data)
                _ok = _save("scc_registration", scc_data)
                show_save_status("scc_registration", _ok)
                st.success(f"✅ SCC '{name}' added successfully!")
                st.balloons()

# ── MEETINGS ─────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("📅 Meeting Records — Lumko 7-Step Method")
    st.caption("The Lumko method: See → Judge → Act — developed for African SCCs")

    with st.expander("➕ Record a Meeting"):
        with st.form("meeting_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                scc_names = [s["Name"] for s in st.session_state.sccs] or ["No SCCs yet"]
                selected_scc = st.selectbox("SCC", scc_names)
                meeting_date = st.date_input("Meeting Date")
                attendees = st.number_input("Number present", min_value=0, value=8)
            with c2:
                reading = st.text_input("Scripture reading discussed", placeholder="Luke 6:17-26")
                action_taken = st.text_area("Action / Resolution from last meeting", height=60)
                new_action = st.text_area("New action agreed today", height=60)

            lumko_step = st.selectbox("Lumko step reached",
                ["Step 1: We speak to God (opening prayer)",
                 "Step 2: We read God's word",
                 "Step 3: We allow God's word to sink in (silence)",
                 "Step 4: We listen to God's word together (sharing)",
                 "Step 5: We apply God's word to our life",
                 "Step 6: We pray together (intercessions)",
                 "Step 7: We go out to love and serve (action point)"])
            prayer_intentions = st.text_area("Prayer intentions raised", height=60)
            absences_reason = st.text_input("Notable absences / follow-up needed")

            if st.form_submit_button("📅 Record Meeting", type="primary"):
                from services.sheets import _save
                meeting_data = {
                    "SCC": selected_scc, "Date": str(meeting_date),
                    "Attendees": attendees, "Reading": reading,
                    "Lumko Step": lumko_step, "New Action": new_action,
                    "Prayer Intentions": prayer_intentions,
                }
                st.session_state.scc_meetings.append(meeting_data)
                _ok = _save("scc_meeting", meeting_data)
                show_save_status("scc_meeting", _ok)
                st.success(f"✅ Meeting for {selected_scc} on {meeting_date} recorded.")

    if st.session_state.scc_meetings:
        import pandas as pd
        st.dataframe(pd.DataFrame(st.session_state.scc_meetings), use_container_width=True)
    else:
        st.info("No meeting records yet. Add one above.")

# ── FORMATION ─────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("📖 Formation Resources")

    with st.expander("🔍 Discussion Guide — Generate for any reading"):
        gospel = st.text_input("Gospel / Reading reference", placeholder="Luke 6:17-26 · 6th Sunday Ordinary Time")
        if st.button("Generate Lumko discussion guide") and gospel:
            st.markdown(f"""
**Lumko Method Discussion Guide — {gospel}**

**Step 1 — Opening Prayer** *(2 min)*
Leader opens with the Sign of the Cross and a brief spontaneous prayer.

**Step 2 — Reading God's Word** *(5 min)*
Read the passage aloud twice (different readers if possible).

**Step 3 — Silence** *(2 min)*
Quiet reflection. "What word or phrase struck you?"

**Step 4 — Sharing** *(10 min)*
Each person shares their word/phrase. *No debate — just sharing.*

**Step 5 — Application** *(15 min)*
- What does this passage say to our community today?
- Is there a situation in our neighbourhood this speaks to?
- What does Jesus want us to do as a result?

**Step 6 — Intercessions** *(5 min)*
Pray for the needs raised in the discussion.

**Step 7 — Action Point** *(5 min)*
Agree on ONE concrete action before the next meeting.
- Who will do it?
- By when?
- Who will check?

*Closing prayer. Announce next meeting date.*
""")

    st.markdown("**📚 Recommended SCC Resources**")
    st.markdown("""
- 🇰🇪 [KCCB SCCs Resources](https://kccb.or.ke) — Kenya Catholic Bishops' Conference
- 🌍 [AMECEA Documentation](https://amecea.org) — Eastern Africa SCC theology
- 📖 *We Are Church* — Lumko Institute, South Africa
- 📘 *Small Christian Communities: A Vision of Hope* — Fr. Joseph Healey
- 🎵 SCC songs and prayer books — available from your diocesan office
""")

# ── ANALYTICS ─────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("📊 SCC Analytics")
    if st.session_state.sccs:
        c1, c2, c3, c4 = st.columns(4)
        total_sccs = len(st.session_state.sccs)
        active = sum(1 for s in st.session_state.sccs if s["Status"] == "Active")
        total_families = sum(s["Families"] for s in st.session_state.sccs)
        c1.metric("Total SCCs", total_sccs)
        c2.metric("Active", active)
        c3.metric("Families covered", total_families)
        c4.metric("Meetings recorded", len(st.session_state.scc_meetings))

        import plotly.express as px
        import pandas as pd
        df = pd.DataFrame(st.session_state.sccs)
        if "Zone" in df.columns:
            fig = px.bar(df.groupby("Zone")["Families"].sum().reset_index(),
                        x="Zone", y="Families", title="Families per Zone")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add SCCs to see analytics.")
