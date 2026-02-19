"""Pastoral Care — Homebound visits, grief support, mentorship, new member integration."""

import streamlit as st
try:
    from services.save_indicator import mark_saved, show_save_status
except Exception:
    def mark_saved(x): pass
    def show_save_status(x, y=None): pass
from datetime import date

st.set_page_config(page_title="Pastoral Care", page_icon="🤝", layout="wide")

st.title("🤝 Pastoral Care")
st.caption("Homebound visits · Grief support · Mentorship · New member integration")

for key, default in [
    ("homebound", [{"Name": "Maria Njeri", "Condition": "Elderly (88)", "Address": "Westlands Rd 12",
                    "Phone": "+254700000001", "Emergency Contact": "Daughter: +254700000002",
                    "Freq": "Weekly", "Minister": "Fr. Patrick", "Last Visit": "2026-02-15",
                    "Communion": True, "Notes": "Prefers morning visits"}]),
    ("grief", []),
    ("mentors", []),
    ("new_members", []),
]:
    if key not in st.session_state:
        st.session_state[key] = default

tab1, tab2, tab3, tab4 = st.tabs(
    ["🏠 Homebound & Sick", "💔 Grief Support", "🤝 Mentorship", "🆕 New Members"]
)

# ── HOMEBOUND ─────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("🏠 Homebound & Sick Visit Register")
    for p in st.session_state.homebound:
        comm_icon = "🍞" if p.get("Communion") else ""
        with st.expander(f"🏠 {p['Name']} {comm_icon} — Last visit: {p.get('Last Visit', 'N/A')}"):
            c1, c2 = st.columns(2)
            c1.markdown(f"**Condition:** {p['Condition']}\n\n**Address:** {p['Address']}\n\n**Phone:** {p['Phone']}")
            c2.markdown(f"**Visit Freq:** {p['Freq']}\n\n**Minister:** {p['Minister']}\n\n**Emergency:** {p.get('Emergency Contact','')}")
            if p["Notes"]:
                st.caption(p["Notes"])

    with st.expander("➕ Add Homebound / Sick Person"):
        with st.form("homebound_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name *")
                condition = st.text_input("Condition / Reason", placeholder="Elderly, Post-surgery, Chronic illness…")
                address = st.text_input("Home Address")
                phone = st.text_input("Contact Phone")
            with c2:
                emergency = st.text_input("Emergency Contact (Name & Phone)")
                freq = st.selectbox("Visit Frequency", ["Weekly", "Bi-weekly", "Monthly", "As needed"])
                minister = st.text_input("Assigned Minister / Volunteer")
                communion = st.checkbox("Receives Communion at home")
            notes = st.text_area("Notes (language preference, best times, special needs)", height=70)

            if st.form_submit_button("🏠 Add to Register", type="primary") and name:
                from services.sheets import _save
                _hb = {
                    "Name": name, "Condition": condition, "Address": address,
                    "Phone": phone, "Emergency Contact": emergency, "Freq": freq,
                    "Minister": minister, "Last Visit": str(date.today()),
                    "Communion": communion, "Notes": notes,
                }
                st.session_state.homebound.append(_hb)
                _ok = _save("pastoral_homebound", _hb)
                show_save_status("pastoral_homebound", _ok)
                st.success(f"✅ {name} added to homebound register.")

    with st.expander("📋 Record a Visit"):
        with st.form("visit_form"):
            names = [p["Name"] for p in st.session_state.homebound] or ["No entries yet"]
            visited = st.selectbox("Person visited", names)
            visit_date = st.date_input("Visit Date")
            visitor = st.text_input("Visiting Minister / Extraordinary Minister")
            communion_given = st.checkbox("Communion administered")
            sacrament = st.selectbox("Other sacrament given",
                ["None", "Anointing of the Sick", "Reconciliation", "Viaticum"])
            observation = st.text_area("Pastoral observation / follow-up needed", height=70)
            if st.form_submit_button("Record Visit", type="primary"):
                for p in st.session_state.homebound:
                    if p["Name"] == visited:
                        p["Last Visit"] = str(visit_date)
                st.success(f"✅ Visit to {visited} on {visit_date} recorded.")

# ── GRIEF ─────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("💔 Grief & Bereavement Support")

    if st.session_state.grief:
        for g in st.session_state.grief:
            with st.expander(f"💔 {g['Name']} — {g['Loss Type']}"):
                c1, c2 = st.columns(2)
                c1.markdown(f"**Loss type:** {g['Loss Type']}\n\n**Date of loss:** {g['Date of Loss']}\n\n**Phone:** {g['Phone']}")
                c2.markdown(f"**Support type:** {g['Support']}\n\n**Assigned to:** {g['Assigned To']}\n\n**Check-in Freq:** {g['Check-in']}")
    else:
        st.info("No grief support records yet.")

    with st.expander("➕ Add Grief Support Case"):
        with st.form("grief_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Person's Name *")
                phone = st.text_input("Contact Phone")
                loss_type = st.selectbox("Type of Loss / Crisis", [
                    "Death of spouse", "Death of child", "Death of parent",
                    "Death of sibling / friend", "Job loss / Financial crisis",
                    "Serious illness (own)", "Serious illness (family)",
                    "Relationship breakdown / Separation", "Miscarriage / Infant loss",
                    "Trauma / Violence", "Other",
                ])
                loss_date = st.date_input("Date of Loss / Crisis")
            with c2:
                support = st.selectbox("Support Type", [
                    "Peer befriending (trained volunteer)",
                    "Grief group (weekly)",
                    "Priest pastoral visit",
                    "Counselling referral",
                    "Practical support (meals, childcare)",
                    "Prayer partner",
                ])
                assigned = st.text_input("Assigned Minister / Volunteer")
                checkin = st.selectbox("Check-in Frequency", ["Weekly", "Bi-weekly", "Monthly"])
            notes = st.text_area("Notes / Context")

            if st.form_submit_button("💔 Add Case", type="primary") and name:
                from services.sheets import _save
                _gr = {
                    "Name": name, "Phone": phone, "Loss Type": loss_type,
                    "Date of Loss": str(loss_date), "Support": support,
                    "Assigned To": assigned, "Check-in": checkin, "Notes": notes,
                }
                st.session_state.grief.append(_gr)
                _ok = _save("pastoral_grief", _gr)
                show_save_status("pastoral_grief", _ok)
                st.success(f"✅ Grief support record for {name} added.")

# ── MENTORSHIP ────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("🤝 Mentorship Programme")

    for m in st.session_state.mentors:
        with st.expander(f"🤝 {m['Mentee']} ← {m['Mentor']} | {m['Focus']}"):
            c1, c2 = st.columns(2)
            c1.markdown(f"**Mentor:** {m['Mentor']}\n\n**Mentee:** {m['Mentee']}\n\n**Started:** {m['Start Date']}")
            c2.markdown(f"**Focus:** {m['Focus']}\n\n**Meet Frequency:** {m['Frequency']}\n\n**Status:** {m['Status']}")

    with st.expander("➕ Create Mentorship Pair"):
        with st.form("mentor_form"):
            c1, c2 = st.columns(2)
            with c1:
                mentor = st.text_input("Mentor Name *")
                mentor_phone = st.text_input("Mentor Phone")
            with c2:
                mentee = st.text_input("Mentee Name *")
                mentee_phone = st.text_input("Mentee Phone")

            focus = st.selectbox("Mentorship Focus", [
                "New Catholic / RCIA follow-up", "Young adult faith journey",
                "Marriage preparation support", "Youth-to-young adult transition",
                "Re-engaging lapsed Catholic", "Addiction recovery support",
                "Career / Vocation discernment", "Prison re-integration",
                "Grief / Trauma recovery", "Leadership development",
            ])
            frequency = st.selectbox("Meeting Frequency", ["Weekly", "Bi-weekly", "Monthly"])
            start = st.date_input("Start Date")
            status = st.selectbox("Status", ["Active", "Completed", "On Hold"])

            if st.form_submit_button("🤝 Create Pair", type="primary") and mentor and mentee:
                st.session_state.mentors.append({
                    "Mentor": mentor, "Mentor Phone": mentor_phone,
                    "Mentee": mentee, "Mentee Phone": mentee_phone,
                    "Focus": focus, "Frequency": frequency,
                    "Start Date": str(start), "Status": status,
                })
                st.success(f"✅ Mentorship pair {mentor} ↔ {mentee} created.")

# ── NEW MEMBERS ───────────────────────────────────────────────────────────────
with tab4:
    st.subheader("🆕 New Member Integration")

    for nm in st.session_state.new_members:
        with st.expander(f"🆕 {nm['Name']} — Joined {nm['Joined']}"):
            c1, c2 = st.columns(2)
            c1.markdown(f"**Phone:** {nm['Phone']}\n\n**How connected:** {nm['How Connected']}\n\n**Assigned SCC:** {nm['SCC']}")
            c2.markdown(f"**Welcome sponsor:** {nm['Sponsor']}\n\n**Follow-up:** {nm['Follow-up']}")

    with st.expander("➕ Register New Member"):
        with st.form("new_member_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name *")
                phone = st.text_input("Phone")
                email = st.text_input("Email (optional)")
                joined = st.date_input("Date First Attended / Joined")
            with c2:
                how = st.selectbox("How Did They Connect?", [
                    "Walked in / Sunday Mass", "RCIA / Inquiry",
                    "Married into parish", "Moved from another parish",
                    "Invited by parishioner", "Online / Social media",
                    "Life event (baptism, funeral)", "Other",
                ])
                scc = st.text_input("Assigned SCC (if any)")
                sponsor = st.text_input("Welcome Sponsor Name")
                followup = st.selectbox("Follow-up Assigned", ["Weekly call", "Monthly check-in", "SCC integration", "RCIA track"])

            notes = st.text_area("Notes")
            if st.form_submit_button("🆕 Register", type="primary") and name:
                st.session_state.new_members.append({
                    "Name": name, "Phone": phone, "Email": email,
                    "Joined": str(joined), "How Connected": how,
                    "SCC": scc, "Sponsor": sponsor, "Follow-up": followup, "Notes": notes,
                })
                st.success(f"✅ {name} registered as new member.")

st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Homebound", len(st.session_state.homebound))
c2.metric("Grief Cases", len(st.session_state.grief))
c3.metric("Mentorships", len(st.session_state.mentors))
c4.metric("New Members", len(st.session_state.new_members))
