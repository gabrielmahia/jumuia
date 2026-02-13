"""
Catholic Network Tools — Formation & Spiritual Education
Track catechesis, RCIA, youth groups, adult education, spiritual development
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Formation", layout="wide")

st.title("👦 Formation & Spiritual Education")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("In Catechesis", "34", "+3 this month")
with col2:
    st.metric("RCIA Candidates", "8", "6-month journey")
with col3:
    st.metric("Youth Group Active", "47", "3 age groups")
with col4:
    st.metric("Adult Bible Study", "12", "2 groups")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Catechesis", "RCIA", "Youth", "Adult Formation", "Progress Tracking"])

with tab1:
    st.markdown("## Catechesis (Children's Formation)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### K-3rd Grade Group")
        st.markdown("""
        **Leader:** Sister Anne  
        **Time:** Saturdays 10am  
        **Curriculum:** God loves me  
        **Enrollment:** 12 children  
        **Attendance:** 10 avg (83%)
        """)
    
    with col2:
        st.markdown("### 4th-6th Grade Group")
        st.markdown("""
        **Leader:** Tom (catechist)  
        **Time:** Saturdays 11:15am  
        **Curriculum:** Sacraments + Saints  
        **Enrollment:** 15 children  
        **Attendance:** 13 avg (87%)
        """)
    
    st.markdown("---")
    st.markdown("### Last Month's Learning")
    
    topics = pd.DataFrame({
        "Group": ["K-3", "K-3", "4-6", "4-6"],
        "Topic": ["Jesus loves me", "We are a family", "Baptism sacrament", "Saints + heroes"],
        "Date": ["Feb 3", "Feb 10", "Feb 3", "Feb 10"],
        "Activity": ["Craft + song", "Community game", "Water baptism experience", "Saint stories"],
        "Engagement": ["High", "Very High", "High", "High"]
    })
    st.dataframe(topics, use_container_width=True)

with tab2:
    st.markdown("## RCIA (Rite of Christian Initiation for Adults)")
    
    st.markdown("### The 6-Month Journey")
    
    st.markdown("""
    **Stage 1: Inquiry (Month 1)**
    - Who is Jesus?
    - What does the Church teach?
    - Is this for me?
    
    **Stage 2: Catechesis (Months 2-4)**
    - Creed (what we believe)
    - Liturgy (how we pray)
    - Morality (how we live)
    - Prayer (direct encounter with God)
    
    **Stage 3: Enlightenment (Month 5)**
    - Preparation for Easter vigil
    - Scrutinies (spiritual checkpoints)
    - Final questions + readiness
    
    **Stage 4: Mystagogy (After Easter)**
    - Sacraments unlocked
    - Small group support
    - Ongoing formation (6 months)
    """)
    
    st.markdown("---")
    st.markdown("### Current RCIA Class")
    
    rcia = pd.DataFrame({
        "Name": ["Rachel", "Michael", "Sarah & James", "David", "Sofia", "John", "Patricia", "Luis"],
        "Journey Started": ["Jan 2024", "Jan 2024", "Jan 2024", "Feb 2024", "Feb 2024", "Feb 2024", "Jan 2024", "Feb 2024"],
        "Background": ["Raised Christian, returning", "No faith background", "Married couple, exploring", "Recovering, seeking faith", "Catholic fiancée influencing", "Conversion from another faith", "Widow exploring deeper faith", "Recently immigrated"],
        "Stage": ["Catechesis", "Inquiry", "Catechesis", "Inquiry", "Catechesis", "Inquiry", "Enlightenment", "Inquiry"],
        "Sponsor/Mentor": ["Tom", "Grace", "Fr. Steve", "Fr. Emmanuel", "Sister Mary", "Tom", "Patricia (self)", "Luis Sr."]
    })
    st.dataframe(rcia, use_container_width=True)

with tab3:
    st.markdown("## Youth Formation (Teens)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Middle School (6-8th)")
        st.markdown("""
        **Leader:** Agnes  
        **When:** Thursday 6pm  
        **Activities:** Games, faith, fun  
        **Attendance:** 12 (avg)  
        **Focus:** Belonging + identity
        """)
    
    with col2:
        st.markdown("### High School (9-12th)")
        st.markdown("""
        **Leaders:** Tom + Grace  
        **When:** Friday 7pm  
        **Activities:** Deeper faith, socials  
        **Attendance:** 18 (avg)  
        **Focus:** Vocation + purpose
        """)
    
    with col3:
        st.markdown("### Young Adults (18-25)")
        st.markdown("""
        **Leader:** Marcus (peer-led)  
        **When:** Sunday 5pm  
        **Activities:** Dine + discuss  
        **Attendance:** 9 (avg)  
        **Focus:** Faith + career
        """)
    
    st.markdown("---")
    st.markdown("### Youth Service Projects (This Quarter)")
    
    projects = pd.DataFrame({
        "Project": ["Food Pantry Day", "Habitat for Humanity", "Prison Letter Writing", "Tutoring at School"],
        "Youth Involved": [22, 8, 15, 6],
        "Hours": [44, 24, 3, 18],
        "Impact": ["200 meals packed", "3 families housed", "50 letters received by inmates", "6 kids improved grades"],
        "Learning": ["Seeing poverty up close", "Building = serving", "Justice + relationship", "Mentoring younger kids"]
    })
    st.dataframe(projects, use_container_width=True)

with tab4:
    st.markdown("## Adult Formation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sunday Bible Study")
        st.markdown("""
        **Time:** Sunday 10:30am (after 9am Mass)  
        **Leader:** Fr. Emmanuel  
        **Topic:** Gospel of Mark (8-week series)  
        **Enrollment:** 12 adults  
        **Attendance:** 9 avg (75%)  
        **Cost:** Free (coffee provided)
        """)
    
    with col2:
        st.markdown("### Thursday Evening Reflection")
        st.markdown("""
        **Time:** Thursday 7pm  
        **Leader:** Sister Mary  
        **Topic:** Contemplative prayer + Scripture  
        **Enrollment:** 8 adults  
        **Attendance:** 7 avg (88%)  
        **Cost:** Free
        """)
    
    st.markdown("---")
    st.markdown("### Adult Topics Completed (This Year)")
    
    adult_topics = pd.DataFrame({
        "Topic": ["Eucharist: Gift of Jesus", "Saints: Models of Faith", "Prayer: Speaking to God", "Justice: Gospel mandate"],
        "Dates": ["Jan 7-28", "Feb 4-11", "Feb 18-Mar 25", "Mar 3-10"],
        "Sessions": [4, 2, 6, 2],
        "Avg Attendance": [9, 8, 10, 7],
        "Resources": ["Catechism + videos", "Saint biographies", "Prayer methods", "Papal documents"]
    })
    st.dataframe(adult_topics, use_container_width=True)

with tab5:
    st.markdown("## Formation Progress Tracking")
    
    st.markdown("### Milestones & Achievements")
    
    milestones = pd.DataFrame({
        "Person/Group": [
            "Michael (RCIA)",
            "Emma (7th grade catechesis)",
            "High School Group",
            "Adult Bible Study Group"
        ],
        "Milestone": [
            "Completed Month 1 (Inquiry)",
            "Received First Communion",
            "Served 100 volunteer hours",
            "Finished Gospel of Mark study"
        ],
        "Date": ["Feb 15", "Feb 18", "Feb 20", "Feb 24"],
        "Celebration": [
            "Class gathering + blessing",
            "Party + family dinner",
            "Certificate + pizza celebration",
            "Potluck dinner + reflection"
        ]
    })
    st.dataframe(milestones, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Spiritual Growth Indicators")
    
    fig = go.Figure(data=[
        go.Bar(x=["Know Faith", "Live Faith", "Share Faith", "Grow in Prayer", "Serve Others"],
               y=[72, 58, 45, 68, 62],
               marker_color=['#42A5F5', '#66BB6A', '#FFA726', '#AB47BC', '#EC407A'])
    ])
    fig.update_layout(title="Formation Goals (% of participants report growth)", height=300)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.info("""
📚 **Formation is how faith deepens with time.**

From children asking "Who is God?" to adults discovering prayer, from teens finding purpose to immigrants being welcomed into the Church—formation is the systematic, loving transmission of our Catholic faith.

Tracking ensures:
- No one is left behind (everyone has access to learning)
- Progress is visible (celebration of growth)
- Leaders are supported (knowing how many to prepare for)
- Youth see faith is alive (taught by adults living it)

**This is how the Church ensures faith survives for generations.**
""")
