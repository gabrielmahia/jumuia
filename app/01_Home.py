"""
Catholic Network Tools — Home Dashboard
Shows parish overview across all 7 dimensions
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Catholic Network Tools", layout="wide", initial_sidebar_state="expanded")

# Page styling
st.markdown("""
    <style>
    .main { padding: 0px; }
    .dimension-card {
        border-left: 5px solid #2E7D32;
        padding: 20px;
        margin: 10px 0;
        border-radius: 5px;
        background: #F1F8F6;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar: Parish selector + user profile
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1549525240-0a6c29835ce2?w=100", width=100)
    st.markdown("### 🙏 Your Parish")
    parish = st.selectbox(
        "Select parish",
        ["Consolata Shrine, Westlands", "All Saints, Virginia", "St. Mary, Kinshasa"],
        label_visibility="collapsed"
    )
    
    role = st.radio("Your role", ["Parishioner", "Pastoral Team", "Finance Council", "Bishop"])
    
    st.divider()
    st.markdown("### ⚙️ Menu")
    st.markdown("""
    - 🛐 Sacraments
    - 🍞 Material Aid
    - 👥 Pastoral Care
    - ⚖️ Justice
    - 👦 Formation
    - 💰 Stewardship
    - 📋 Admin
    """)

# Main dashboard
st.title("⛪ Catholic Network Tools")
st.markdown(f"**{parish}** — Dashboard for {datetime.now().strftime('%B %Y')}")

st.markdown("---")

# Key metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Parishioners Active", "487", "+12% this month")
with col2:
    st.metric("🛐 Sacraments This Month", "12", "5 baptisms, 2 marriages")
with col3:
    st.metric("🤝 Volunteer Hours", "284", "+50% this quarter")
with col4:
    st.metric("💚 Giving This Month", "$8,347", "+8%")

st.markdown("---")

# The 7 Dimensions
st.markdown("## 7 Dimensions of Parish Life")

# Row 1: Spiritual + Material + Community
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🛐 Spiritual
    **Sacraments & Prayer**
    - 5 baptisms this month
    - 2 marriages prepared
    - 12 prayer intentions active
    - 23 people in prayer circles
    
    [→ View Sacraments](./02_Sacraments)
    """)

with col2:
    st.markdown("""
    ### 🍞 Material
    **Serve the Least**
    - 87 people fed this week
    - 12 families in emergency aid
    - 3 tutoring groups active
    - 5 volunteers at food pantry
    
    [→ View Material Aid](./pages/02_Material)
    """)

with col3:
    st.markdown("""
    ### 👥 Community
    **Pastoral Care**
    - 23 homebound visited this week
    - 8 people in grief groups
    - 12 marriages in prep
    - 47 new members welcomed
    
    [→ View Pastoral Care](./pages/03_Pastoral)
    """)

# Row 2: Justice + Formation + Stewardship
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### ⚖️ Justice
    **Advocacy & Organizing**
    - 23 on living wage campaign
    - 89 letters written to parliament
    - 2 rallies organized
    - 3,047 workers benefited
    
    [→ View Campaigns](./pages/04_Justice)
    """)

with col2:
    st.markdown("""
    ### 👦 Formation
    **Education & Growth**
    - 34 in catechesis classes
    - 8 in RCIA (6-month program)
    - 47 in youth groups
    - 12 in adult Bible study
    
    [→ View Formation](./pages/05_Formation)
    """)

with col3:
    st.markdown("""
    ### 💰 Stewardship
    **Giving with Impact**
    - $8,347 given this month
    - 23 donors tracked
    - 30% to food pantry
    - 40% to formation
    
    [→ View Giving](./pages/06_Stewardship)
    """)

# Row 3: Admin
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    ### 📋 Admin
    **Coordination**
    - 4 Masses/week
    - 23 volunteers scheduled
    - 45 facility bookings/month
    - 0 conflicts ✓
    
    [→ View Schedule](./pages/07_Admin)
    """)

st.markdown("---")

# Recent activity
st.markdown("## Recent Activity")

activity_df = pd.DataFrame({
    "Time": ["2 hours ago", "5 hours ago", "1 day ago", "2 days ago"],
    "Activity": [
        "Maria visited Mrs. Nyambura (prayer + soup from food pantry)",
        "Fr. Emmanuel recorded 3 baptisms scheduled",
        "Justice campaign: 12 letters written to parliament",
        "Youth group: 15 attended confirmation prep"
    ],
    "Type": ["🤝 Pastoral", "🛐 Sacrament", "⚖️ Justice", "👦 Formation"]
})
st.dataframe(activity_df, use_container_width=True)

st.markdown("---")

# Stats by dimension
st.markdown("## Engagement by Dimension (% of parish)")

fig = go.Figure(data=[
    go.Bar(x=["Spiritual", "Material", "Community", "Justice", "Formation", "Stewardship", "Admin"],
           y=[65, 48, 52, 23, 34, 67, 89],
           marker_color=['#2E7D32', '#FFA726', '#AB47BC', '#EF5350', '#42A5F5', '#66BB6A', '#78909C'])
])
fig.update_layout(title="Parish Engagement (% active in each dimension)",
                  xaxis_title="Dimension", yaxis_title="% Engaged",
                  height=300, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Call to action
st.markdown("""
## Ready to Get Involved?

Choose how you want to participate:

| I Want To... | Start Here |
|---|---|
| **Pray** | Join prayer circle (→ Spiritual) |
| **Serve** | Volunteer (→ Material or Community) |
| **Advocate** | Join justice campaign (→ Justice) |
| **Learn** | Register for catechesis (→ Formation) |
| **Give** | Make donation (→ Stewardship) |
| **Lead** | Join a team (→ Admin) |

""")

# Footer
st.divider()
st.markdown("""
*Built for parishes by parishes. Global community. Local impact. GitHub-powered. Streamlit-deployed. 100% free forever.*

[💬 Feedback](https://github.com/gabrielmahia/catholic-network-tools/discussions) | 
[📚 Documentation](https://github.com/gabrielmahia/catholic-network-tools/tree/main/docs) |
[🙏 Prayer Request](mailto:contact@aikungfu.dev)
""")
