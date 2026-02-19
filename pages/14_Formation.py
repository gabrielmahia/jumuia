"""Formation & Spiritual Education — Programmes, enrolment, curriculum, progress tracking."""

import streamlit as st
try:
    from services.save_indicator import mark_saved, show_save_status
except Exception:
    def mark_saved(x): pass
    def show_save_status(x, y=None): pass
from datetime import date

st.set_page_config(page_title="Formation", page_icon="🎓", layout="wide")

st.title("🎓 Formation & Spiritual Education")
st.caption("RCIA · Adult faith · Youth · Bible study · Retreats · Vocations")

if "formation_programmes" not in st.session_state:
    st.session_state.formation_programmes = [
        {"Programme": "RCIA (Rite of Christian Initiation)", "Category": "Adult Formation",
         "Leader": "Deacon Samuel", "Duration": "Sep 2025 – Easter 2026",
         "Enrolled": 12, "Status": "Active", "Meeting": "Tuesday 7 PM", "Location": "Parish Hall"},
        {"Programme": "Youth Confirmation Prep", "Category": "Youth",
         "Leader": "Sr. Agnes", "Duration": "Jan – May 2026",
         "Enrolled": 24, "Status": "Active", "Meeting": "Saturday 10 AM", "Location": "School Room 3"},
        {"Programme": "Adult Bible Study", "Category": "Scripture",
         "Leader": "Mrs. Wanjiku", "Duration": "Ongoing (term basis)",
         "Enrolled": 16, "Status": "Active", "Meeting": "Wednesday 6 PM", "Location": "Library"},
    ]
if "formation_participants" not in st.session_state:
    st.session_state.formation_participants = []

tab1, tab2, tab3 = st.tabs(["📋 Programmes", "👤 Participant Register", "📖 Curriculum Library"])

with tab1:
    for prog in st.session_state.formation_programmes:
        status_color = "🟢" if prog["Status"] == "Active" else ("🟡" if prog["Status"] == "Planned" else "🔴")
        with st.expander(f"{status_color} {prog['Programme']} — {prog['Category']}"):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Leader:** {prog['Leader']}\n\n**Duration:** {prog['Duration']}")
            c2.markdown(f"**Meets:** {prog['Meeting']}\n\n**Location:** {prog['Location']}")
            c3.metric("Enrolled", prog["Enrolled"])

    st.divider()
    with st.expander("➕ Add Formation Programme"):
        with st.form("prog_form"):
            c1, c2 = st.columns(2)
            with c1:
                prog_name = st.text_input("Programme Name *")
                category = st.selectbox("Category", [
                    "Adult Formation", "RCIA", "Youth", "Children's Catechesis",
                    "Scripture / Bible Study", "Marriage & Family", "Vocations",
                    "Retreat / Renewal", "Leadership Formation", "Justice & Peace"])
                leader = st.text_input("Programme Leader")
                duration = st.text_input("Duration", placeholder="Jan – May 2026")
            with c2:
                meeting_day = st.text_input("Meeting Day & Time", placeholder="Tuesday 7 PM")
                location = st.text_input("Location")
                enrolled = st.number_input("Initial enrolment", min_value=0, value=0)
                status = st.selectbox("Status", ["Planned", "Active", "Completed", "Suspended"])

            if st.form_submit_button("➕ Add Programme", type="primary") and prog_name:
                from services.sheets import _save
                _prog = {"Programme": prog_name, "Category": category, "Leader": leader,
                    "Duration": duration, "Enrolled": enrolled, "Status": status,
                    "Meeting": meeting_day, "Location": location}
                st.session_state.formation_programmes.append(_prog)
                _ok = _save("formation_programme", _prog)
                    show_save_status("formation_programme", _ok)
                st.success(f"✅ '{prog_name}' added.")

with tab2:
    if st.session_state.formation_participants:
        import pandas as pd
        st.dataframe(pd.DataFrame(st.session_state.formation_participants), use_container_width=True)
    else:
        st.info("No participants registered yet.")

    with st.expander("➕ Register Participant"):
        with st.form("part_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name *")
                phone = st.text_input("Phone")
                email = st.text_input("Email")
                dob = st.date_input("Date of Birth", max_value=date.today())
            with c2:
                prog_names = [p["Programme"] for p in st.session_state.formation_programmes] or ["No programmes yet"]
                programme = st.selectbox("Programme *", prog_names)
                enrol_date = st.date_input("Enrolment Date")
                sessions_attended = st.number_input("Sessions Attended", min_value=0, value=0)
                completion_status = st.selectbox("Status", ["Enrolled", "Active", "Completed", "Withdrawn"])

            notes = st.text_area("Notes / Special requirements")

            if st.form_submit_button("Register", type="primary") and name:
                from services.sheets import _save
                _part = {"Name": name, "Phone": phone, "Email": email,
                    "Programme": programme, "Enrolled": str(enrol_date),
                    "Sessions": sessions_attended, "Status": completion_status, "Notes": notes}
                st.session_state.formation_participants.append(_part)
                _ok = _save("formation_participant", _part)
                    show_save_status("formation_participant", _ok)
                st.success(f"✅ {name} registered for {programme}.")

with tab3:
    st.subheader("📖 Curriculum & Resource Library")

    resources = {
        "RCIA": [
            "RCIA process: Precatechumenate → Catechumenate → Purification → Mystagogy",
            "*Rite of Christian Initiation of Adults* (RCIA) — official ritual text (USCCB)",
            "*The RCIA: Transforming the Church* — Thomas Morris",
            "Kenya: KCCB RCIA guidelines — contact your diocese",
        ],
        "Youth Formation": [
            "*YouCat* (Youth Catechism of the Catholic Church)",
            "*DOCAT* — Catholic Social Teaching for young people",
            "World Youth Day resources — dicasteryforlaity.va",
            "Kenya Catholic Youth Organization (KCAYO) — kcayo.org",
        ],
        "Bible Study": [
            "Lectio Divina (Sacred Reading) method — 4 steps: Read, Meditate, Pray, Contemplate",
            "*The Bible Timeline* — Jeff Cavins (Great Adventure Bible Study)",
            "*Walking with God* — Tim Gray & Jeff Cavins",
            "Africa: BICAM (Biblical Institute of Central Africa)",
        ],
        "Adult Faith": [
            "*Catechism of the Catholic Church* (CCC) — free at Vatican.va",
            "*Compendium of the CCC* — concise summary",
            "*Theology of the Body* — St. John Paul II",
            "FORMED.org — online Catholic content library",
        ],
        "Justice & Peace": [
            "*Rerum Novarum* (1891) — Leo XIII — labour and capital",
            "*Gaudium et Spes* (1965) — Vatican II on Church in modern world",
            "*Laudato Si'* (2015) — Francis — care for creation",
            "*Laudate Deum* (2023) — Francis — climate action",
            "CAFOD, Caritas Internationalis — justice programme resources",
        ],
    }

    for category, items in resources.items():
        with st.expander(f"📚 {category}"):
            for item in items:
                st.markdown(f"• {item}")

    st.divider()
    st.markdown("**🌐 Key Formation Links**")
    st.markdown("""
- [Vatican.va](https://vatican.va) — Official documents, Catechism
- [KCCB](https://kccb.or.ke) — Kenya Catholic Bishops' Conference
- [AMECEA](https://amecea.org) — Association of Member Episcopal Conferences in Eastern Africa
- [USCCB](https://usccb.org) — US Bishops (Formation resources in English)
- [FORMED](https://formed.org) — Parish content subscription
""")
