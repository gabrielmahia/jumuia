"""
Catholic Network Tools — Sacraments & Prayer
Track baptisms, confirmations, marriages, funerals + prayer intentions
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Sacraments", layout="wide")

st.title("🛐 Sacraments & Prayer")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Sacraments", "Prayer Circle", "Follow-up Needed", "Statistics"])

with tab1:
    st.markdown("## Upcoming Sacraments")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        sacrament_type = st.selectbox("Filter by sacrament", 
            ["All", "Baptism", "First Communion", "Confirmation", "Marriage", "Funeral"])
    with col2:
        st.metric("This Month", "12 sacraments", "+3 from last month")
    
    # Sacrament schedule
    sacraments = pd.DataFrame({
        "Date": ["Mar 5", "Mar 12", "Mar 19", "Mar 26", "Apr 2"],
        "Type": ["Baptism", "First Communion", "Confirmation", "Marriage", "Baptism"],
        "Family/Person": ["Njoroge family", "30 children", "16 youth", "David & Sarah", "Kipchoge family"],
        "Prep Status": ["✓ Complete", "🟡 In progress", "✓ Complete", "✓ Complete", "✓ Complete"],
        "Pastoral Follow-up": ["Home visit scheduled", "Class attendance: 8/10", "Retreat: 100% attended", "Honeymoon support", "Home visit pending"]
    })
    st.dataframe(sacraments, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Record New Sacrament")
    
    col1, col2 = st.columns(2)
    with col1:
        sac_type = st.selectbox("Sacrament type", ["Baptism", "First Communion", "Confirmation", "Marriage", "Holy Orders", "Religious Profession", "Funeral"])
        person_name = st.text_input("Person/Family name")
        sacrament_date = st.date_input("Date of sacrament")
    
    with col2:
        if sac_type == "Baptism":
            godparent1 = st.text_input("Godparent 1")
            godparent2 = st.text_input("Godparent 2")
        elif sac_type == "Marriage":
            spouse = st.text_input("Spouse")
            witness1 = st.text_input("Witness 1")
    
    if st.button("Record Sacrament"):
        st.success(f"✅ {sac_type} for {person_name} recorded on {sacrament_date}")
        st.markdown("**Next steps:**\n- Assign pastoral follow-up team\n- Schedule home visit (if applicable)\n- Send formal certificate\n- Add to parish archive")

with tab2:
    st.markdown("## Prayer Circle")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        prayer_group = st.selectbox("Prayer circle", 
            ["All", "Morning Rosary", "Evening Intentions", "Healing Circle", "Migrant Solidarity"])
    with col2:
        st.metric("Active Prayers", "23 intentions", "Prayed for 412 times this week")
    
    # Active prayer intentions
    prayers = pd.DataFrame({
        "Intention": [
            "Healing for Mrs. Nyambura (arthritis)",
            "Blessing for refugee family (safety)",
            "Job for Mr. Tom (65, long-term unemployed)",
            "Guidance for Rachel (RCIA discernment)",
            "Peace in Ukraine"
        ],
        "Submitted by": ["Maria", "Fr. Emmanuel", "Pastoral team", "Rachel", "Justice team"],
        "Date": [
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
        ],
        "Times Prayed": [47, 89, 156, 203, 412],
        "Status": ["🟡 Ongoing", "🟢 Answered", "🟢 Answered", "🟡 Ongoing", "🟡 Ongoing"]
    })
    st.dataframe(prayers, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Add Prayer Intention")
    
    col1, col2 = st.columns(2)
    with col1:
        intention = st.text_area("What should we pray for?")
        circle = st.selectbox("Which prayer circle?", ["Morning Rosary", "Evening Intentions", "Healing Circle", "Migrant Solidarity"])
    with col2:
        st.info("✊ **Our prayer becomes action.**\n\nWhen we pray for a refugee family's safety, we also advocate for their legal rights.\n\nWhen we pray for someone's healing, we also visit them + bring meals.\n\nPrayer + action together.")
    
    if st.button("Submit Prayer Intention"):
        st.success("🙏 Your intention has been added. Pray with us!")

with tab3:
    st.markdown("## Pastoral Follow-up Needed")
    
    follow_ups = pd.DataFrame({
        "Family/Person": [
            "Kipchoge family (baptism)",
            "Marriage couple (David & Sarah)",
            "3 first communicants",
            "Mrs. Nyambura (homebound)"
        ],
        "Type": ["Post-baptism visit", "Marriage prep session 2", "Celebration visit", "Weekly check-in"],
        "Due": ["This week", "Next week", "This month", "This week"],
        "Assigned To": ["Maria", "Fr. Steve", "Volunteers", "Pastoral team"],
        "Status": ["📅 Scheduled", "⏳ Pending", "Not yet assigned", "✓ Complete this week"]
    })
    st.dataframe(follow_ups, use_container_width=True)

with tab4:
    st.markdown("## Sacrament Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Baptisms (YTD)", "23", "+2 from last quarter")
    with col2:
        st.metric("Marriages (YTD)", "8", "+1 from last quarter")
    with col3:
        st.metric("Funerals (YTD)", "5", "-2 from last year")
    with col4:
        st.metric("Prayer Active", "23", "+12 this month")
    
    st.markdown("---")
    st.markdown("### Sacrament Trends")
    
    import plotly.graph_objects as go
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    baptisms = [3, 4, 5, 4, 3, 4]
    marriages = [1, 1, 2, 1, 1, 2]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=baptisms, mode='lines+markers', name='Baptisms'))
    fig.add_trace(go.Scatter(x=months, y=marriages, mode='lines+markers', name='Marriages'))
    fig.update_layout(title="Sacrament Frequency (2024)", height=300)
    st.plotly_chart(fig, use_container_width=True)
