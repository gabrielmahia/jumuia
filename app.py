"""
Catholic Spiritual OS - Personal formation platform
Consolidated into single Catholic Network Tools repository
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from spiritual_os.domain.rule_of_life import RuleOfLife, generate_rule_template
from spiritual_os.domain.liturgy import LiturgyCalendar, season_description
from spiritual_os.domain.journal import Journal, JournalTemplate
from spiritual_os.domain.sacraments import SacramentTracker, default_sacrament_template
from spiritual_os.domain.parish import Parish, ParishBulletin
from spiritual_os.domain.diocese import Diocese, DioceseDirectory
from spiritual_os.storage.local_store import LocalStore, PRIVACY_NOTICE

# Configure page
st.set_page_config(
    page_title="Catholic Spiritual OS",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .dimension-card {
        border-left: 5px solid #2E7D32;
        padding: 20px;
        margin: 10px 0;
        border-radius: 5px;
        background: #F1F8F6;
    }
    .season-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_default"
if "store" not in st.session_state:
    st.session_state.store = LocalStore()
if "rule_of_life" not in st.session_state:
    st.session_state.rule_of_life = generate_rule_template()
if "journal" not in st.session_state:
    st.session_state.journal = Journal(user_id=st.session_state.user_id)
if "sacrament_tracker" not in st.session_state:
    st.session_state.sacrament_tracker = default_sacrament_template()

# Sidebar
with st.sidebar:
    st.markdown("## 🙏 Spiritual OS")
    st.write("Personal formation platform")
    
    st.divider()
    
    st.markdown("### Layers")
    st.write("""
    **D** Personal Spiritual OS (You are here)
    **A** Parish Utilities
    **B** Diocese Governance
    **C** Global Coordination (Roadmap)
    **E** Resilience Integration (Roadmap)
    """)
    
    st.divider()
    st.markdown(PRIVACY_NOTICE)

# Main header
st.markdown("# ✝️ Catholic Spiritual OS")
st.write("*Personal formation. Parish coordination. Diocese governance. Global vision.*")

st.divider()

# Liturgical context banner
season = LiturgyCalendar.current_season()
color = LiturgyCalendar.current_color()
feast_today = LiturgyCalendar.today_feast()

st.markdown(f"""
    <div class="season-banner">
    <h3>⛪ {season.value} — {season_description()}</h3>
    <p>Liturgical color: <strong>{color.upper()}</strong></p>
    {f"<p>Today: <strong>{feast_today.name}</strong></p>" if feast_today else ""}
    </div>
""", unsafe_allow_html=True)

# Main tabs
tabs = st.tabs([
    "🏠 Dashboard",
    "📖 Rule of Life",
    "📔 Journaling",
    "🛐 Sacraments",
    "📰 Parish",
    "⛪ Diocese",
    "❓ Help"
])

# TAB 0: Dashboard
with tabs[0]:
    st.header("Your Spiritual Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        daily_practices = st.session_state.rule_of_life.daily_practices()
        st.metric("Daily Practices", len(daily_practices))
    
    with col2:
        total_minutes = st.session_state.rule_of_life.total_daily_minutes()
        st.metric("Daily Commitment", f"{total_minutes} min")
    
    with col3:
        journal_entries = len(st.session_state.journal.entries)
        st.metric("Journal Entries", journal_entries)
    
    with col4:
        in_progress = st.session_state.sacrament_tracker.get_in_progress()
        st.metric("In Progress", len(in_progress))
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📖 Today's Practices")
        for practice in daily_practices:
            st.write(f"✓ **{practice.name}** ({practice.duration_minutes} min)")
            if practice.notes:
                st.write(f"  *{practice.notes}*")
    
    with col2:
        st.subheader("🛐 Sacramental Life")
        for milestone in st.session_state.sacrament_tracker.milestones:
            status = "✅" if milestone.is_received() else "⏳"
            st.write(f"{status} {milestone.name}")

# TAB 1: Rule of Life
with tabs[1]:
    st.header("📖 Rule of Life")
    st.write("*Daily/weekly spiritual practices*")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Your Practices")
        for entry in st.session_state.rule_of_life.entries:
            st.write(f"""
            **{entry.name}** ({entry.duration_minutes} min, {entry.frequency})
            - Category: {entry.category}
            - {entry.notes}
            """)
    
    with col2:
        st.subheader("Statistics")
        st.metric("Total Entries", len(st.session_state.rule_of_life.entries))
        st.metric("Daily Total", f"{st.session_state.rule_of_life.total_daily_minutes()} min")
    
    st.divider()
    
    st.subheader("Add Practice")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        practice_name = st.text_input("Practice name")
    with col2:
        category = st.selectbox("Category", ["prayer", "scripture", "examen", "virtue", "fasting", "mercy"])
    with col3:
        duration = st.number_input("Duration (min)", 1, 120, 15)
    
    if st.button("Add to Rule", use_container_width=True):
        from spiritual_os.domain.rule_of_life import RuleEntry
        entry = RuleEntry(
            name=practice_name,
            category=category,
            duration_minutes=duration,
            frequency="daily"
        )
        st.session_state.rule_of_life.add_entry(entry)
        st.success(f"Added: {practice_name}")
        st.rerun()

# TAB 2: Journaling
with tabs[2]:
    st.header("📔 Spiritual Journal")
    st.write("*Guided reflection with templates*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Journal Entries")
        if st.session_state.journal.entries:
            for entry in reversed(st.session_state.journal.entries[-10:]):
                st.write(f"**{entry.date}** - {entry.template_type}")
                if entry.title:
                    st.write(f"*{entry.title}*")
        else:
            st.info("No journal entries yet")
    
    with col2:
        st.subheader("Templates")
        template_choice = st.selectbox(
            "Choose template",
            ["Examen", "Lectio Divina", "Hardening vs Healing", "Fatigue Warning"]
        )
    
    st.divider()
    
    st.subheader("New Entry")
    
    template_map = {
        "Examen": JournalTemplate.examen_template(),
        "Lectio Divina": JournalTemplate.lectio_divina_template(),
        "Hardening vs Healing": JournalTemplate.hardening_healing_template(),
        "Fatigue Warning": JournalTemplate.fatigue_warning_template()
    }
    
    template = template_map.get(template_choice)
    
    if template:
        st.write(f"**{template['name']}** (~{template['time_minutes']} min)")
        
        for prompt in template["prompts"]:
            st.write(f"*{prompt}*")
        
        entry_content = st.text_area("Your reflection:", height=200)
        
        if st.button("Save Entry", use_container_width=True):
            from spiritual_os.domain.journal import JournalEntry
            from datetime import date
            
            entry = JournalEntry(
                date=str(date.today()),
                template_type=template_choice.lower(),
                content=entry_content
            )
            st.session_state.journal.add_entry(entry)
            st.success("Entry saved!")
            st.rerun()

# TAB 3: Sacraments
with tabs[3]:
    st.header("🛐 Sacramental Life")
    st.write("*Track your sacramental milestones*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Your Milestones")
        for milestone in st.session_state.sacrament_tracker.milestones:
            status = "✅ Received" if milestone.is_received() else "⏳ Preparing..."
            st.write(f"**{milestone.name}** — {status}")
            if milestone.date_received:
                st.write(f"  Date: {milestone.date_received}")
            if milestone.notes:
                st.write(f"  {milestone.notes}")
    
    with col2:
        st.subheader("In Progress")
        in_progress = st.session_state.sacrament_tracker.get_in_progress()
        st.metric("Count", len(in_progress))

# TAB 4: Parish
with tabs[4]:
    st.header("📰 Parish Layer (A)")
    st.write("*Parish bulletin, events, coordination*")
    
    st.info("🚧 Parish utilities loaded from local data (CSV/JSON)")
    
    st.subheader("Sample Parish Data")
    
    sample_parish = Parish(
        name="Sample Parish",
        diocese="Sample Diocese",
        active_members_count=487,
        weekly_attendance=234
    )
    
    st.write(f"**{sample_parish.name}** ({sample_parish.diocese})")
    st.write(f"- Active: {sample_parish.active_members_count}")
    st.write(f"- Weekly attendance: {sample_parish.weekly_attendance}")
    
    st.subheader("To load your parish:")
    st.code("Place bulletin CSV in /Data/parishes/")

# TAB 5: Diocese
with tabs[5]:
    st.header("⛪ Diocese Layer (B)")
    st.write("*Governance, coordination, aggregate stats (NO personal data)*")
    
    st.info("🚧 Diocese directory loaded from configuration")
    
    st.subheader("Aggregate Statistics")
    
    sample_diocese = Diocese(
        name="Sample Diocese",
        region="Sample Region",
        bishop_name="Bishop Name",
        stats=type('DioceseStats', (), {
            'total_parishes': 50,
            'total_catholics': 100000,
            'weekly_attendance': 25000,
            'priests_count': 120,
            'deacons_count': 45
        })()
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Parishes", sample_diocese.stats.total_parishes)
    with col2:
        st.metric("Catholics", f"{sample_diocese.stats.total_catholics:,}")
    with col3:
        st.metric("Weekly Attendance", f"{sample_diocese.stats.weekly_attendance:,}")

# TAB 6: Help
with tabs[6]:
    st.header("❓ Help & Information")
    
    st.subheader("What is Spiritual OS?")
    st.write("""
    A **personal spiritual formation platform** built on Catholic theology.
    
    **Five Layers:**
    - **D** Personal (You) - Rule of Life, Journaling, Sacraments
    - **A** Parish - Bulletins, Events, Community
    - **B** Diocese - Governance, Coordination (aggregate stats only)
    - **C** Global (Planned) - Federated coordination
    - **E** Resilience (Planned) - Disaster/crisis response
    """)
    
    st.subheader("🔒 Privacy")
    st.write("""
    - All data stored **locally** on your device
    - Never sent to external servers
    - You control all data
    - Spiritual formation is personal
    """)
    
    st.subheader("⚠️ Disclaimer")
    st.write("""
    **This is a TOOL, not a SUBSTITUTE for:**
    - Clergy or spiritual direction
    - Medical/mental health care
    - Professional counseling
    
    For serious spiritual concerns, consult your priest or bishop.
    For crisis support, contact emergency services.
    """)
    
    st.divider()
    
    st.markdown("""
    **📜 License:** CC BY-NC-ND 4.0
    **🔗 Repo:** github.com/gabrielmahia/catholic-network-tools
    **📧 Support:** contact@aikungfu.dev
    
    ---
    *"Prayer is not asking. It is a longing of the soul." — Gandhi*
    """)

# Footer
st.divider()
st.markdown("""
**Catholic Spiritual OS v0.1**
— Personal. Parish. Diocese. Global. Resilient. —

Built with ❤️ for the People of God.
Forever free. Community-owned. AGPL licensed.
""")
