"""
Catholic Network Tools — Pastoral Care & Community
Track homebound visits, grief support, mentorship, integration
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Pastoral Care", layout="wide")

st.title("👥 Pastoral Care & Community")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Care Cases", "23", "+3 this month")
with col2:
    st.metric("Visits This Week", "18", "+2 from last week")
with col3:
    st.metric("Volunteers Serving", "12", "100% engaged")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Homebound", "Grief Support", "Mentorship", "New Member Integration"])

with tab1:
    st.markdown("## Homebound Parishioners")
    
    st.markdown("### Who Needs Visiting?")
    
    homebound = pd.DataFrame({
        "Name": ["Mrs. Nyambura", "Mr. James", "Sr. Margaret", "Mr. Kipchoge", "Mrs. Sarah"],
        "Age": [87, 92, 85, 78, 81],
        "Condition": ["Arthritis (mobility limited)", "Post-surgery recovery", "Dementia (memory care)", "Heart condition", "Diabetes (wound care)"],
        "Last Visited": [
            (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
        ],
        "Needs": ["Prayer circle, soup", "Physical therapy encouragement", "Gentle visit, reminiscence", "Blood pressure check-in", "Wound dressing help"],
        "Visit Frequency": ["3x/week", "2x/week", "1x/week", "2x/week", "3x/week"],
        "Assigned Visitor": ["Maria", "Tom", "Sister Anne", "Joseph", "Grace"]
    })
    st.dataframe(homebound, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Log a Visit")
    
    col1, col2 = st.columns(2)
    with col1:
        person = st.selectbox("Person visited", ["Mrs. Nyambura", "Mr. James", "Sr. Margaret", "Mr. Kipchoge", "Mrs. Sarah"])
        visitor = st.text_input("Visitor name")
        date = st.date_input("Date of visit")
    
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=15, max_value=180, value=45)
        notes = st.text_area("Visit notes (prayer shared, needs identified, follow-up)")
        mood = st.select_slider("Person's mood", ["Struggling", "Okay", "Good", "Great"])
    
    if st.button("Log Visit"):
        st.success(f"✅ Visit logged for {person} on {date} by {visitor}")

with tab2:
    st.markdown("## Grief Support")
    
    st.markdown("### Active Grief Cases")
    
    grief_cases = pd.DataFrame({
        "Name": ["David (wife passed)", "Rachel (lost job)", "James (son illness)", "Susan (parent death)"],
        "Loss Type": ["Death (spouse)", "Job loss", "Illness (child)", "Death (parent)"],
        "Date of Loss": ["2024-01-15", "2024-02-01", "2024-01-10", "2023-12-20"],
        "Support Assigned": ["Grief group + meals", "Financial counseling", "Prayer support", "1-on-1 counseling"],
        "Status": ["Attending weekly group", "Beginning recovery", "Ongoing prayer support", "Transitioning to small group"]
    })
    st.dataframe(grief_cases, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Grief Support Groups")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Tuesday Evening Grief Circle**
        - Time: 7pm
        - Leader: Sr. Mary + Tom
        - Attendees: 4 people
        - Focus: Loss + hope
        """)
    
    with col2:
        st.markdown("""
        **Sunday Morning "New Beginnings"**
        - Time: 10:30am
        - Leader: Fr. Emmanuel
        - Attendees: 7 people
        - Focus: Long-term recovery
        """)
    
    if st.button("Join a grief group"):
        st.success("We'll connect you with others on similar journeys. 💚")

with tab3:
    st.markdown("## Mentorship Programs")
    
    st.markdown("### Mentor-Mentee Pairings")
    
    mentorship = pd.DataFrame({
        "Mentor": ["Tom (retired teacher)", "Grace (nurse)", "Fr. Emmanuel", "Agnes (social worker)"],
        "Mentee": ["Marcus (18, exploring faith)", "Jennifer (25, career discernment)", "Samuel (teen, at-risk)", "David (recovering addiction)"],
        "Focus": ["Faith + discernment", "Work-life balance", "Belonging + purpose", "Accountability + hope"],
        "Meeting Frequency": ["2x/month", "1x/month", "Weekly", "2x/week"],
        "Duration": ["3 months", "6 months", "Ongoing", "12 months"]
    })
    st.dataframe(mentorship, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Looking for a Mentor?")
    
    if st.button("Request a mentor"):
        st.markdown("""
        **You'll be matched based on:**
        - Your age group (teen, young adult, adult, senior)
        - Your interests (faith, career, recovery, purpose)
        - Your availability (frequency of meetings)
        
        **Next steps:**
        - Complete short form
        - Meet potential mentors
        - Start meeting
        """)

with tab4:
    st.markdown("## New Member Integration")
    
    st.markdown("### New Parishioners (Last 3 Months)")
    
    new_members = pd.DataFrame({
        "Name": ["Sofia & Luis", "Michael", "Jessica", "The Chen family", "Robert"],
        "Joined": ["Jan 15", "Jan 22", "Feb 5", "Feb 12", "Feb 10"],
        "Status": ["Welcomed + small group assigned", "1st visit scheduled", "Attending regularly", "Baptism class next", "Connected to justice team"],
        "Contact Made": ["✓", "✓", "✓", "✓", "✓"],
        "Small Group Assigned": ["Yes (young adults)", "Pending", "Yes (faith explorers)", "Yes (families)", "Yes (justice)"],
        "Next Step": ["Confirm small group start", "Schedule welcome visit", "Invite to Easter vigil", "Complete baptism prep", "Justice campaign invite"]
    })
    st.dataframe(new_members, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Welcome Process Checklist")
    
    st.markdown("""
    ✅ **Week 1:** Personal welcome call  
    ✅ **Week 2:** Small group invitation  
    ✅ **Week 3:** Coffee with pastoral team  
    ✅ **Week 4:** Connect to volunteer opportunity  
    ✅ **Month 2:** Check-in call  
    ✅ **Month 3:** Celebrate! (Welcome party or special role)
    """)

st.markdown("---")

st.markdown("## Pastoral Care Statistics")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Homebound Visits", "23", "This month")
with col2:
    st.metric("Grief Support Active", "4 cases", "+1 from last month")
with col3:
    st.metric("Mentorships Active", "8 pairs", "Growing")
with col4:
    st.metric("New Members Integrated", "5", "This quarter")

st.info("""
💚 **Pastoral care is the heartbeat of parish community.**

When someone experiences loss, illness, loneliness, or searching—the Church shows up. 
This tracking ensures no one falls through the cracks. Relationships are built systematically. 
Trust is earned through presence.

This is how the Church becomes the **Body of Christ in action.**
""")
