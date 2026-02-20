"""Catechist Certification Tracking — Multi-level, renewals, diocesan standards."""

import streamlit as st
try:
    from services.save_indicator import mark_saved, show_save_status
except Exception:
    def mark_saved(x): pass
    def show_save_status(x, y=None): pass
from datetime import date, timedelta

st.set_page_config(page_title="Catechist Certification", page_icon="📚", layout="wide")

st.title("📚 Catechist Certification")
st.caption("Multi-level certification tracking · Renewal cycles · Diocesan standards")

CERT_LEVELS = {
    "Basic": {"hours": 48, "years_valid": 3, "color": "🟡"},
    "Intermediate": {"hours": 80, "years_valid": 3, "color": "🟠"},
    "Advanced": {"hours": 120, "years_valid": 3, "color": "🔵"},
    "Master Catechist": {"hours": 180, "years_valid": 5, "color": "🟣"},
}

MINISTRY_AREAS = [
    "RCIA (Adult Formation)", "Sacramental Preparation (Children)",
    "Religious Education (School-age)", "Youth Ministry",
    "Adult Faith Formation", "Marriage Preparation",
    "Special Needs Ministry", "Prison Ministry",
    "RITE (Adapted RCIA)", "SCC Formation",
]

if "catechists" not in st.session_state:
    st.session_state.catechists = [
        {"Name": "Agnes Wanjiku Muthoni", "Email": "agnes.muthoni@stjoserph.ac.ke", "Phone": "+254711234567",
         "Level": "Advanced", "Ministry": "Sacramental Preparation (Children)",
         "Start Date": "2022-03-01", "Hours Completed": 110, "Hours Required": 120,
         "Status": "In Progress", "Background Check": True, "Renewal Due": "2026-03-15", "Notes": "Teaching First Communion class, Rongai"},
        {"Name": "Peter Otieno Odhiambo", "Email": "", "Phone": "+254722987654",
         "Level": "Basic", "Ministry": "RCIA (Adult Formation)",
         "Start Date": "2021-09-10", "Hours Completed": 48, "Hours Required": 48,
         "Status": "Renewal Due", "Background Check": True, "Renewal Due": "2026-03-30", "Notes": "Renewal due — contact by end of month"},
        {"Name": "Sr. Consolata Akinyi", "Email": "c.akinyi@consolata.org", "Phone": "+254733456789",
         "Level": "Master Catechist", "Ministry": "Adult Faith Formation",
         "Start Date": "2019-01-20", "Hours Completed": 180, "Hours Required": 180,
         "Status": "Certified", "Background Check": True, "Renewal Due": "2027-01-20", "Notes": "Also coordinates Kiswahili liturgy group"},
        {"Name": "James Kamau Njoroge", "Email": "", "Phone": "+254700112233",
         "Level": "Intermediate", "Ministry": "Youth Ministry",
         "Start Date": "2023-06-01", "Hours Completed": 55, "Hours Required": 80,
         "Status": "In Progress", "Background Check": False, "Renewal Due": "2026-06-01", "Notes": "Background check pending — remind Fr. Daniel"},
        {"Name": "Mary Wairimu Gitau", "Email": "wairimu.gitau@gmail.com", "Phone": "+254755667788",
         "Level": "Basic", "Ministry": "Special Needs Ministry",
         "Start Date": "2024-01-10", "Hours Completed": 48, "Hours Required": 48,
         "Status": "Certified", "Background Check": True, "Renewal Due": "2027-01-10", "Notes": "Works with deaf community, St Austin's"},
    ]

# Demo notice
st.info(
    "**Preview mode** — Sample records shown so you can explore the tool. "
    "Your parish's real data will be saved privately once your coordinator connects the register.",
    icon="ℹ️"
)

tab1, tab2, tab3 = st.tabs(["👥 Catechist Register", "📊 Analytics & Renewals", "📋 Training Log"])

with tab1:
    # Filters
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        level_filter = st.selectbox("Level", ["All"] + list(CERT_LEVELS.keys()))
    with fc2:
        status_filter = st.selectbox("Status", ["All", "Certified", "In Progress", "Renewal Due", "Expired"])
    with fc3:
        search = st.text_input("🔍 Search", placeholder="Name, ministry…")

    catechists = st.session_state.catechists
    if level_filter != "All":
        catechists = [c for c in catechists if c["Level"] == level_filter]
    if status_filter != "All":
        catechists = [c for c in catechists if c["Status"] == status_filter]
    if search:
        q = search.lower()
        catechists = [c for c in catechists if q in c["Name"].lower() or q in c["Ministry"].lower()]

    for cat in catechists:
        level_info = CERT_LEVELS.get(cat["Level"], {})
        icon = level_info.get("color", "⚪")
        pct = min(100, int(cat["Hours Completed"] / cat["Hours Required"] * 100)) if cat["Hours Required"] else 100
        bg_ok = "✅" if cat["Background Check"] else "⚠️ No check"

        with st.expander(f"{icon} {cat['Name']} — {cat['Level']} · {cat['Status']}"):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Ministry:** {cat['Ministry']}\n\n**Email:** {cat['Email']}\n\n**Phone:** {cat['Phone']}")
            c2.markdown(f"**Started:** {cat['Start Date']}\n\n**Renewal Due:** {cat['Renewal Due']}\n\n**Background Check:** {bg_ok}")
            c3.markdown(f"**Progress:** {cat['Hours Completed']}/{cat['Hours Required']} hours")
            st.progress(pct / 100, text=f"{pct}% complete")
            if cat["Notes"]:
                st.caption(cat["Notes"])

    st.divider()
    with st.expander("➕ Add New Catechist"):
        with st.form("cat_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name *")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                ministry = st.selectbox("Ministry Area", MINISTRY_AREAS)
            with c2:
                level = st.selectbox("Certification Level", list(CERT_LEVELS.keys()))
                status = st.selectbox("Status", ["In Progress", "Certified", "Renewal Due", "Expired"])
                start = st.date_input("Start Date")
                bg_check = st.checkbox("Background check completed", value=True)

            hours_done = st.number_input("Hours Completed", min_value=0,
                                          max_value=300, value=0)
            notes = st.text_area("Notes")

            if st.form_submit_button("📚 Add Catechist", type="primary") and name:
                req = CERT_LEVELS[level]["hours"]
                valid = CERT_LEVELS[level]["years_valid"]
                renewal = (start + timedelta(days=365 * valid)).strftime("%Y-%m-%d")
                from services.sheets import _save
                _cat = {"Name": name, "Email": email, "Phone": phone,
                    "Level": level, "Ministry": ministry,
                    "Start Date": str(start), "Hours Completed": hours_done,
                    "Hours Required": req, "Status": status,
                    "Background Check": bg_check, "Renewal Due": renewal, "Notes": notes}
                st.session_state.catechists.append(_cat)
                _ok = _save("catechist_registration", _cat)
                show_save_status("catechist_registration", _ok)
                st.success(f"✅ {name} added as {level} catechist.")

with tab2:
    c1, c2, c3, c4 = st.columns(4)
    total = len(st.session_state.catechists)
    certified = sum(1 for c in st.session_state.catechists if c["Status"] == "Certified")
    in_prog = sum(1 for c in st.session_state.catechists if c["Status"] == "In Progress")
    due = sum(1 for c in st.session_state.catechists if c["Status"] in ["Renewal Due", "Expired"])
    c1.metric("Total Catechists", total)
    c2.metric("Certified", certified)
    c3.metric("In Progress", in_prog)
    c4.metric("Renewal/Expired", due, delta=f"-{due}" if due else None,
              delta_color="inverse" if due else "normal")

    # Upcoming renewals
    st.subheader("🔔 Upcoming Renewals (next 6 months)")
    today = date.today()
    upcoming = []
    for c in st.session_state.catechists:
        try:
            rd = date.fromisoformat(c["Renewal Due"])
            days = (rd - today).days
            if -30 <= days <= 180:
                upcoming.append({**c, "Days Until Renewal": days})
        except:
            pass
    if upcoming:
        import pandas as pd
        df = pd.DataFrame(upcoming)[["Name", "Level", "Ministry", "Renewal Due", "Days Until Renewal"]]
        st.dataframe(df.sort_values("Days Until Renewal"), use_container_width=True)
    else:
        st.success("✅ No renewals due in the next 6 months.")

    # Level breakdown
    if st.session_state.catechists:
        import plotly.express as px
        import pandas as pd
        df = pd.DataFrame(st.session_state.catechists)
        fig = px.pie(df, names="Level", title="Catechists by Certification Level")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("📋 Training Log")
    st.caption("Record individual course completions, workshops, and continuing formation")

    if "training_log" not in st.session_state:
        st.session_state.training_log = []

    with st.expander("➕ Log Training / Course Completion"):
        with st.form("training_form"):
            c1, c2 = st.columns(2)
            with c1:
                cat_names = [c["Name"] for c in st.session_state.catechists] or ["No catechists yet"]
                catechist = st.selectbox("Catechist", cat_names)
                course = st.text_input("Course / Workshop Name *")
                completed = st.date_input("Date Completed")
            with c2:
                provider = st.text_input("Provider / Trainer", placeholder="Diocese, KCCB, etc.")
                hours = st.number_input("Hours", min_value=0.5, max_value=200.0, value=3.0, step=0.5)
                category = st.selectbox("Category", [
                    "Scripture", "Catechetical Method", "Liturgy & Sacraments",
                    "Church Teaching", "Pastoral Skills", "Child Safeguarding",
                    "Special Needs", "Technology"])
            cert_received = st.checkbox("Certificate received")
            notes = st.text_area("Notes")

            if st.form_submit_button("📋 Log Training", type="primary") and course and catechist:
                from services.sheets import _save
                _tr = {"Catechist": catechist, "Course": course,
                    "Date": str(completed), "Provider": provider,
                    "Hours": hours, "Category": category, "Certificate": cert_received}
                st.session_state.training_log.append(_tr)
                _ok = _save("catechist_training", _tr)
                show_save_status("catechist_training", _ok)
                # Update catechist hours
                for c in st.session_state.catechists:
                    if c["Name"] == catechist:
                        c["Hours Completed"] = min(c["Hours Required"],
                                                   int(c["Hours Completed"]) + int(hours))
                st.success(f"✅ {hours}h logged for {catechist}.")

    if st.session_state.training_log:
        import pandas as pd
        st.dataframe(pd.DataFrame(st.session_state.training_log), use_container_width=True)
    else:
        st.info("No training logged yet.")

    st.divider()
    st.markdown("**📏 Certification Requirements Reference**")
    for level, info in CERT_LEVELS.items():
        st.markdown(f"**{info['color']} {level}** — {info['hours']} hours required · valid {info['years_valid']} years · 3-year renewal cycle")
