"""
Catholic Network Tools — Justice & Advocacy
Coordinate campaigns, organize action, measure impact
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Justice & Advocacy", layout="wide")

st.title("⚖️ Justice & Advocacy Campaigns")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Campaigns", "5", "23 parishioners involved")
with col2:
    st.metric("Actions Taken", "89", "Letters written to parliament")
with col3:
    st.metric("Benefited", "3,047", "Agricultural workers")

st.markdown("---")

# Campaign selector
selected_campaign = st.selectbox("View campaign",
    ["Living Wage for Agricultural Workers", "Refugee Rights", "Climate Justice", "Education Access", "Healthcare Reform"])

st.markdown(f"## {selected_campaign}")

# Campaign details
if selected_campaign == "Living Wage for Agricultural Workers":
    st.markdown("""
    ### Campaign Brief
    
    **Goal:** Tea farm workers in Kenya earn 25% more + improved working conditions
    
    **Why it matters:** 
    - Current wage: 3,000 KES/month (unsustainable for family of 4)
    - Living wage: 5,200 KES/month
    - 3,000+ workers affected across Rift Valley
    - *"Whatever you do for the least of these, you do for me." (Matthew 25)*
    
    **Our Role:**
    - Pressurize tea companies + government
    - Educate parishioners on labor rights
    - Coordinate with farmworker unions
    - Document success + celebrate wins
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Campaign Status: 🟡 In Progress")
        st.markdown("""
        - **Started:** Jan 2024
        - **Target company:** Kericho Tea Ltd
        - **Current wage:** 3,000 KES
        - **Demanded wage:** 5,200 KES
        - **Expected outcome:** Wage negotiation in April 2024
        """)
    
    with col2:
        st.markdown("### Parishioner Involvement")
        participants = pd.DataFrame({
            "Action": ["Letters to CEO", "Rallies attended", "Social media shares", "Education talks"],
            "People": [89, 23, 156, 47]
        })
        st.dataframe(participants, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Actions Taken")
    
    actions = pd.DataFrame({
        "Date": ["Jan 15", "Jan 22", "Feb 5", "Feb 19", "Mar 12"],
        "Action": [
            "Town hall: 23 parishioners learned about tea worker wages",
            "Letter-writing campaign: 89 letters sent to CEO",
            "Rally at parliament: 23 joined farmworker march",
            "Social media campaign: 156 shares, 2,400 views",
            "Media appearance: Fr. Emmanuel interviewed on Catholic radio"
        ],
        "Impact": [
            "Knowledge ↑",
            "Pressure on company ↑",
            "Visibility ↑",
            "Public awareness ↑",
            "Faith leaders credibility ↑"
        ],
        "Follow-up Needed": ["None", "Track CEO response", "Document participant stories", "Share wins on social", ""]
    })
    st.dataframe(actions, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### How to Participate")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **📝 Write a Letter**
        - Template provided
        - Takes 10 min
        - Make your voice heard
        """)
        if st.button("Open letter template"):
            st.markdown("""
            ---
            Dear [CEO Name],
            
            As a member of [Parish Name], I'm writing about your company's wage practices.
            
            Tea workers earn 3,000 KES/month—below living wage. With family to support, they live in poverty while producing your profit.
            
            I urge you to:
            1. Increase wages to 5,200 KES/month
            2. Improve working conditions
            3. Recognize farmworker unions
            
            This is a moral issue. Catholics believe work deserves fair wages.
            
            Sincerely,
            [Your Name]
            ---
            """)
    
    with col2:
        st.markdown("""
        **🤝 Join a Rally**
        - Next rally: April 8 (parliament)
        - Transportation provided
        - 23 parishioners attending
        - Bring signs + voices
        """)
        if st.button("RSVP for April 8 rally"):
            st.success("✅ You're registered! See you April 8.")
    
    with col3:
        st.markdown("""
        **💬 Share on Social Media**
        - Posts provided (no writing needed)
        - Use #JustWagesKE
        - Tag @KeriochoTea
        - Reach: 2,400+ people so far
        """)
        if st.button("Share pre-written posts"):
            st.markdown("""
            Post 1: "My faith calls me to justice. Tea workers earn 3,000 KES/month. That's poverty wages. @KeriochoTea, pay them fairly. #JustWagesKE"
            
            Post 2: "3,000 workers depend on tea farming. Their wages are below living expenses. Let's organize for dignity. #JustWagesKE"
            """)

st.markdown("---")

st.markdown("### Cross-Parish Solidarity")

solidarity = pd.DataFrame({
    "Parish": [
        "Consolata Shrine (Nairobi)",
        "All Saints (Virginia)",
        "St. John (São Paulo, Brazil)",
        "Santa María (Mexico City)"
    ],
    "Campaign": ["Living Wage", "Living Wage", "Child Labor in Coffee", "Living Wage"],
    "Participants": [89, 47, 34, 156],
    "Actions": ["Letters", "Letters + Rallies", "Petitions", "Education + Advocacy"]
})
st.dataframe(solidarity, use_container_width=True)

st.markdown("""
**Global solidarity in action.** Four parishes on three continents, organized through one platform, 
advocating for workers' dignity. When Nairobi farmers win, they celebrate with Virginia. When Brazil 
coffee farmers succeed, Mexico learns and amplifies.

This is **The Church witnessing to justice globally.**
""")

st.markdown("---")

# All campaigns overview
st.markdown("### All Active Campaigns")

campaigns = pd.DataFrame({
    "Campaign": [
        "Living Wage for Agricultural Workers",
        "Refugee Rights & Legal Protection",
        "Climate Justice (Divestment)",
        "Education Access (Subsidy)",
        "Healthcare Reform (Affordable)"
    ],
    "Goal": [
        "5,200 KES wage for 3,000 workers",
        "Legal aid + housing for 150 families",
        "Diocese divests from fossil fuels",
        "1,000 children access free tutoring",
        "Free clinic for 500 low-income"
    ],
    "Parishes": [4, 7, 12, 3, 5],
    "Parishioners": [196, 287, 543, 89, 167],
    "Status": ["🟡 Negotiating", "🟢 Winning", "🟡 In Progress", "🟡 Organizing", "🟢 Clinic Open"],
    "Impact": ["TBD (April)", "56 families housed", "100M divested", "$0 so far", "2,300 served"]
})
st.dataframe(campaigns, use_container_width=True)

st.markdown("---")

st.markdown("### Justice Wins (This Year)")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.success("✅ Refugee Legal Aid\n\n56 families housed")
with col2:
    st.success("✅ Divestment\n\n$100M from fossil fuels")
with col3:
    st.success("✅ Fair Trade Coffee\n\n45 farms certified")
with col4:
    st.success("✅ Prison Ministry\n\n8 men in reentry program")

st.markdown("---")

st.markdown("### How Justice Work Strengthens Faith")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **Without this platform:**
    - Justice work is invisible (no one knows what's happening)
    - Efforts are fragmented (parishes don't coordinate)
    - Impact is unknown (did we win? How many benefited?)
    - Youth never see faith in action
    - Givers don't see where donations go
    
    Result: Justice feels optional, not core to faith.
    """)

with col2:
    st.markdown("""
    **With this platform:**
    - Justice is visible (dashboards show wins)
    - Parishes amplify power (89 + 47 + 34 + 156 = global force)
    - Impact is clear (3,000 workers won 25% wage increase)
    - Youth see faith come alive
    - Givers celebrate concrete wins
    
    Result: **Justice is lived discipleship.**
    """)

st.info("""
**"Seek justice, love mercy, walk humbly with your God." (Micah 6:8)**

This platform makes that possible at scale. Globally. Together.
""")
