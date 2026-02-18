"""
Today's Liturgy — Daily Mass Readings & Liturgical Season
Computed liturgical calendar + live Scripture via bible-api.com
"""
import streamlit as st
import sys, os
sys.path.insert(0, ".")

st.set_page_config(page_title="Today's Liturgy — CNT", page_icon="📖", layout="wide")

# ── Liturgical engine ─────────────────────────────────────────────────────────
_LIT_OK = False
try:
    from services.liturgical_engine import get_liturgical_day
    from services.mass_readings import get_daily_readings
    _LIT_OK = True
except Exception as e:
    st.error(f"Liturgical service unavailable: {e}")

# ── Season color mapping ──────────────────────────────────────────────────────
_SEASON_EMOJI = {
    "Advent":       "🕯️",
    "Christmas":    "⭐",
    "Ordinary Time":"🌿",
    "Lent":         "✝️",
    "Holy Week":    "🌿",
    "Easter":       "✨",
}
_COLOR_HEX = {
    "Purple": "#6b21a8",
    "White":  "#78716c",
    "Green":  "#15803d",
    "Red":    "#b91c1c",
    "Rose":   "#db2777",
    "Gold":   "#b45309",
    "Black/Purple": "#4b5563",
}

if not _LIT_OK:
    st.stop()

# ── Fetch data ────────────────────────────────────────────────────────────────
with st.spinner("Loading today's liturgy…"):
    data = get_daily_readings()

lit_color = data["color"]
hex_color = _COLOR_HEX.get(lit_color, "#374151")
season_emoji = _SEASON_EMOJI.get(data["season"], "✝️")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="
  border-left: 5px solid {hex_color};
  padding: 1rem 1.5rem;
  border-radius: 0 8px 8px 0;
  margin-bottom: 1.5rem;
  background: rgba(128,128,128,0.06);
">
  <div style="font-size:1.7rem; font-weight:700;">{season_emoji} {data['display']}</div>
  <div style="font-size:1rem; opacity:0.75;">{data['date']} &nbsp;·&nbsp; Liturgical color: {lit_color}
  &nbsp;·&nbsp; Year {data['liturgical_year']}</div>
  {"<div style='margin-top:.4rem; font-style:italic;'>🎉 " + data['feast'] + "</div>" if data.get('feast') else ""}
</div>
""", unsafe_allow_html=True)

# ── Season context ────────────────────────────────────────────────────────────
season_descriptions = {
    "Advent":       "A time of joyful expectation as we prepare for Christ's coming at Christmas and his return in glory.",
    "Christmas":    "We celebrate the Incarnation — God becoming human in Jesus Christ. Joy to the world!",
    "Ordinary Time":"Ordinary Time is not ordinary in the sense of boring — it is numbered time, the time of the Church's mission and growth.",
    "Lent":         "Forty days of prayer, fasting, and almsgiving. We walk with Christ toward Jerusalem and the Paschal Mystery.",
    "Holy Week":    "The holiest week of the year. We enter into the Passion, Death, and Resurrection of Jesus Christ.",
    "Easter":       "The great fifty days of Easter joy. Alleluia! Christ is risen — he is truly risen!",
}
if data["season"] in season_descriptions:
    st.caption(season_descriptions[data["season"]])

st.divider()

# ── Readings ──────────────────────────────────────────────────────────────────
readings = data.get("readings")

if readings:
    col_order = [
        ("first_reading",  "📜 First Reading"),
        ("psalm",          "🎵 Responsorial Psalm"),
        ("second_reading", "✉️ Second Reading"),
        ("gospel",         "📖 Gospel"),
    ]

    for key, label in col_order:
        reading = readings.get(key)
        if not reading:
            continue
        with st.expander(f"{label} — {reading['citation']}", expanded=(key == "gospel")):
            if reading["text"]:
                st.markdown(reading["text"])
                st.caption(f"Source: bible-api.com · {reading['citation']}")
            else:
                st.info(f"Full text not available offline. Citation: **{reading['citation']}**")
                st.markdown(f"[Look up on USCCB Bible](https://bible.usccb.org/bible/{reading['citation']})")

    # ── Reflection prompt (Claude-powered if available) ──────────────────────
    st.divider()
    st.subheader("💭 Reflection")

    gospel = readings.get("gospel", {})
    gospel_citation = gospel.get("citation", "today's Gospel")

    _ai_ok = False
    try:
        if "ANTHROPIC_API_KEY" in st.secrets:
            os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
        _ai_ok = bool(os.getenv("ANTHROPIC_API_KEY"))
    except Exception:
        pass

    if _ai_ok:
        if "reflection_generated" not in st.session_state:
            st.session_state.reflection_generated = {}

        cache_key = data["date"]

        if cache_key in st.session_state.reflection_generated:
            st.markdown(st.session_state.reflection_generated[cache_key])
        else:
            if st.button("✨ Generate reflection questions", type="secondary"):
                try:
                    from services.ai_service import homily_helper
                    with st.spinner("Generating reflection questions…"):
                        r = homily_helper(
                            gospel_citation,
                            data["season"],
                            parish_context=f"Liturgy of {data['date']}, {data['display']}",
                            language_code="en",
                            audience="individual daily prayer",
                        )
                    if r["success"]:
                        st.markdown(r["content"])
                        st.session_state.reflection_generated[cache_key] = r["content"]
                    else:
                        st.error(f"Could not generate reflection: {r['error']}")
                except Exception as ex:
                    st.error(f"AI service error: {ex}")
    else:
        # Static reflection prompts based on season
        prompts = {
            "Lent":         ["Where is God calling me to conversion this Lenten season?",
                             "What attachments do I need to let go of?",
                             "How can I practice fasting, prayer, and almsgiving this week?"],
            "Advent":       ["How am I preparing my heart for Christ's coming?",
                             "Where do I see hope in my community?",
                             "What does it mean to wait in joyful expectation?"],
            "Easter":       ["How does the Resurrection change the way I live today?",
                             "Where do I see new life emerging around me?",
                             "How can I be a witness to the Risen Christ this week?"],
            "Ordinary Time": ["What is God saying to me through today's readings?",
                               "How does this Gospel challenge me to grow?",
                               "What one concrete action can I take this week?"],
        }
        seasonal_prompts = prompts.get(data["season"], prompts["Ordinary Time"])
        st.markdown("**Questions for personal reflection:**")
        for p in seasonal_prompts:
            st.markdown(f"- {p}")
        st.caption("Enable AI features (ANTHROPIC_API_KEY) for personalised reflection questions.")

else:
    # Not a Sunday with lectionary readings
    st.info(f"""
**Today ({data['display']}) is not a Sunday.**

Sunday readings are displayed with full text from the lectionary.
For weekday readings, visit:
- [USCCB Daily Readings](https://bible.usccb.org/daily-bible-reading)
- [Universalis](https://universalis.com/today.htm) (global, multi-language)
- [Vatican Daily Readings](https://www.vaticannews.va/en/liturgy-of-the-day.html)
""")

st.divider()

# ── Liturgical calendar quick view ────────────────────────────────────────────
st.subheader("📅 Coming Up")

from services.liturgical_engine import get_liturgical_day
import datetime

upcoming = []
for delta in range(1, 14):
    future = datetime.date.today() + datetime.timedelta(days=delta)
    ld = get_liturgical_day(future)
    if ld.feast or ld.weekday_name == "Sunday":
        upcoming.append(ld)

if upcoming:
    cols = st.columns(min(len(upcoming), 4))
    for i, ld in enumerate(upcoming[:4]):
        with cols[i]:
            color_hex = _COLOR_HEX.get(ld.color, "#374151")
            label = ld.feast if ld.feast else ld.display
            st.markdown(
                f"<div style='border-left:3px solid {color_hex}; padding:.5rem .8rem; border-radius:0 6px 6px 0; background:rgba(128,128,128,0.05);'>"
                f"<small><b>{ld.date.strftime('%b %d')}</b></small><br/>{label}"
                f"</div>",
                unsafe_allow_html=True,
            )
else:
    st.caption("No feasts or Sundays in the next 14 days.")

st.divider()
st.caption(
    "📖 Scripture text from [bible-api.com](https://bible-api.com) · "
    "Lectionary: Roman Rite General Calendar · "
    "Liturgical dates computed from Easter (Gregorian algorithm) · "
    "All Catholics worldwide share the same Sunday readings."
)
