"""
Catholic Network Tools — Stewardship & Giving
Track donations, budgets, impact, volunteer hours, financial transparency
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Stewardship", layout="wide")

st.title("💰 Stewardship & Giving")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Giving This Month", "$8,347", "+8% from last month")
with col2:
    st.metric("Active Donors", "67", "+5 new this month")
with col3:
    st.metric("Volunteer Hours", "284", "+50 from last week")
with col4:
    st.metric("Pledges Fulfilled", "98%", "Very high engagement")

st.markdown("---")

st.markdown("## 💚 Where Your Donation Goes")

col1, col2 = st.columns([2, 1])

with col1:
    # Budget allocation
    fig = go.Figure(data=[
        go.Pie(
            labels=["Food Pantry", "Formation", "Building", "Staff", "Justice Work", "Other"],
            values=[2100, 2500, 1500, 1200, 900, 147],
            marker=dict(colors=['#66BB6A', '#42A5F5', '#AB47BC', '#FFA726', '#EF5350', '#78909C']),
            textposition='inside',
            textinfo='label+percent'
        )
    ])
    fig.update_layout(title="Budget Allocation ($8,347 this month)", height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    ### What Each Dollar Does
    
    **$1.00 donated:**
    - $0.25 → Food (87 fed/week)
    - $0.30 → Formation (99 people learning faith)
    - $0.18 → Building (maintained, safe)
    - $0.14 → Staff (pastoral care)
    - $0.11 → Justice (advocacy, organizing)
    - $0.02 → Admin
    
    **Total served:** 487 parishioners  
    **Plus 2,300 in material aid/year**
    """)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Make a Donation", "Giving Stories", "Volunteer Hours", "Budget Transparency"])

with tab1:
    st.markdown("## Make a Donation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input("Donation amount", min_value=1, value=50)
        currency = st.selectbox("Currency", ["KES (Kenya)", "USD (USA)", "EUR (Europe)", "BRL (Brazil)"])
        
        allocation = st.multiselect(
            "Where should this donation go?",
            ["Food Pantry", "Formation", "Building", "Justice Work", "General Fund"],
            default=["General Fund"]
        )
    
    with col2:
        st.markdown("### Donation Options")
        st.markdown("""
        - 💳 **One-time donation** (credit card, mobile money)
        - 📅 **Monthly pledge** (automatic withdrawal)
        - 🎁 **Special gifts** (memory of loved one, in honor of)
        - 📊 **Workplace giving** (payroll deduction)
        """)
    
    if st.button(f"Donate {amount}"):
        st.success(f"""
        ✅ Thank you for your generosity!
        
        Your donation of {amount} (allocated to {', '.join(allocation)}) strengthens our parish.
        
        You'll receive:
        - Donation receipt (for tax purposes)
        - Impact report (see where your gift goes)
        - Invitation to quarterly gratitude celebration
        """)

with tab2:
    st.markdown("## Stories of Generosity & Impact")
    
    stories = pd.DataFrame({
        "Name": ["Maria", "Tom's Family", "Sofia & Luis", "Justice Team", "Youth Group"],
        "Gift": ["Monthly prayer + meal prep", "$100/month to food pantry", "Wedding gift to parish", "Justice campaign donations", "Pizza sale fundraiser"],
        "Impact": ["23 homebound visited/month", "200 meals for hungry", "Building repairs completed", "$847 for advocacy", "$340 for youth retreat"],
        "Story": [
            "Maria visits Mrs. Nyambura weekly + brings soup. 'My faith comes alive when I serve.'",
            "Tom's family commits 10% to food pantry. 'We've been blessed. Now we bless others.'",
            "Instead of gifts, Sofia & Luis asked guests to contribute to parish. 'Our love multiplied.'",
            "Justice team raises funds for advocacy. '3,000 workers earned 25% more wages because we gave.'",
            "Teens sell pizza. 'We earned $340 for our mission trip + helped our church.'",
        ]
    })
    
    for idx, row in stories.iterrows():
        st.markdown(f"""
        ### {row['Name']}
        **Gift:** {row['Gift']}  
        **Impact:** {row['Impact']}
        
        *{row['Story']}*
        
        ---
        """)

with tab3:
    st.markdown("## Volunteer Hours (Valued Service)")
    
    st.markdown("### Volunteer Time Valued at Local Wage Rate")
    
    volunteer_hours = pd.DataFrame({
        "Service": ["Food Pantry", "Tutoring", "Homebound Visits", "Youth Ministry", "Building/Maintenance", "Office Admin"],
        "Hours/Month": [44, 18, 23, 36, 12, 8],
        "Avg Wage": ["$10/hr", "$25/hr", "$15/hr", "$15/hr", "$20/hr", "$18/hr"],
        "Monthly Value": ["$440", "$450", "$345", "$540", "$240", "$144"],
        "Annual Value": ["$5,280", "$5,400", "$4,140", "$6,480", "$2,880", "$1,728"]
    })
    st.dataframe(volunteer_hours, use_container_width=True)
    
    st.markdown("""
    ---
    **Total Volunteer Contribution This Month:** 141 hours = **$2,159 in value**
    
    **Annual Volunteer Stewardship:** 1,692 hours = **$25,908 in value**
    
    *This doesn't include pray time, emotional labor, or the intangible value of community strengthened.*
    """)

with tab4:
    st.markdown("## Budget Transparency")
    
    st.markdown("### Complete Budget (2024)")
    
    budget = pd.DataFrame({
        "Category": [
            "Food Pantry & Material Aid",
            "Formation (Catechesis, RCIA, Youth)",
            "Building (Mortgage, Utilities, Maintenance)",
            "Staff (Pastoral Associates, Admin)",
            "Justice & Advocacy",
            "Prayer & Liturgy Supplies",
            "Insurance & Compliance",
            "Administrative"
        ],
        "Budgeted": ["$28,000", "$32,000", "$18,000", "$15,000", "$10,000", "$3,000", "$2,000", "$2,000"],
        "YTD Spent": ["$6,200", "$7,400", "$3,800", "$2,800", "$1,900", "$600", "$350", "$297"],
        "% of Budget": ["22%", "23%", "21%", "19%", "19%", "20%", "18%", "15%"],
        "On Track": ["✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"]
    })
    st.dataframe(budget, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Stewardship Council Decision-Making")
    
    st.markdown("""
    **Q1 Decision:** "We're spending well on material aid (food) but need to boost formation. 
    Proposal: Increase youth ministry stipend by $200/month."
    
    **Q2 Decision:** "Justice advocacy is underfunded. If we get $500 in additional gifts, 
    we'll fund a full-time community organizer position."
    
    **Q3 Decision:** "Building needs roof repair ($8,000). Let's do a capital campaign 
    rather than drain operating budget. 'Roof Campaign' goal: $10,000."
    """)

st.markdown("---")

st.info("""
💚 **Stewardship is a spiritual discipline.**

Money reflects values. Transparency builds trust. When you give, you're not just funding a budget—you're voting 
for the parish's priorities. When you see your donation fed 12 hungry people, your faith is strengthened.

This platform makes all of that visible + intentional.

**What would change if every parishioner could see where their $50 donation went?**
""")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Questions About Giving?")
    st.markdown("""
    - How do I start giving?
    - Can I earmark my donation?
    - Is my giving confidential?
    - How do I see impact reports?
    """)

with col2:
    st.markdown("### Answer:")
    st.markdown("""
    Email: stewardship@parish.org  
    Or speak with our Stewardship Coordinator  
    **All donations are confidential (unless you request recognition)**
    """)
