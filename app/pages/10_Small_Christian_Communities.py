"""
Small Christian Communities (SCCs) - Catholic Spiritual OS

Manage and coordinate Small Christian Communities, the foundational
pastoral structure for parishes in Eastern Africa.

Kenya has 45,000+ SCCs as the primary way of "being Church" at grassroots.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.spiritual_os.domain.scc import (
    SmallChristianCommunity,
    Zone,
    SCCMinistry,
    MeetingFrequency,
    DEMO_SCC,
    DEMO_ZONE
)

# Page config
st.set_page_config(
    page_title="Small Christian Communities | Catholic Spiritual OS",
    page_icon="✝️",
    layout="wide"
)

# Data mode indicator
st.info("📊 **Data Mode**: DEMO — Sample SCC data for demonstration", icon="ℹ️")

st.title("👥 Small Christian Communities (SCCs)")

st.markdown("""
**Small Christian Communities** are the heart of parish life in Eastern Africa. These neighborhood-based 
groups of 10-20 families meet weekly for prayer, scripture reflection, and social action.

*"We have to insist on building church life and work on Basic Christian Communities in both rural and urban areas."*  
— AMECEA Study Conference, Nairobi, 1973
""")

# ============================================================================
# PARISH SCC OVERVIEW
# ============================================================================

st.header("Parish Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Active SCCs",
        value="8",
        delta="+2 this year"
    )

with col2:
    st.metric(
        label="Total Families",
        value="120"
    )

with col3:
    st.metric(
        label="Weekly Meetings",
        value="8"
    )

with col4:
    st.metric(
        label="Zones",
        value="1"
    )

st.divider()

# ============================================================================
# ZONE VIEW
# ============================================================================

st.header("Zones")

with st.expander(f"🗺️ {DEMO_ZONE.name} — {DEMO_ZONE.scc_count} SCCs"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Coordinator**: {DEMO_ZONE.coordinator_name}  
        **Contact**: {DEMO_ZONE.coordinator_contact}  
        **Geographic Area**: {DEMO_ZONE.geographic_area}
        """)
    
    with col2:
        st.markdown(f"""
        **Total Families**: {DEMO_ZONE.total_families}  
        **SCCs**: {DEMO_ZONE.scc_count}  
        **Established**: {DEMO_ZONE.established_date.strftime('%B %Y')}
        """)

st.divider()

# ============================================================================
# SCC DIRECTORY
# ============================================================================

st.header("SCC Directory")

# Sample SCC card
with st.container():
    st.subheader(f"✝️ {DEMO_SCC.name}")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown(f"""
        **Location**: {DEMO_SCC.location_description}  
        **Meeting Place**: {DEMO_SCC.meeting_place}  
        **Neighborhood**: {DEMO_SCC.neighborhood}
        """)
    
    with col2:
        st.markdown(f"""
        **Coordinator**: {DEMO_SCC.coordinators[0].name}  
        **Contact**: {DEMO_SCC.contact_phone}  
        **Established**: {DEMO_SCC.established_date.strftime('%B %Y')}
        """)
    
    with col3:
        st.markdown(f"""
        **Families**: {DEMO_SCC.family_count}  
        **Members**: {DEMO_SCC.active_members_count}  
        **Youth**: {DEMO_SCC.youth_count}
        """)
    
    # Meeting schedule
    st.markdown("### 📅 Meeting Schedule")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Every {DEMO_SCC.meeting_day}** at {DEMO_SCC.meeting_time.strftime('%I:%M %p')}")
    
    with col2:
        if DEMO_SCC.last_meeting_date:
            st.write(f"**Last Meeting**: {DEMO_SCC.last_meeting_date.strftime('%b %d, %Y')}")
    
    with col3:
        if DEMO_SCC.upcoming_meeting_date:
            st.success(f"**Next**: {DEMO_SCC.upcoming_meeting_date.strftime('%b %d, %Y')}")
    
    # Ministries
    st.markdown("### 🎯 Active Ministries")
    
    ministry_display = {
        SCCMinistry.PRAYER: "🙏 Prayer & Worship",
        SCCMinistry.SOCIAL_ACTION: "🤝 Social Action",
        SCCMinistry.FORMATION: "📚 Faith Formation",
        SCCMinistry.EVANGELIZATION: "📢 Evangelization",
        SCCMinistry.YOUTH: "👦 Youth Ministry",
        SCCMinistry.FAMILY: "👨‍👩‍👧‍👦 Family Ministry"
    }
    
    ministry_cols = st.columns(len(DEMO_SCC.active_ministries))
    for idx, ministry in enumerate(DEMO_SCC.active_ministries):
        with ministry_cols[idx]:
            st.write(ministry_display.get(ministry, ministry.value))
    
    # Social projects
    if DEMO_SCC.social_projects:
        st.markdown("### 🌍 Social Action Projects")
        for project in DEMO_SCC.social_projects:
            st.write(f"- {project}")
    
    # Reflection method
    st.markdown("### 📖 Scripture Reflection Method")
    
    if DEMO_SCC.uses_lumko_method:
        st.success(f"✅ Uses {DEMO_SCC.scripture_reflection_method}")
        
        with st.expander("Learn about the 7-Step Lumko Method"):
            st.markdown("""
            The **Lumko Method** is the most popular scripture reflection structure for SCCs in Africa:
            
            1. **Welcome & Opening Prayer** — Create a prayerful atmosphere
            2. **Psalm or Hymn** — Praise God together
            3. **Gospel Reading** — Read the scripture passage (usually Sunday's Gospel)
            4. **Meditation in Silence** — Allow the Word to speak to hearts
            5. **Sharing Reflections** — "What does this passage say to me/us?"
            6. **Action Commitment** — "What will we do this week because of this Word?"
            7. **Closing Prayer & Sending** — Go forth to live the Gospel
            
            **Why this works**: Combines listening to God's Word with practical action in daily life.
            """)
    else:
        st.info(f"Uses: {DEMO_SCC.scripture_reflection_method}")

st.divider()

# ============================================================================
# SCC COORDINATOR RESOURCES
# ============================================================================

st.header("Coordinator Resources")

tab1, tab2, tab3 = st.tabs(["📋 Meeting Planning", "📚 Reflection Guides", "📊 Reports"])

with tab1:
    st.markdown("### Weekly Meeting Checklist")
    
    st.markdown("""
    **Before the Meeting**:
    - [ ] Confirm meeting location and time
    - [ ] Review Sunday's Gospel reading
    - [ ] Prepare reflection questions
    - [ ] Send reminder to all members
    - [ ] Arrange for refreshments (if rotating)
    
    **During the Meeting**:
    - [ ] Welcome and opening prayer (5 min)
    - [ ] Hymn or psalm (5 min)
    - [ ] Gospel reading (2 min)
    - [ ] Silent meditation (5 min)
    - [ ] Sharing and reflection (30 min)
    - [ ] Action commitment (10 min)
    - [ ] Announcements and prayer requests (5 min)
    - [ ] Closing prayer (3 min)
    
    **Total Time**: ~65 minutes
    
    **After the Meeting**:
    - [ ] Note action commitments
    - [ ] Record attendance
    - [ ] Follow up on prayer requests
    - [ ] Plan next meeting logistics
    """)

with tab2:
    st.markdown("### This Sunday's Reflection Guide")
    
    # In production, this would pull from liturgical calendar
    st.info("📅 This week: Connect to Liturgy of the Day page for Sunday's Gospel")
    
    st.markdown("""
    **Reflection Questions** (adapt to your community):
    
    1. **Listen**: What word or phrase from this Gospel catches your attention?
    2. **Understand**: What is Jesus teaching or revealing in this passage?
    3. **Apply**: Where do you see this playing out in your life right now?
    4. **Act**: What is one concrete thing you/we can do this week in response?
    5. **Share**: Who needs to hear this message? How can we share it?
    """)

with tab3:
    st.markdown("### Activity Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Meetings This Year", DEMO_SCC.meetings_this_year)
        st.metric("Average Attendance", "85%")
        st.metric("Social Projects Active", len(DEMO_SCC.social_projects))
    
    with col2:
        st.write("**Most Recent Activities**:")
        st.write("- Feb 6: Weekly meeting (24 attendees)")
        st.write("- Feb 3: Food bank collection")
        st.write("- Jan 30: Weekly meeting (22 attendees)")
        st.write("- Jan 28: Visit to elderly parishioners")

st.divider()

# ============================================================================
# FORMING NEW SCCs
# ============================================================================

st.header("Starting a New SCC")

with st.expander("📘 Guide to Forming a New Small Christian Community"):
    st.markdown("""
    ### Step 1: Discernment & Prayer (Weeks 1-2)
    - Pray about forming an SCC in your neighborhood
    - Talk to your parish priest for blessing and guidance
    - Identify 3-5 families interested in joining
    
    ### Step 2: Initial Gathering (Week 3)
    - Host an informal gathering at someone's home
    - Share the vision of SCCs
    - Discuss meeting schedule and location
    - Agree on scripture reflection method
    
    ### Step 3: First Official Meetings (Weeks 4-8)
    - Meet weekly to establish rhythm
    - Keep meetings simple: prayer, Gospel, sharing
    - Rotate meeting locations among families
    - Build trust and community bonds
    
    ### Step 4: Structure & Leadership (Weeks 9-12)
    - Select coordinator and other roles
    - Register with parish as official SCC
    - Join parish zone structure
    - Begin outreach to neighbors
    
    ### Step 5: Mission & Growth (Ongoing)
    - Identify a social action project
    - Invite new families to join
    - Connect with other SCCs in zone
    - Participate in parish-wide SCC events
    
    **Remember**: Start small, pray consistently, act charitably. The rest will follow!
    """)

st.divider()

# ============================================================================
# RESOURCES
# ============================================================================

st.header("Additional Resources")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📚 Formation Materials")
    st.markdown("""
    - **Lumko Institute** (South Africa): Scripture reflection methods
    - **AMECEA Pastoral Institute** (Kenya): SCC leadership training
    - **Catholic Diocese Resources**: Local formation programs
    - **Jesuit Centre for Theological Reflection** (Zambia): Justice & peace guides
    """)

with col2:
    st.markdown("### 🌍 Network Connections")
    st.markdown("""
    - **Kenya Catholic SCCs**: 45,000+ communities nationwide
    - **AMECEA Region**: 160,000+ SCCs across Eastern Africa
    - **Global SCCs**: Networks in Asia, Latin America, Africa
    - **World Church**: Parish-based community movements
    """)

st.info("""
**Note**: Small Christian Communities are also called Basic Christian Communities (BCCs), 
Basic Ecclesial Communities, or Neighborhood Faith Communities in different regions.
""")

st.markdown("---")
st.caption("Catholic Spiritual OS | [GitHub](https://github.com/gabrielmahia/catholic-network-tools) | CC BY-NC-ND 4.0")
