"""
Liturgy of the Day - Catholic Spiritual OS

Daily liturgical calendar with:
- Current liturgical season and color
- Today's celebration/feast
- Liturgical context for spiritual formation
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import date, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.spiritual_os.liturgical_calendar import (
    LiturgicalCalendar,
    LiturgicalColor,
    LiturgicalSeason
)
from src.spiritual_os.mass_readings import MassReadingsAPI, ReadingType

# Page config
st.set_page_config(
    page_title="Liturgy of the Day | Catholic Spiritual OS",
    page_icon="✝️",
    layout="wide"
)

# Data mode indicator
st.info("📊 **Data Mode**: LIVE — Connected to Church Calendar API", icon="ℹ️")

st.title("✝️ Liturgy of the Day")

st.markdown("""
The liturgical calendar guides our spiritual journey through the Church year. 
Each season invites us into different aspects of Christ's life and our formation as disciples.
""")

# ============================================================================
# TODAY'S LITURGY
# ============================================================================

st.header("Today's Celebration")

today = LiturgicalCalendar.get_today()

if today:
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader(today.primary_celebration)
        st.markdown(f"**{today.date.strftime('%A, %B %d, %Y')}**")
    
    with col2:
        # Liturgical color
        color_emoji = {
            LiturgicalColor.GREEN: "🟢",
            LiturgicalColor.WHITE: "⚪",
            LiturgicalColor.RED: "🔴",
            LiturgicalColor.PURPLE: "🟣",
            LiturgicalColor.ROSE: "🌸",
            LiturgicalColor.BLACK: "⚫"
        }
        emoji = color_emoji.get(today.color, "🔵")
        
        st.metric(
            label="Liturgical Color",
            value=f"{emoji} {today.color.value.capitalize()}"
        )
    
    with col3:
        # Liturgical season
        season_emoji = {
            LiturgicalSeason.ORDINARY: "🌱",
            LiturgicalSeason.ADVENT: "🕯️",
            LiturgicalSeason.CHRISTMAS: "⭐",
            LiturgicalSeason.LENT: "🙏",
            LiturgicalSeason.EASTER: "🌅"
        }
        s_emoji = season_emoji.get(today.season, "📅")
        
        st.metric(
            label="Season",
            value=f"{s_emoji} {today.season.value.capitalize()}",
            delta=f"Week {today.season_week}"
        )
    
    st.divider()
    
    # Color meaning
    st.markdown("### Liturgical Color Meaning")
    st.info(LiturgicalCalendar.get_color_description(today.color))
    
    # All celebrations for today
    if len(today.celebrations) > 1:
        st.markdown("### Additional Commemorations")
        for idx, celebration in enumerate(today.celebrations[1:], 1):
            with st.expander(f"{idx}. {celebration.get('title', 'Unknown')}"):
                st.write(f"**Rank**: {celebration.get('rank', 'N/A')}")
                st.write(f"**Color**: {celebration.get('colour', 'N/A')}")
    
    st.divider()
    
    # Spiritual reflection prompt
    st.markdown("### Reflection Prompt")
    
    season_prompts = {
        LiturgicalSeason.ORDINARY: "How is God calling you to grow in everyday faithfulness today?",
        LiturgicalSeason.ADVENT: "How are you preparing room in your heart for Christ's coming?",
        LiturgicalSeason.CHRISTMAS: "Where do you see God's light breaking into darkness in your life?",
        LiturgicalSeason.LENT: "What is God inviting you to let go of or take up in this season?",
        LiturgicalSeason.EASTER: "How are you experiencing Christ's resurrection in your daily life?"
    }
    
    prompt = season_prompts.get(today.season, "How is God present in your life today?")
    st.write(f"💭 *{prompt}*")
    
else:
    st.warning("Unable to retrieve liturgical data. Please check your internet connection.")

st.divider()

# ============================================================================
# TODAY'S MASS READINGS
# ============================================================================

st.header("📖 Today's Mass Readings")

st.markdown("""
The Word of God proclaimed at Mass. Listen, reflect, and respond to God's call in Scripture.
""")

mass_readings = MassReadingsAPI.get_today()

if mass_readings:
    # Display liturgical context
    st.info(f"**{mass_readings.liturgical_title}** | Cycle {mass_readings.liturgical_cycle.value}")
    
    # First Reading
    with st.expander("📜 First Reading", expanded=True):
        st.markdown(f"### {mass_readings.first_reading.citation}")
        st.markdown(mass_readings.first_reading.text)
    
    # Responsorial Psalm
    with st.expander("🎵 Responsorial Psalm"):
        st.markdown(f"### {mass_readings.psalm.citation}")
        st.markdown(mass_readings.psalm.text)
    
    # Second Reading (if Sunday/Solemnity)
    if mass_readings.second_reading:
        with st.expander("📜 Second Reading"):
            st.markdown(f"### {mass_readings.second_reading.citation}")
            st.markdown(mass_readings.second_reading.text)
    
    # Gospel
    with st.expander("✝️ Gospel", expanded=True):
        st.markdown(f"### {mass_readings.gospel.citation}")
        st.markdown(mass_readings.gospel.text)
        
        # Gospel reflection prompts
        if mass_readings.reflections:
            st.markdown("---")
            st.markdown("**Reflection Questions:**")
            for reflection in mass_readings.reflections:
                st.write(f"💭 {reflection}")
    
    # Alleluia
    if mass_readings.alleluia:
        st.success(f"**Alleluia!** {mass_readings.alleluia.text}")
    
    # Saint of the day
    if mass_readings.saint_of_day:
        st.info(f"**Saint of the Day**: {mass_readings.saint_of_day}")
    
    # Actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**[Listen on USCCB →](https://bible.usccb.org/daily-bible-reading)**")
    
    with col2:
        st.markdown("**[Print for Bulletin →](#)**")
    
    with col3:
        st.markdown("**[Share Readings →](#)**")

else:
    st.warning("""
    Unable to retrieve Mass readings. Please check your internet connection or visit:
    - **USCCB Daily Readings**: https://bible.usccb.org/daily-bible-reading
    - **Universalis**: https://universalis.com
    """)

st.divider()

# ============================================================================
# LITURGICAL CALENDAR BROWSER
# ============================================================================

st.header("Browse Liturgical Calendar")

col_prev, col_date, col_next = st.columns([1, 2, 1])

with col_date:
    selected_date = st.date_input(
        "Select date",
        value=date.today(),
        min_value=date(1970, 1, 1),
        max_value=date(2099, 12, 31)
    )

if selected_date != date.today():
    selected_day = LiturgicalCalendar.get_day(selected_date)
    
    if selected_day:
        st.subheader(selected_day.primary_celebration)
        st.markdown(f"**{selected_day.date.strftime('%A, %B %d, %Y')}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Color**: {selected_day.color.value.capitalize()}")
            st.write(f"**Season**: {selected_day.season.value.capitalize()}, Week {selected_day.season_week}")
        
        with col2:
            st.write(f"**Rank**: {selected_day.rank}")
    else:
        st.warning(f"Unable to retrieve liturgical data for {selected_date}")

st.divider()

# ============================================================================
# LITURGICAL SEASONS OVERVIEW
# ============================================================================

st.header("Liturgical Seasons Guide")

with st.expander("🕯️ Advent (4 weeks before Christmas)"):
    st.markdown("""
    **Theme**: Waiting and preparation for Christ's coming
    
    **Color**: Purple (preparation, penance)
    
    **Focus**: Anticipation, hope, preparation of heart
    
    **Special Note**: 3rd Sunday (Gaudete Sunday) uses rose vestments to celebrate joy in anticipation
    """)

with st.expander("⭐ Christmas (Dec 25 - Baptism of the Lord)"):
    st.markdown("""
    **Theme**: Joy of the Incarnation
    
    **Color**: White (joy, purity, glory)
    
    **Focus**: God becoming human, Emmanuel (God with us)
    
    **Duration**: From Christmas Eve through Baptism of the Lord (early January)
    """)

with st.expander("🌱 Ordinary Time (2 periods)"):
    st.markdown("""
    **Theme**: Growth in discipleship
    
    **Color**: Green (growth, life, hope)
    
    **Focus**: Following Christ day by day, formation in virtue
    
    **Duration**: 
    - Period 1: After Christmas until Ash Wednesday
    - Period 2: After Pentecost until Advent (longest period)
    """)

with st.expander("🙏 Lent (Ash Wednesday to Holy Thursday)"):
    st.markdown("""
    **Theme**: Repentance and preparation for Easter
    
    **Color**: Purple (penance, conversion)
    
    **Focus**: Prayer, fasting, almsgiving; dying to self
    
    **Special Note**: 4th Sunday (Laetare Sunday) uses rose vestments for rejoicing at coming Easter
    
    **Duration**: 40 days (not counting Sundays) + Holy Week
    """)

with st.expander("🌅 Easter (Easter Sunday through Pentecost)"):
    st.markdown("""
    **Theme**: Resurrection and new life in Christ
    
    **Color**: White (through Ascension), Red (Pentecost)
    
    **Focus**: Baptismal renewal, living as resurrection people
    
    **Duration**: 50 days from Easter Sunday to Pentecost
    
    **Culmination**: Pentecost (descent of Holy Spirit)
    """)

st.divider()

# ============================================================================
# RESOURCES
# ============================================================================

st.header("Resources")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### For Parishes")
    st.markdown("""
    - **Parish Bulletins**: Use liturgical data for weekly bulletin headers
    - **Formation Programs**: Align catechesis with liturgical season
    - **Homily Prep**: Context for Sunday readings
    - **Decoration Planning**: Liturgical color coordination
    """)

with col2:
    st.markdown("### For Individuals")
    st.markdown("""
    - **Daily Prayer**: Connect personal prayer to Church's rhythm
    - **Spiritual Reading**: Choose books matching liturgical season
    - **Family Catechesis**: Teach children about Church year
    - **Fasting/Feasting**: Align personal practices with season
    """)

st.info("""
**Data Source**: Church Calendar API (http://calapi.inadiutorium.cz/)

This liturgical data follows the General Roman Calendar as promulgated after Vatican II. 
For specific national or diocesan calendars, consult your local ordinary or bishop's conference.
""")

st.markdown("---")
st.caption("Catholic Spiritual OS | [GitHub](https://github.com/gabrielmahia/catholic-network-tools) | CC BY-NC-ND 4.0")
