"""
Global Church Directory - Catholic Spiritual OS

Find Catholic churches anywhere in the world.

The "Bhutan Problem" solved: Find the 7 Catholic parishes in Bhutan
(0.1% Catholic, no online presence) or any of 100,000+ parishes globally.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.spiritual_os.church_directory import (
    Church,
    ChurchDirectory,
    ChurchType,
    MassLanguage,
    WelcomeLevel,
    DEMO_CHURCHES
)

# Page config
st.set_page_config(
    page_title="Find a Church | Catholic Spiritual OS",
    page_icon="✝️",
    layout="wide"
)

# Data mode indicator
st.info("📊 **Data Mode**: DEMO (2 churches) | Production: 100,000+ parishes worldwide", icon="ℹ️")

st.title("🌍 Find a Catholic Church")

st.markdown("""
Locate Catholic parishes anywhere in the world. From Bhutan to Brazil, Kenya to Korea.

**Whether you're**:
- Traveling and need Mass times
- New to an area
- Looking for Mass in your language
- Seeking a welcoming community

**We'll help you find your spiritual home.**
""")

st.divider()

# ============================================================================
# SEARCH INTERFACE
# ============================================================================

st.header("Search for a Church")

search_type = st.radio(
    "How do you want to search?",
    ["By Location", "By Language", "By Name", "Near Me"],
    horizontal=True
)

results = []

if search_type == "By Location":
    col1, col2 = st.columns(2)
    
    with col1:
        country = st.selectbox(
            "Country",
            ["", "Bhutan", "Kenya", "United States", "Brazil", "Philippines", "India"],
            help="Select country or type to search"
        )
    
    with col2:
        city = st.text_input(
            "City (optional)",
            placeholder="e.g., Thimphu, Nairobi"
        )
    
    if st.button("Search", type="primary"):
        if country:
            results = ChurchDirectory.search_by_location(country, city if city else None)
        else:
            st.warning("Please select a country")

elif search_type == "By Language":
    language = st.selectbox(
        "Mass Language",
        [lang.value for lang in MassLanguage]
    )
    
    if st.button("Search", type="primary"):
        lang_enum = [l for l in MassLanguage if l.value == language][0]
        results = ChurchDirectory.search_by_language(lang_enum)

elif search_type == "By Name":
    church_name = st.text_input(
        "Church Name",
        placeholder="e.g., St. Mary's, Consolata"
    )
    
    if st.button("Search", type="primary"):
        if church_name:
            results = ChurchDirectory.search_by_name(church_name)
        else:
            st.warning("Please enter a church name")

elif search_type == "Near Me":
    st.info("""
    📍 **Location Services Required**
    
    To find churches near you, we need your location.
    
    In production, this would:
    1. Request your browser location (latitude/longitude)
    2. Search radius: 5km, 10km, 25km, 50km, 100km
    3. Sort by distance
    
    For demo, try "By Location" search above.
    """)

st.divider()

# ============================================================================
# SEARCH RESULTS
# ============================================================================

if results:
    st.success(f"Found {len(results)} church(es)")
    
    for church in results:
        with st.container():
            # Church header
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"## ✝️ {church.name}")
                st.caption(f"{church.type.value} | {church.city}, {church.country}")
            
            with col2:
                if church.verified:
                    st.success("✅ Verified")
                else:
                    st.caption("Unverified listing")
            
            # Location & Contact
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📍 Location")
                st.write(f"**Address**: {church.address}")
                st.write(f"**City**: {church.city}, {church.region or ''}")
                st.write(f"**Country**: {church.country}")
                
                # Map link
                maps_url = f"https://www.google.com/maps/search/?api=1&query={church.latitude},{church.longitude}"
                st.markdown(f"[📍 View on Google Maps]({maps_url})")
            
            with col2:
                st.markdown("### 📞 Contact")
                if church.contact.phone:
                    st.write(f"**Phone**: {church.contact.phone}")
                if church.contact.email:
                    st.write(f"**Email**: {church.contact.email}")
                if church.contact.website:
                    st.markdown(f"**Website**: [{church.contact.website}]({church.contact.website})")
                if church.contact.whatsapp:
                    st.write(f"**WhatsApp**: {church.contact.whatsapp}")
            
            # Mass Schedule
            with st.expander("⏰ Mass Schedule", expanded=True):
                if church.mass_schedule.sunday_times:
                    st.markdown("**Sunday Masses**:")
                    for mass_time in church.mass_schedule.sunday_times:
                        st.write(f"- {mass_time}")
                
                if church.mass_schedule.saturday_vigil:
                    st.write(f"**Saturday Vigil**: {church.mass_schedule.saturday_vigil}")
                
                if church.mass_schedule.weekday_times:
                    st.markdown("**Weekday Masses**:")
                    for mass_time in church.mass_schedule.weekday_times:
                        st.write(f"- {mass_time}")
                
                if church.mass_schedule.confession_times:
                    st.markdown("**Confession**:")
                    for conf_time in church.mass_schedule.confession_times:
                        st.write(f"- {conf_time}")
                
                if church.mass_schedule.adoration_times:
                    st.info(f"**Adoration**: {church.mass_schedule.adoration_times}")
            
            # Community Info
            with st.expander("👥 Community & Ministries"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if church.registered_families:
                        st.metric("Registered Families", church.registered_families)
                    if church.average_sunday_attendance:
                        st.metric("Sunday Attendance", church.average_sunday_attendance)
                
                with col2:
                    st.markdown("**Languages**: " + ", ".join([lang.value for lang in church.mass_languages]))
                    st.markdown(f"**Welcome Level**: {church.welcome_level.value}")
                
                if church.ethnic_communities:
                    st.markdown("**Ethnic Communities**:")
                    st.write(", ".join(church.ethnic_communities))
                
                if church.special_ministries:
                    st.markdown("**Special Ministries**:")
                    for ministry in church.special_ministries:
                        st.write(f"- {ministry}")
            
            # Additional Info
            with st.expander("ℹ️ Additional Information"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Diocese**: {church.diocese}")
                    if church.bishop:
                        st.write(f"**Bishop**: {church.bishop}")
                    if church.pastor:
                        st.write(f"**Pastor**: {church.pastor}")
                    if church.established_year:
                        st.write(f"**Established**: {church.established_year}")
                
                with col2:
                    if church.patron_saint:
                        st.write(f"**Patron Saint**: {church.patron_saint}")
                    st.write(f"**Wheelchair Accessible**: {'Yes' if church.wheelchair_accessible else 'No'}")
                    st.write(f"**Parking Available**: {'Yes' if church.parking_available else 'No'}")
                    st.write(f"**Nursery**: {'Available' if church.nursery_available else 'Not available'}")
                
                if church.notes:
                    st.info(church.notes)
            
            st.divider()

elif search_type in ["By Location", "By Language", "By Name"]:
    if st.session_state.get('search_attempted'):
        st.warning("No churches found. Try a different search or help us add this church!")

st.divider()

# ============================================================================
# ADD A CHURCH
# ============================================================================

st.header("Can't Find Your Church?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📝 Add a Church
    
    Help us build the world's most comprehensive Catholic directory!
    
    **Submit a church**:
    1. Church name and location
    2. Contact information
    3. Mass schedule
    4. Parish details
    
    We verify all submissions before publishing.
    """)
    
    if st.button("Submit a Church"):
        st.info("Church submission form coming soon! For now, email: contact@aikungfu.dev")

with col2:
    st.markdown("""
    ### ✅ Claim Your Parish
    
    Are you a parish administrator?
    
    **Claim your listing** to:
    - Verify information
    - Update Mass times
    - Add photos
    - Promote ministries
    - Respond to reviews
    
    Free for all parishes.
    """)
    
    if st.button("Claim This Parish"):
        st.info("Parish verification coming soon! Email: contact@aikungfu.dev")

st.divider()

# ============================================================================
# COVERAGE MAP
# ============================================================================

st.header("Global Coverage")

st.markdown("""
**Current Coverage** (Demo): 2 churches in 2 countries  
**Production Goal**: 100,000+ parishes in 200+ countries

**Featured Countries**:
- 🇻🇦 Vatican City: 1
- 🇮🇹 Italy: 25,000+
- 🇺🇸 United States: 17,000+
- 🇧🇷 Brazil: 11,000+
- 🇲🇽 Mexico: 8,000+
- 🇵🇭 Philippines: 7,000+
- 🇵🇱 Poland: 10,000+
- 🇰🇪 Kenya: 500+
- 🇧🇹 Bhutan: 7
- 🇲🇲 Myanmar: 350
- 🇳🇵 Nepal: 12
- 🇸🇦 Saudi Arabia: 2 (expat communities)

**Rare but present**: Mongolia, Laos, Afghanistan, Yemen, North Korea (underground)
""")

# Partnership opportunities
st.info("""
**Partnership Opportunities**:
- **Dioceses**: Bulk import your parish directory
- **GCatholic.org**: Data partnership for global coverage
- **USCCB**: Official US Catholic directory
- **National Conferences**: Local church data
""")

st.divider()

# ============================================================================
# WHY THIS MATTERS
# ============================================================================

st.header("Why a Global Directory Matters")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🌏 For Travelers
    
    **The Problem**:
    You're in Bhutan for work. You're Catholic. Where's the nearest church?
    
    **Google**: Shows Buddhist temples
    **Facebook**: No results
    **Local contacts**: Maybe one person knows
    
    **Our Solution**: 
    Instant answer with Mass times, languages, contact info.
    """)

with col2:
    st.markdown("""
    ### 🏠 For Migrants
    
    **The Problem**:
    Filipino nurse in Saudi Arabia needs Sunday Mass in Tagalog.
    
    **Without directory**:
    Months of asking around, maybe never finds community.
    
    **With directory**:
    Finds Filipino Catholic Center in 2 minutes, connects immediately.
    """)

with col3:
    st.markdown("""
    ### ⛪ For Parishes
    
    **The Problem**:
    Small parish in rural area, no website, invisible online.
    
    **Result**:
    Visitors can't find them. New residents don't know they exist.
    
    **Solution**:
    Free listing = instant discoverability worldwide.
    """)

st.markdown("---")
st.caption("Catholic Spiritual OS | [GitHub](https://github.com/gabrielmahia/catholic-network-tools) | CC BY-NC-ND 4.0")
