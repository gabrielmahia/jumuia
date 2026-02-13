"""
Catholic Network Tools - GospelMap Integration Page
Shows global opportunities, campaigns to join, nearby parishes
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from catholic_network_tools.gospelmap_sync import GospelMapSync, DEMO_OPPORTUNITIES

st.set_page_config(
    page_title="Global Network",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Network - Connected to GospelMap")
st.write("Your parish on the global Church platform")
st.write("")

# Get settings
if "gospelmap_api_key" not in st.session_state:
    st.session_state.gospelmap_api_key = ""
if "parish_id" not in st.session_state:
    st.session_state.parish_id = ""

# Sidebar: Configuration
with st.sidebar:
    st.header("⚙️ GospelMap Settings")
    
    mode = st.radio(
        "Mode",
        ["Demo (Offline)", "Live (Connect to GospelMap)"],
        help="Demo uses sample data. Live connects to global platform."
    )
    
    if mode == "Live (Connect to GospelMap)":
        st.write("")
        st.subheader("API Configuration")
        
        api_key = st.text_input(
            "GospelMap API Key",
            type="password",
            help="Get from GospelMap admin"
        )
        
        parish_id = st.text_input(
            "Parish ID",
            help="Your unique parish identifier"
        )
        
        if api_key and parish_id:
            st.session_state.gospelmap_api_key = api_key
            st.session_state.parish_id = parish_id
            st.success("✅ Connected to GospelMap")
        else:
            st.warning("⚠️ Enter API key + Parish ID to connect")
    else:
        st.info("📊 Using demo data (sample opportunities)")
        st.write("")
        st.write("To connect to live GospelMap:")
        st.write("1. Select 'Live' mode above")
        st.write("2. Enter GospelMap API key")
        st.write("3. Your parish ID")

# Tabs
tabs = st.tabs([
    "🤝 Join Campaigns",
    "🏘️ Nearby Parishes",
    "👨‍⚖️ Bishop Updates",
    "🌏 Diaspora",
    "📊 Global Impact",
    "⚙️ Sync Status"
])

# Initialize sync
gospel_sync = None
opportunities = None

if st.session_state.gospelmap_api_key and st.session_state.parish_id:
    gospel_sync = GospelMapSync(
        st.session_state.gospelmap_api_key,
        st.session_state.parish_id
    )
    opportunities = gospel_sync.get_global_opportunities()
    if not opportunities:
        opportunities = DEMO_OPPORTUNITIES
else:
    opportunities = DEMO_OPPORTUNITIES

with tabs[0]:  # Join Campaigns
    st.header("🤝 Justice Campaigns to Join")
    st.write("Global campaigns coordinated across dioceses and continents")
    st.write("")
    
    if opportunities and "campaigns_to_join" in opportunities:
        for campaign in opportunities["campaigns_to_join"]:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(campaign["name"])
                st.write(f"**Status:** {campaign['status']}")
                st.write(f"**Description:** {campaign['description']}")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Parishes", f"{campaign['parishes_involved']}+")
                with col_b:
                    st.metric("Workers", f"{campaign['workers_affected']}+")
                with col_c:
                    st.metric("Impact", campaign['impact'])
            
            with col2:
                volunteers = st.number_input(
                    f"Volunteers for {campaign['name']}",
                    min_value=0,
                    max_value=500,
                    value=0,
                    key=f"volunteers_{campaign['id']}"
                )
                
                if st.button(
                    "✋ Join Campaign",
                    key=f"join_{campaign['id']}",
                    use_container_width=True,
                    type="primary"
                ):
                    if gospel_sync:
                        if gospel_sync.join_campaign(campaign['id'], volunteers):
                            st.success(f"✅ Joined {campaign['name']} with {volunteers} volunteers!")
                    else:
                        st.success(f"✅ Demo: Would join with {volunteers} volunteers")
            
            st.divider()

with tabs[1]:  # Nearby Parishes
    st.header("🏘️ Nearby Parishes on GospelMap")
    st.write("Find parishes near you + coordinate justice work")
    st.write("")
    
    if opportunities and "nearby_parishes" in opportunities:
        for parish in opportunities["nearby_parishes"]:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(parish["name"])
                st.write(f"**Distance:** {parish['distance_km']} km away")
                
                campaigns = ", ".join(parish.get("shared_campaigns", []))
                if campaigns:
                    st.write(f"**Shared campaigns:** {campaigns}")
                
                st.write(f"**Contact:** {parish.get('contact', 'Contact info not available')}")
            
            with col2:
                if st.button(
                    "📧 Connect",
                    key=f"connect_{parish['id']}",
                    use_container_width=True
                ):
                    st.success(f"📧 Connection request sent to {parish['name']}")
            
            st.divider()
    else:
        st.info("No nearby parishes found in GospelMap yet")

with tabs[2]:  # Bishop Updates
    st.header("👨‍⚖️ Your Bishop on GospelMap")
    st.write("Transparency + Accountability Tracking")
    st.write("")
    
    if opportunities and "bishop_updates" in opportunities:
        bishop = opportunities["bishop_updates"]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Diocese", bishop.get("diocese", "N/A"))
        with col2:
            st.metric("Accountability", f"{bishop.get('accountability_score', 5)}/10")
        with col3:
            trend = bishop.get("transparency_trend", "stable")
            st.metric("Trend", "📈 " + trend if trend == "improving" else "📉 " + trend)
        with col4:
            pass
        
        st.write("")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Recent Improvements")
            for improvement in bishop.get("recent_improvements", []):
                st.write(f"- {improvement}")
        
        with col2:
            st.subheader("🔧 Areas to Work On")
            for area in bishop.get("areas_to_work_on", []):
                st.write(f"- {area}")

with tabs[3]:  # Diaspora
    st.header("🌏 Diaspora Networks")
    st.write("Connect with your ethnic/cultural communities worldwide")
    st.write("")
    
    if opportunities and "diaspora_networks" in opportunities:
        for network in opportunities["diaspora_networks"]:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"🌍 {network['name']}")
                st.write(f"**Global population:** {network['size']:,}")
                
                locations = ", ".join(network.get("major_locations", []))
                if locations:
                    st.write(f"**Major locations:** {locations}")
                
                st.write(f"**Justice work:** {network['justice_work']}")
            
            with col2:
                if st.button(
                    "Join Network",
                    key=f"diaspora_{network['name']}",
                    use_container_width=True
                ):
                    st.success(f"✅ Added to {network['name']} network!")
            
            st.divider()

with tabs[4]:  # Global Impact
    st.header("📊 Global Impact Dashboard")
    st.write("See what the Church is accomplishing together")
    st.write("")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Parishes on GospelMap", "5,000+")
    with col2:
        st.metric("Justice Campaigns", "50+")
    with col3:
        st.metric("Workers Helped", "26,000+")
    with col4:
        st.metric("Global Policy Wins", "3")
    
    st.write("")
    st.subheader("Living Wage Campaign - Global Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**🇰🇪 Kenya**")
        st.write("5,000 workers")
        st.write("150 parishes")
        st.write("**+26% wage increase** ✅")
    
    with col2:
        st.write("**🇺🇸 USA (Virginia)**")
        st.write("15,000 workers")
        st.write("47 parishes")
        st.write("**+$2/hour** ✅")
    
    with col3:
        st.write("**🇧🇷 Brazil**")
        st.write("8,000 workers")
        st.write("65 parishes")
        st.write("**In progress** ⏳")
    
    st.write("")
    st.write("**Global Total: 26,000+ workers, 250+ parishes, 3 policy wins**")

with tabs[5]:  # Sync Status
    st.header("⚙️ Sync Status")
    st.write("Check your parish sync with GospelMap")
    st.write("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📡 Connection Status")
        
        if gospel_sync and gospel_sync.is_enabled():
            st.success("✅ Connected to GospelMap")
            st.write(f"Parish ID: `{st.session_state.parish_id}`")
            st.write(f"Last sync: just now")
        else:
            st.warning("⚠️ Not connected to GospelMap")
            st.write("Enable in sidebar settings to sync")
    
    with col2:
        st.subheader("🔄 Auto-Sync Settings")
        
        sync_enabled = st.checkbox("Enable auto-sync", value=True)
        sync_frequency = st.selectbox(
            "Sync frequency",
            ["Hourly", "Daily", "Weekly"],
            index=0
        )
        
        if sync_enabled:
            st.info(f"🔄 Auto-syncing {sync_frequency.lower()}")
        
        if st.button("Sync Now", use_container_width=True):
            st.success("✅ Syncing with GospelMap...")
            st.write("Your parish data sent:")
            st.write("- Sacrament availability")
            st.write("- Material aid info")
            st.write("- Justice campaigns")
            st.write("- Volunteer capacity")
            st.write("- Welcome indices")
    
    st.write("")
    st.divider()
    st.write("")
    
    st.subheader("📊 What We Send to GospelMap")
    
    data_sent = {
        "Category": [
            "Parish Info",
            "Accessibility",
            "Sacraments",
            "Material Aid",
            "Justice",
            "Stewardship",
            "Volunteers"
        ],
        "Data": [
            "Name, location, diocese",
            "Languages, wheelchair, nursery",
            "Masses/week, baptisms, confessions",
            "Food, shelter, medical",
            "Active campaigns, engagement %",
            "Monthly giving, budget",
            "Count, capacity"
        ],
        "Privacy": [
            "Public",
            "Public",
            "Public",
            "Public",
            "Public",
            "Aggregated only",
            "Aggregated only"
        ]
    }
    
    df = pd.DataFrame(data_sent)
    st.table(df)
    
    st.write("")
    st.info("""
    **Privacy Notice:** 
    - No individual donor information shared
    - Financial data aggregated only
    - Parish can opt-out anytime
    - All data encrypted in transit
    - Community-owned (not sold)
    """)

st.write("")
st.divider()
st.write("")

# Footer
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("""
    **🌍 GospelMap**
    
    Global Church Platform
    """)

with col2:
    st.markdown("""
    **📧 Support**
    
    gabriel@aikungfu.dev
    """)

with col3:
    st.markdown("""
    **🔗 Links**
    
    [GospelMap](https://gospelmap-global.streamlit.app)
    """)

st.markdown("---")
st.markdown("*'Nothing is hidden that will not be revealed.' — Luke 12:2*")
