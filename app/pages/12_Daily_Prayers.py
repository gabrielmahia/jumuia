"""
Daily Prayers - Catholic Spiritual OS

Complete Catholic prayer library for personal and communal prayer.

Includes:
- Basic prayers (Our Father, Hail Mary, etc.)
- Rosary with all mysteries
- Marian devotions
- Prayers for various occasions
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.spiritual_os.prayers import (
    PrayerLibrary,
    PrayerCategory,
    PrayerLanguage,
    JOYFUL_MYSTERIES,
    SORROWFUL_MYSTERIES,
    GLORIOUS_MYSTERIES,
    LUMINOUS_MYSTERIES
)

# Page config
st.set_page_config(
    page_title="Daily Prayers | Catholic Spiritual OS",
    page_icon="✝️",
    layout="wide"
)

# Data mode indicator
st.info("📊 **Content Mode**: LIVE — Traditional Catholic prayers", icon="ℹ️")

st.title("🙏 Daily Prayers")

st.markdown("""
Traditional Catholic prayers for personal devotion and communal worship. 
Pray these daily to grow in relationship with God and deepen your faith.

*"Prayer is the raising of one's mind and heart to God." — St. John Damascene*
""")

# Language selector
language = st.selectbox(
    "Select Language",
    ["English", "Latin", "Swahili"],
    help="Choose your preferred prayer language"
)

language_map = {
    "English": "en",
    "Latin": "la",
    "Swahili": "sw"
}
lang_code = language_map[language]

st.divider()

# ============================================================================
# BASIC PRAYERS
# ============================================================================

st.header("Essential Daily Prayers")

st.markdown("""
These are the foundational prayers every Catholic should know. 
Pray them daily, teach them to children, and use them throughout the day.
""")

basic_prayers = PrayerLibrary.get_basic_prayers(lang_code)

for prayer in basic_prayers:
    with st.expander(f"✝️ {prayer.title}"):
        st.markdown(f"### {prayer.title}")
        
        # Prayer text
        prayer_text = prayer.text.get(lang_code, prayer.text.get("en", "Translation not available"))
        st.markdown(f"*{prayer_text}*")
        
        # Additional info
        if prayer.biblical_reference:
            st.caption(f"📖 Biblical Reference: {prayer.biblical_reference}")
        
        if prayer.when_to_pray:
            st.caption(f"⏰ When to Pray: {prayer.when_to_pray}")
        
        if prayer.notes:
            st.info(prayer.notes)

st.divider()

# ============================================================================
# THE HOLY ROSARY
# ============================================================================

st.header("🌹 The Holy Rosary")

st.markdown("""
The Rosary is a powerful Marian prayer that meditates on the life of Christ through Mary's eyes.

**How to Pray the Rosary**:
1. Make the Sign of the Cross and say the Apostles' Creed
2. Say the Our Father
3. Say three Hail Marys (for Faith, Hope, and Charity)
4. Say the Glory Be
5. Announce the First Mystery and say the Our Father
6. Say ten Hail Marys while meditating on the Mystery
7. Say the Glory Be and (optional) Fatima Prayer
8. Repeat steps 5-7 for remaining four Mysteries
9. Conclude with Hail Holy Queen and closing prayers
""")

# Determine today's mysteries
today = datetime.now()
weekday = today.weekday()  # 0=Monday, 6=Sunday

mystery_schedule = {
    0: ("Joyful", JOYFUL_MYSTERIES),      # Monday
    1: ("Sorrowful", SORROWFUL_MYSTERIES), # Tuesday
    2: ("Glorious", GLORIOUS_MYSTERIES),   # Wednesday
    3: ("Luminous", LUMINOUS_MYSTERIES),   # Thursday
    4: ("Sorrowful", SORROWFUL_MYSTERIES), # Friday
    5: ("Joyful", JOYFUL_MYSTERIES),       # Saturday
    6: ("Glorious", GLORIOUS_MYSTERIES),   # Sunday
}

mystery_name, mysteries = mystery_schedule[weekday]

st.success(f"**Today's Mysteries**: {mystery_name} Mysteries ({today.strftime('%A')})")

# Display mysteries
tab1, tab2, tab3, tab4 = st.tabs(["Joyful", "Luminous", "Sorrowful", "Glorious"])

with tab1:
    st.markdown("### 🌅 Joyful Mysteries")
    st.caption("*Prayed on Mondays and Saturdays*")
    for i, mystery in enumerate(JOYFUL_MYSTERIES, 1):
        st.write(f"{i}. {mystery}")
    
    st.markdown("""
    **Fruit of the Mysteries**: Joy, Humility, Charity, Obedience, Piety
    
    **Meditation**: The Joyful Mysteries invite us to contemplate the incarnation of Christ
    and Mary's role in salvation history. Through her "yes" (fiat), the Word became flesh.
    """)

with tab2:
    st.markdown("### 💡 Luminous Mysteries")
    st.caption("*Prayed on Thursdays*")
    for i, mystery in enumerate(LUMINOUS_MYSTERIES, 1):
        st.write(f"{i}. {mystery}")
    
    st.markdown("""
    **Fruit of the Mysteries**: Openness to Holy Spirit, Faith, Conversion, Fortitude, Adoration
    
    **Meditation**: The Luminous Mysteries, introduced by Pope John Paul II in 2002,
    focus on Christ's public ministry and the revelation of his divinity.
    """)

with tab3:
    st.markdown("### 😢 Sorrowful Mysteries")
    st.caption("*Prayed on Tuesdays and Fridays*")
    for i, mystery in enumerate(SORROWFUL_MYSTERIES, 1):
        st.write(f"{i}. {mystery}")
    
    st.markdown("""
    **Fruit of the Mysteries**: Contrition, Patience, Mortification, Obedience, Compassion
    
    **Meditation**: The Sorrowful Mysteries invite us to walk with Jesus in his Passion,
    experiencing the depths of God's love in the cross and redemptive suffering.
    """)

with tab4:
    st.markdown("### 🌟 Glorious Mysteries")
    st.caption("*Prayed on Wednesdays and Sundays*")
    for i, mystery in enumerate(GLORIOUS_MYSTERIES, 1):
        st.write(f"{i}. {mystery}")
    
    st.markdown("""
    **Fruit of the Mysteries**: Faith, Hope, Wisdom, Devotion to Mary, Grace of Holy Death
    
    **Meditation**: The Glorious Mysteries celebrate the triumph of Christ over death
    and the glory that awaits those who remain faithful to him.
    """)

# Fatima Prayer
st.markdown("### 💫 Fatima Prayer (After Each Decade)")
st.info("""
*O my Jesus, forgive us our sins, save us from the fires of hell, 
and lead all souls to Heaven, especially those in most need of Thy mercy. Amen.*
""")

st.divider()

# ============================================================================
# PRAYERS FOR SPECIFIC OCCASIONS
# ============================================================================

st.header("Prayers for Life Situations")

col1, col2 = st.columns(2)

with col1:
    with st.expander("🌅 Morning Offering"):
        st.markdown("""
        *O Jesus, through the Immaculate Heart of Mary,
        I offer You my prayers, works, joys, and sufferings of this day
        for all the intentions of Your Sacred Heart,
        in union with the Holy Sacrifice of the Mass throughout the world,
        for the salvation of souls, the reparation of sins,
        the reunion of all Christians,
        and in particular for the intentions of the Holy Father this month. Amen.*
        """)
    
    with st.expander("🌙 Night Prayer (Compline)"):
        st.markdown("""
        **Examination of Conscience**:
        - What am I grateful for today?
        - Where did I see God present?
        - Where did I fall short of love?
        - What grace do I need for tomorrow?
        
        **Night Prayer**:
        *Lord, I give You thanks for the good things of this day.
        I ask Your forgiveness for my failings.
        Protect me and my loved ones through this night.
        May Your angels watch over us. Amen.*
        """)
    
    with st.expander("🍞 Grace Before Meals"):
        st.markdown("""
        *Bless us, O Lord, and these Thy gifts,
        which we are about to receive from Thy bounty,
        through Christ our Lord. Amen.*
        """)
    
    with st.expander("🙏 Grace After Meals"):
        st.markdown("""
        *We give Thee thanks, Almighty God,
        for all Thy benefits,
        who lives and reigns forever and ever. Amen.*
        """)

with col2:
    with st.expander("😰 Prayer in Difficulty"):
        st.markdown("""
        *Lord Jesus Christ, you said, "Come to me, all who labor and are heavy laden,
        and I will give you rest." I come to you now with my burdens.
        Grant me peace in this storm, strength for this trial,
        and faith to trust in your loving plan. Amen.*
        """)
    
    with st.expander("🕊️ Prayer for Peace"):
        st.markdown("""
        **Prayer of St. Francis**:
        
        *Lord, make me an instrument of your peace:
        where there is hatred, let me sow love;
        where there is injury, pardon;
        where there is doubt, faith;
        where there is despair, hope;
        where there is darkness, light;
        where there is sadness, joy.
        
        O divine Master, grant that I may not so much seek
        to be consoled as to console,
        to be understood as to understand,
        to be loved as to love.
        For it is in giving that we receive,
        it is in pardoning that we are pardoned,
        and it is in dying that we are born to eternal life. Amen.*
        """)
    
    with st.expander("💒 Prayer for the Church"):
        st.markdown("""
        *Lord Jesus, you promised to be with your Church always.
        Guide our Holy Father, our bishops, and all who serve your people.
        Renew your Church in holiness, unity, and mission.
        Raise up many vocations to the priesthood and religious life.
        Help us all to be faithful witnesses to your Gospel. Amen.*
        """)
    
    with st.expander("⚰️ Eternal Rest (for the Dead)"):
        st.markdown("""
        *Eternal rest grant unto them, O Lord,
        and let perpetual light shine upon them.
        May the souls of the faithful departed,
        through the mercy of God, rest in peace. Amen.*
        """)

st.divider()

# ============================================================================
# PRAYER RESOURCES
# ============================================================================

st.header("Prayer Resources")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📱 Prayer Apps")
    st.markdown("""
    - **Laudate**: Complete Catholic app
    - **iBreviary**: Liturgy of the Hours
    - **Hallow**: Guided meditation
    - **Echo**: Audio prayers
    """)

with col2:
    st.markdown("### 📚 Prayer Books")
    st.markdown("""
    - **Roman Missal**: Official liturgy
    - **Christian Prayer**: Liturgy of Hours
    - **Pieta Prayer Book**: Traditional
    - **Magnificat**: Daily prayers
    """)

with col3:
    st.markdown("### 🌐 Online Resources")
    st.markdown("""
    - **USCCB**: [usccb.org/prayers](https://www.usccb.org/prayers)
    - **Pray As You Go**: Audio meditations
    - **Sacred Space**: Daily prayer
    - **Universalis**: Liturgy of Hours
    """)

st.divider()

# ============================================================================
# TEACHING: HOW TO PRAY
# ============================================================================

st.header("How to Pray")

with st.expander("📖 What is Prayer?"):
    st.markdown("""
    Prayer is **conversation with God** — speaking and listening to the One who loves you infinitely.
    
    **Four Types of Prayer** (ACTS):
    - **Adoration**: Praising God for who He is
    - **Contrition**: Asking forgiveness for sins
    - **Thanksgiving**: Gratitude for blessings
    - **Supplication**: Requesting help for needs
    
    *"Prayer is not asking. Prayer is putting oneself in the hands of God."* — Mother Teresa
    """)

with st.expander("⏰ When to Pray"):
    st.markdown("""
    **Traditional Times**:
    - **Morning**: Offer your day to God
    - **Noon**: Angelus (12pm)
    - **Evening**: Examination of conscience
    - **Night**: Thanksgiving and surrender
    
    **Throughout the Day**:
    - Before meals
    - During work breaks
    - In moments of stress
    - When making decisions
    - Before sleep
    
    **Goal**: "Pray without ceasing" (1 Thessalonians 5:17) — constant awareness of God's presence
    """)

with st.expander("📍 Where to Pray"):
    st.markdown("""
    **Sacred Spaces**:
    - Church (especially before the Blessed Sacrament)
    - Home prayer corner
    - Nature (mountains, gardens, beaches)
    - Anywhere quiet
    
    **But also**: God is everywhere! Pray on the bus, at work, while walking. 
    The goal is to "pray always" by maintaining awareness of God's presence.
    """)

with st.expander("💡 Tips for Beginners"):
    st.markdown("""
    1. **Start small**: 5 minutes daily is better than 1 hour once a week
    2. **Be consistent**: Same time, same place helps build habit
    3. **Use structure**: Pray the Rosary, Liturgy of Hours, or traditional prayers
    4. **Speak honestly**: God wants relationship, not performance
    5. **Listen too**: Silence is essential for hearing God
    6. **Don't give up**: Dryness in prayer is normal and even beneficial
    7. **Ask for help**: Spiritual directors, priests, trusted mentors
    
    **Remember**: God desires your presence more than your perfect prayers.
    """)

st.markdown("---")
st.caption("Catholic Spiritual OS | [GitHub](https://github.com/gabrielmahia/catholic-network-tools) | CC BY-NC-ND 4.0")
