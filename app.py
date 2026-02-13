"""
Catholic Spiritual OS - Nested Architecture
Single app, five lenses: Personal → Parish → Diocese → Global → Crisis

Like Google Maps: Zoom in/out to see different levels of detail
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.spiritual_os.models import (
    User, Parish, Diocese, JusticeCampaign, CrisisEvent,
    UserRole, PermissionContext
)
from src.spiritual_os.aggregation import AggregationEngine, QueryBuilder

# Configure page
st.set_page_config(
    page_title="Catholic Spiritual OS",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .lens-container {
        border-left: 5px solid #2E7D32;
        padding: 20px;
        margin: 10px 0;
        border-radius: 5px;
        background: #F1F8F6;
    }
    .lens-header {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #1B5E20;
    }
    .zoom-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        margin: 5px;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "user" not in st.session_state:
    st.session_state.user = None
if "current_lens" not in st.session_state:
    st.session_state.current_lens = "personal"
if "crisis_active" not in st.session_state:
    st.session_state.crisis_active = False

# Sample data for demo
DEMO_USER = User(
    id="user_001",
    name="John Smith",
    email="john@example.com",
    role=UserRole.INDIVIDUAL,
    parish_id="parish_001",
    diocese_id="diocese_001",
    opt_in_to_parish_aggregates=True,
    opt_in_to_diocese_aggregates=False,
)

DEMO_PARISH = Parish(
    id="parish_001",
    name="St. Mary's Parish",
    diocese_id="diocese_001",
    coordinator_id="coord_001",
    aggregated_members_count=487,
    aggregated_formation_participants=342,
    aggregated_avg_practice_minutes=23.0,
    aggregated_volunteer_count=45,
)

DEMO_DIOCESE = Diocese(
    id="diocese_001",
    name="Diocese of Springfield",
    bishop_name="Bishop Michael",
    region="Midwest USA",
    aggregated_parishes_count=50,
    aggregated_total_catholics=98000,
    aggregated_weekly_attendance=34000,
    aggregated_formation_participants=16800,
    aggregated_workers_helped=26000,
    aggregated_policy_wins=3,
)

DEMO_CAMPAIGN = JusticeCampaign(
    id="campaign_001",
    name="Living Wage East Africa",
    campaign_type="living_wage",
    dioceses_joined=["diocese_kenya_001", "diocese_uganda_001"],
    parishes_joined_count=250,
    aggregated_workers_affected=26000,
    aggregated_wage_increase_percent=26.0,
    aggregated_income_increase_dollars=45000000,
    aggregated_policy_wins=3,
)

DEMO_CRISIS = CrisisEvent(
    id="crisis_001",
    name="East Africa Drought",
    event_type="drought",
    location="Kenya, Uganda, Ethiopia",
    activated_at="2026-02-13",
    affected_dioceses=["diocese_kenya_001"],
    activated_parishes=["parish_nairobi_001", "parish_mombasa_001"],
    people_affected=450000,
    people_receiving_aid=45000,
    total_funds_raised=2100000,
)

# ============================================================================
# PERMISSION CHECKS
# ============================================================================

def get_permission_context() -> PermissionContext:
    """Get current user's permission context"""
    if not st.session_state.user:
        return None
    
    return PermissionContext(
        user_id=st.session_state.user.id,
        role=st.session_state.user.role,
        parish_id=st.session_state.user.parish_id,
        diocese_id=st.session_state.user.diocese_id,
    )

# ============================================================================
# LENS: PERSONAL (Individual Formation)
# ============================================================================

def show_lens_personal():
    """Personal formation lens - Your private data"""
    
    st.markdown('<div class="lens-header">🧑 Personal Spiritual OS</div>', unsafe_allow_html=True)
    st.write("Your private formation journey. Nothing here leaves your device.")
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Your Dashboard")
        st.metric("Daily Practices", "3/6 complete")
        st.metric("Current Season", "Lent")
        st.metric("Feast Day", "St. Joseph (March 19)")
    
    with col2:
        st.subheader("🛐 Sacramental Journey")
        st.write("✓ Baptism (1982)")
        st.write("✓ Confirmation (1995)")
        st.write("✓ Eucharist (weekly)")
        st.write("⏳ Reconciliation: Last 2 weeks")
    
    st.divider()
    
    tabs = st.tabs(["Rule of Life", "Journal", "Sacraments", "Prayer"])
    
    with tabs[0]:
        st.write("**Your daily practices:**")
        st.write("- ✓ Morning prayer (15 min)")
        st.write("- ✓ Scripture - Lectio Divina (20 min)")
        st.write("- ☐ Evening examen (10 min)")
        st.write("- ✓ Work of mercy (daily)")
    
    with tabs[1]:
        st.write("**Today's evening examen:**")
        st.text_area("Your reflection:", value="Where did I feel God's grace today?", height=150)
    
    with tabs[2]:
        st.write("**Sacramental milestones:**")
        st.write("Track your sacramental life journey")
    
    with tabs[3]:
        st.write("**Prayer practices:**")
        st.write("Customize your prayer life")
    
    st.divider()
    
    # Peek upward
    if st.session_state.user.opt_in_to_parish_aggregates:
        st.subheader("📊 Your Parish (Aggregated View)")
        st.write(f"""
        **{DEMO_PARISH.name}** - You see trends, not individuals
        - **Members**: {DEMO_PARISH.aggregated_members_count}
        - **In daily formation**: {DEMO_PARISH.aggregated_formation_participants} (70%)
        - **Average practice time**: {DEMO_PARISH.aggregated_avg_practice_minutes} min/day
        - **You're in top 15% of participants**
        """)
        
        if st.button("Zoom Out → See Parish Operations"):
            st.session_state.current_lens = "parish"
            st.rerun()

# ============================================================================
# LENS: PARISH (Operations)
# ============================================================================

def show_lens_parish():
    """Parish operations lens - Coordinator view"""
    
    st.markdown('<div class="lens-header">🏛️ Parish Operations</div>', unsafe_allow_html=True)
    st.write("Parish coordination and aggregated member view")
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Members", DEMO_PARISH.aggregated_members_count)
    with col2:
        st.metric("Volunteers", DEMO_PARISH.aggregated_volunteer_count)
    with col3:
        st.metric("In Formation", DEMO_PARISH.aggregated_formation_participants)
    with col4:
        st.metric("Avg. Daily", f"{DEMO_PARISH.aggregated_avg_practice_minutes} min")
    
    st.divider()
    
    tabs = st.tabs(["Bulletin", "Events", "Volunteers", "Justice", "Statistics"])
    
    with tabs[0]:
        st.subheader("📰 This Week's Bulletin")
        st.write("- Sunday Readings (Lent 2)")
        st.write("- Mass Schedule: Sat 5:30pm, Sun 8/10/12am")
        st.write("- Community Dinner: Thursday 6pm")
        st.write("- Living wage campaign kickoff: Next month")
    
    with tabs[1]:
        st.subheader("📅 Upcoming Events")
        st.write("- RCIA class: Tuesday 7pm (12 registered)")
        st.write("- Marriage prep: Saturday 9am (4 couples)")
        st.write("- Service day: Saturday afternoon")
    
    with tabs[2]:
        st.subheader("👥 Volunteers Available")
        st.metric("Available Now", 45)
        st.write("Skills: Food prep (12), Construction (8), Transportation (23)")
    
    with tabs[3]:
        st.subheader("✊ Justice Initiatives")
        st.write("- Living wage campaign: 23 volunteers, $4,200 donated")
        st.write("- Refugee family sponsorship: 1 family, 6 months")
        st.write("- Food pantry: 120 families/month")
    
    with tabs[4]:
        st.subheader("📈 Trends")
        st.write("- Formation participation: +8% YoY")
        st.write("- Volunteer engagement: +12% YoY")
        st.write("- Justice involvement: +15% YoY")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Zoom In to Personal"):
            st.session_state.current_lens = "personal"
            st.rerun()
    
    with col2:
        if st.button("Zoom Out → Diocese →"):
            st.session_state.current_lens = "diocese"
            st.rerun()

# ============================================================================
# LENS: DIOCESE (Governance)
# ============================================================================

def show_lens_diocese():
    """Diocese governance lens - Bishop/leader view"""
    
    st.markdown('<div class="lens-header">⛪ Diocese Governance</div>', unsafe_allow_html=True)
    st.write("Diocese-wide coordination and strategic oversight")
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Parishes", DEMO_DIOCESE.aggregated_parishes_count)
    with col2:
        st.metric("Catholics", f"{DEMO_DIOCESE.aggregated_total_catholics:,}")
    with col3:
        st.metric("Weekly Attendance", f"{DEMO_DIOCESE.aggregated_weekly_attendance:,}")
    with col4:
        st.metric("In Formation", f"{DEMO_DIOCESE.aggregated_formation_participants:,}")
    
    st.divider()
    
    tabs = st.tabs(["Overview", "Parishes", "Justice", "Transparency", "Strategic"])
    
    with tabs[0]:
        st.subheader(f"{DEMO_DIOCESE.name}")
        st.write(f"""
        **Formation**: {DEMO_DIOCESE.aggregated_formation_participants:,} people (+12% YoY)
        **Justice**: {DEMO_DIOCESE.aggregated_workers_helped:,} workers helped
        **Sacraments**: Weddings declining, need focus
        **Clergy**: 2 retirements next year, 1 ordination
        """)
    
    with tabs[1]:
        st.subheader("🗺️ Parishes in Diocese")
        st.write(f"Total: {DEMO_DIOCESE.aggregated_parishes_count}")
        st.write("Click to see aggregates (no personal data)")
    
    with tabs[2]:
        st.subheader("✊ Justice Campaigns")
        st.write("- Living wage: 12 parishes, 26,000 workers")
        st.write("  + 26% wage increase")
        st.write("- Refugee support: 8 parishes, 45 families")
        st.write("- Housing justice: 5 parishes, 120 families")
    
    with tabs[3]:
        st.subheader("📊 Bishop's Transparency Report")
        st.write("""
        **What I'm Prioritizing This Year:**
        - Formation: 16,800 people in daily prayer ✓
        - Justice: 26,000 workers getting fair wages ✓
        - Sacraments: Marriages declining, need focus
        - Vocations: Supporting 3 new priests
        
        **Challenge:** Rural parishes need more support
        """)
    
    with tabs[4]:
        st.subheader("📋 5-Year Plan")
        st.write("1. Double formation engagement")
        st.write("2. Triple justice impact")
        st.write("3. Support vocations (3 new priests)")
        st.write("4. Plant 3 new parishes")
        st.write("5. Build interfaith network")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Zoom In to Parish"):
            st.session_state.current_lens = "parish"
            st.rerun()
    
    with col2:
        if st.button("Zoom Out → Global Network →"):
            st.session_state.current_lens = "global"
            st.rerun()

# ============================================================================
# LENS: GLOBAL (Justice Coordination)
# ============================================================================

def show_lens_global():
    """Global justice network lens - Coordinator view"""
    
    st.markdown('<div class="lens-header">🌍 Global Justice Network</div>', unsafe_allow_html=True)
    st.write("Cross-diocesan justice campaigns and global impact")
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Dioceses", "47")
    with col2:
        st.metric("Parishes", "2,300")
    with col3:
        st.metric("Catholics", "1.3B")
    with col4:
        st.metric("Workers Helped", "26,000")
    
    st.divider()
    
    tabs = st.tabs(["Campaigns", "Global Impact", "Diocese Leaders", "Stories", "New Campaigns"])
    
    with tabs[0]:
        st.subheader("🌍 Active Campaigns")
        
        st.write(f"""
        **{DEMO_CAMPAIGN.name}**
        - Dioceses involved: {len(DEMO_CAMPAIGN.dioceses_joined)}
        - Parishes: {DEMO_CAMPAIGN.parishes_joined_count}
        - Workers affected: {DEMO_CAMPAIGN.aggregated_workers_affected:,}
        - Wage increase: +{DEMO_CAMPAIGN.aggregated_wage_increase_percent}%
        - Income increase: ${DEMO_CAMPAIGN.aggregated_income_increase_dollars:,}
        - Policy wins: {DEMO_CAMPAIGN.aggregated_policy_wins}
        """)
        
        st.write("---")
        st.write("**Living Wage - Latin America** (45 parishes)")
        st.write("- Workers: 8,000 | Wage increase: +18%")
        
        st.write("**Living Wage - Asia** (23 parishes)")
        st.write("- Workers: 3,000 | Wage increase: +14%")
    
    with tabs[1]:
        st.subheader("📊 Aggregate Global Impact")
        st.metric("Total Workers Helped (2026)", "26,000+")
        st.metric("Total Income Increased", "$45M+")
        st.metric("Policy Wins", "5")
        st.metric("Countries", "84")
    
    with tabs[2]:
        st.subheader("🏆 Top Dioceses by Impact")
        st.write("1. Diocese of Nairobi: 450 workers, +28%")
        st.write("2. Diocese of Manila: 380 workers, +24%")
        st.write("3. Diocese of Springfield: 260 workers, +26%")
        st.write("4. Diocese of São Paulo: 220 workers, +19%")
    
    with tabs[3]:
        st.subheader("🌟 Success Stories")
        st.write("- 'How Diocese of Nairobi achieved +28%'")
        st.write("- '5 parishes, 1 victory: Housing justice'")
        st.write("- 'From 0 to 380 workers: Manila's journey'")
    
    with tabs[4]:
        st.subheader("🚀 Pilots Being Scaled")
        st.write("- Tech ethics (AI, labor): 3 dioceses")
        st.write("- Climate justice (green jobs): 8 dioceses")
        st.write("- Debt relief (student loans): 2 dioceses")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Back to Diocese"):
            st.session_state.current_lens = "diocese"
            st.rerun()
    
    with col2:
        if "diocesan_leader" in str(st.session_state.user.role):
            if st.button("🚨 Activate Crisis Mode"):
                st.session_state.crisis_active = True
                st.rerun()
    
    with col3:
        st.write("")

# ============================================================================
# LENS: CRISIS (Emergency Response)
# ============================================================================

def show_lens_crisis():
    """Crisis response lens - Emergency coordination"""
    
    st.markdown('<div class="lens-header">🚨 CRISIS MODE - East Africa Drought</div>', unsafe_allow_html=True)
    st.write("**ACTIVE EMERGENCY** - Temporary crisis response coordination")
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Dioceses Activated", len(DEMO_CRISIS.affected_dioceses))
    with col2:
        st.metric("Volunteers", len(DEMO_CRISIS.volunteers))
    with col3:
        st.metric("People Aided", f"{DEMO_CRISIS.people_receiving_aid:,}")
    with col4:
        st.metric("Funds Raised", f"${DEMO_CRISIS.total_funds_raised:,}")
    
    st.divider()
    
    tabs = st.tabs(["Impact", "Volunteers", "Resources", "Needs", "Communication"])
    
    with tabs[0]:
        st.subheader("📊 Crisis Impact")
        st.write(f"**Location**: {DEMO_CRISIS.location}")
        st.write(f"**Type**: {DEMO_CRISIS.event_type.upper()}")
        st.write(f"**People Affected**: {DEMO_CRISIS.people_affected:,}")
        st.write(f"**Receiving Aid**: {DEMO_CRISIS.people_receiving_aid:,}")
        st.write(f"**Funds Raised**: ${DEMO_CRISIS.total_funds_raised:,}")
        st.info("⏰ Auto-purges: 90 days after resolution (Privacy by design)")
    
    with tabs[1]:
        st.subheader("👥 Volunteers Mobilized")
        st.metric("Available Now", len(DEMO_CRISIS.volunteers))
        st.write("- Medical: 340  | Logistics: 560")
        st.write("- Food prep: 450  | Childcare: 280")
        st.write("- Construction: 190  | Translation: 45")
    
    with tabs[2]:
        st.subheader("📦 Resources")
        st.write("**Donated:**")
        st.write("- Food kits: 2,300 packages")
        st.write("- Water filters: 450")
        st.write("- Medical supplies: $85k")
        st.write("- Cash donations: $2.1M")
    
    with tabs[3]:
        st.subheader("🆘 Needs Assessment")
        st.write("**CRITICAL:**")
        st.write("- Food: 15,000 families")
        st.write("- Water: 8,000 families")
        st.write("- Medical: 3,200 people")
    
    with tabs[4]:
        st.subheader("💬 Real-Time Updates")
        st.write("- ✓ Water shipment arriving tomorrow, Kisumu")
        st.write("- ✓ Need 20 volunteers for Mombasa clinic")
        st.write("- ✓ Food distribution schedule updated")
    
    st.divider()
    
    if st.button("← Exit Crisis Mode"):
        st.session_state.crisis_active = False
        st.rerun()

# ============================================================================
# MAIN APP LOGIC
# ============================================================================

def main():
    """Main app logic"""
    
    # Header
    st.markdown("# ✝️ Catholic Spiritual OS")
    st.markdown("*Personal • Parish • Diocese • Global • Crisis*")
    
    # Sidebar: User & Role Selection
    with st.sidebar:
        st.markdown("## 👤 User")
        
        role_choice = st.radio(
            "Select your role (for demo):",
            ["Individual", "Parish Coordinator", "Diocesan Leader", "Global Coordinator", "Crisis Responder"],
            index=0
        )
        
        role_map = {
            "Individual": UserRole.INDIVIDUAL,
            "Parish Coordinator": UserRole.PARISH_COORDINATOR,
            "Diocesan Leader": UserRole.DIOCESAN_LEADER,
            "Global Coordinator": UserRole.GLOBAL_COORDINATOR,
            "Crisis Responder": UserRole.CRISIS_RESPONDER,
        }
        
        st.session_state.user = User(
            id="demo_user",
            name=f"Demo {role_choice}",
            email="demo@example.com",
            role=role_map[role_choice],
            parish_id="parish_001",
            diocese_id="diocese_001",
            opt_in_to_parish_aggregates=True,
        )
        
        st.divider()
        
        st.markdown("## 🔍 Current Lens")
        st.write(f"**{st.session_state.current_lens.upper()}**")
        
        if st.session_state.crisis_active:
            st.warning("🚨 CRISIS MODE ACTIVE")
        
        st.divider()
        
        st.markdown("## 📖 About This App")
        st.write("""
        One app, five nested lenses:
        
        🧑 **Personal** - Your formation
        🏛️ **Parish** - Your community
        ⛪ **Diocese** - Your leadership
        🌍 **Global** - Your impact
        🚨 **Crisis** - Emergency response
        
        **Zoom in/out like Google Maps**
        """)
        
        st.markdown("## 🔒 Privacy")
        st.info("All data stays local. Aggregates only shared with permission.")
    
    st.divider()
    
    # Show appropriate lens based on role and selection
    if st.session_state.crisis_active and st.session_state.user.role in [UserRole.DIOCESAN_LEADER, UserRole.CRISIS_RESPONDER]:
        show_lens_crisis()
    elif st.session_state.current_lens == "personal":
        show_lens_personal()
    elif st.session_state.current_lens == "parish":
        show_lens_parish()
    elif st.session_state.current_lens == "diocese":
        show_lens_diocese()
    elif st.session_state.current_lens == "global":
        show_lens_global()
    else:
        show_lens_personal()
    
    st.divider()
    
    # Footer
    st.markdown("""
    **Catholic Spiritual OS v0.2 (Nested Architecture)**
    
    Built with ❤️ for the People of God
    Forever free. Community-owned. CC BY-NC-ND 4.0
    """)

if __name__ == "__main__":
    main()
