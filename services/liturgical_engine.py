"""
Liturgical Engine — Catholic Network Tools
Computes the correct liturgical season, week number, color, and feast for any date.
No external dependencies. Based on Roman Rite General Calendar.

Easter algorithm: Anonymous Gregorian (O'Beirne 1961).
All derived dates flow from Easter — no hard-coded seasons.
"""

from datetime import date, timedelta
from dataclasses import dataclass
from typing import Optional


@dataclass
class LiturgicalDay:
    date: date
    season: str           # "Advent" | "Christmas" | "Ordinary Time" | "Lent" | "Holy Week" | "Easter"
    week: int             # Week number within season
    weekday_name: str     # "Sunday" | "Monday" ... "Saturday"
    color: str            # "Green" | "Purple" | "White" | "Red" | "Rose" | "Gold"
    display: str          # Human-friendly label e.g. "6th Sunday in Ordinary Time"
    feast: Optional[str]  # Saint/feast name if applicable
    liturgical_year: str  # "A" | "B" | "C"


# ── Fixed feasts (month, day) ────────────────────────────────────────────────
FIXED_FEASTS: dict[tuple, tuple] = {
    (1, 1):  ("Solemnity of Mary, Mother of God", "White"),
    (1, 6):  ("Epiphany of the Lord", "White"),
    (2, 2):  ("Presentation of the Lord", "White"),
    (2, 14): ("Saints Cyril and Methodius", "White"),
    (3, 19): ("Saint Joseph, Spouse of the Virgin Mary", "White"),
    (3, 25): ("Annunciation of the Lord", "White"),
    (6, 24): ("Birth of Saint John the Baptist", "White"),
    (6, 29): ("Saints Peter and Paul, Apostles", "Red"),
    (8, 6):  ("Transfiguration of the Lord", "White"),
    (8, 15): ("Assumption of the Blessed Virgin Mary", "White"),
    (9, 8):  ("Birth of the Blessed Virgin Mary", "White"),
    (9, 14): ("Exaltation of the Holy Cross", "Red"),
    (10, 2): ("Guardian Angels", "White"),
    (11, 1): ("All Saints", "White"),
    (11, 2): ("All Souls", "Black/Purple"),
    (11, 9): ("Dedication of the Lateran Basilica", "White"),
    (12, 8): ("Immaculate Conception of the Blessed Virgin Mary", "White"),
    (12, 25): ("Nativity of the Lord", "White"),
    (12, 26): ("Saint Stephen", "Red"),
    (12, 27): ("Saint John the Apostle", "White"),
    (12, 28): ("Holy Innocents", "Red"),
}


def _easter(year: int) -> date:
    """Gregorian Easter algorithm (Anonymous / Meeus table-based)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(114 + h + l - 7 * m, 31)
    return date(year, month, day + 1)


def _ordinal(n: int) -> str:
    suffixes = {1: "st", 2: "nd", 3: "rd"}
    return f"{n}{suffixes.get(n if n < 20 else n % 10, 'th')}"


def _liturgical_year(year: int) -> str:
    """Year A/B/C — determined by the Sunday cycle starting Advent."""
    # Cycle starts Advent of previous year for A/B/C
    cycle = (year - 1) % 3  # 2024 Advent = Year B → returns "B"
    return ["A", "B", "C"][cycle]


WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def get_liturgical_day(for_date: Optional[date] = None) -> LiturgicalDay:
    """Return the complete liturgical characterisation for a given date."""
    d = for_date or date.today()
    year = d.year
    weekday_name = WEEKDAY_NAMES[d.weekday()]  # Monday=0, Sunday=6

    # ── Compute key dates for this liturgical year ────────────────────────────
    easter = _easter(year)
    easter_next = _easter(year + 1)

    # Advent: 4 Sundays before Christmas. Start = Sunday on or nearest Nov 30.
    christmas = date(year, 12, 25)
    # Find Sunday on/before Nov 30 that is 4 Sundays before Christmas
    # Advent I = 4th Sunday before Christmas
    advent_start = christmas - timedelta(days=christmas.weekday() + 22)
    # Ensure it falls on a Sunday (weekday 6)
    while advent_start.weekday() != 6:
        advent_start -= timedelta(days=1)
    # Correct: Advent I Sunday = the one closest to but not after Nov 30
    # Simpler and correct: 4 Sundays before Christmas
    advent_start = christmas - timedelta(days=(christmas.weekday() + 1) % 7 + 21)

    advent_start_prev_year = advent_start.replace(year=year - 1)
    # Also compute next Advent for dates in Nov/Dec
    advent_start_next = christmas.replace(year=year) - timedelta(
        days=(christmas.weekday() + 1) % 7 + 21
    )

    # Lent starts Ash Wednesday = 46 days before Easter
    ash_wednesday = easter - timedelta(days=46)
    # Palm Sunday = Easter - 7
    palm_sunday = easter - timedelta(days=7)
    # Pentecost = Easter + 49
    pentecost = easter + timedelta(days=49)
    # Corpus Christi = Pentecost + 11 (Thursday, or Sunday in some countries)
    corpus_christi = pentecost + timedelta(days=11)

    # ── Also check dates against previous year's Advent (Dec of last year) ────
    christmas_prev = date(year - 1, 12, 25)
    advent_start_prev = christmas_prev - timedelta(
        days=(christmas_prev.weekday() + 1) % 7 + 21
    )
    epiphany = date(year, 1, 6)

    # ── Determine season ─────────────────────────────────────────────────────
    season = "Ordinary Time"
    week = 1
    color = "Green"
    feast_name: Optional[str] = None
    feast_color: Optional[str] = None

    # Check fixed feasts
    fixed = FIXED_FEASTS.get((d.month, d.day))
    if fixed:
        feast_name, feast_color = fixed

    # ── Advent (previous year: Dec 1 area) ────────────────────────────────────
    if advent_start_prev <= d < date(year, 1, 1):
        season = "Advent"
        color = "Purple"
        days_in = (d - advent_start_prev).days
        week = days_in // 7 + 1
        # Rose Sunday = 3rd Sunday of Advent (Gaudete)
        if week == 3 and weekday_name == "Sunday":
            color = "Rose"

    # ── Christmas Time (Jan 1 through Epiphany or Baptism of the Lord) ────────
    elif date(year, 1, 1) <= d <= date(year, 1, 13):
        season = "Christmas"
        color = "White"
        week = 1

    # ── Ordinary Time (before Lent) ───────────────────────────────────────────
    elif date(year, 1, 14) <= d < ash_wednesday:
        season = "Ordinary Time"
        color = "Green"
        # Week 1 begins after Baptism of Lord (Jan 13 area). Count from Jan 13.
        baptism_of_lord = date(year, 1, 13)
        days_in = (d - baptism_of_lord).days
        week = days_in // 7 + 2  # Week 2 starts after Baptism
        week = max(1, min(week, 34))

    # ── Lent ─────────────────────────────────────────────────────────────────
    elif ash_wednesday <= d < palm_sunday:
        season = "Lent"
        color = "Purple"
        days_in = (d - ash_wednesday).days
        week = days_in // 7 + 1
        # Laetare Sunday = 4th Sunday of Lent
        if week == 4 and weekday_name == "Sunday":
            color = "Rose"
        if d == ash_wednesday:
            feast_name = feast_name or "Ash Wednesday"

    # ── Holy Week ─────────────────────────────────────────────────────────────
    elif palm_sunday <= d < easter:
        season = "Holy Week"
        color = "Red"
        week = 1
        if d == palm_sunday:
            feast_name = feast_name or "Palm Sunday"
        elif d == easter - timedelta(days=3):
            feast_name = feast_name or "Holy Thursday"
        elif d == easter - timedelta(days=2):
            feast_name = feast_name or "Good Friday"
            color = "Red"
        elif d == easter - timedelta(days=1):
            feast_name = feast_name or "Holy Saturday"
            color = "White"

    # ── Easter Time (50 days: Easter Sunday through Pentecost) ───────────────
    elif easter <= d <= pentecost:
        season = "Easter"
        color = "White"
        days_in = (d - easter).days
        week = days_in // 7 + 1
        if d == easter:
            feast_name = feast_name or "Easter Sunday"
        elif d == easter + timedelta(days=39):
            feast_name = feast_name or "Ascension of the Lord"
        elif d == pentecost:
            feast_name = feast_name or "Pentecost Sunday"
            color = "Red"

    # ── Ordinary Time (after Pentecost) ──────────────────────────────────────
    elif pentecost < d < advent_start_next:
        season = "Ordinary Time"
        color = "Green"
        # Count back from Christ the King (last Sunday of liturgical year)
        # Ordinary Time week after Pentecost: week 9 or so through 34
        # Simple approach: count Sundays from Baptism of Lord, skipping Lent/Easter
        days_after_pentecost = (d - pentecost).days
        # Pentecost ends at week 7 of Easter, so OT continues from week ~10
        # A simpler accurate method: calculate from Advent backwards
        weeks_to_advent = (advent_start_next - d).days // 7
        week = 34 - weeks_to_advent
        week = max(9, min(week, 34))
        # Feasts that override green
        if d == corpus_christi:
            feast_name = feast_name or "Corpus Christi"
            color = "White"
        # Christ the King = last Sunday before Advent
        if weekday_name == "Sunday" and (advent_start_next - d).days < 7:
            feast_name = feast_name or "Our Lord Jesus Christ, King of the Universe"
            color = "White"

    # ── Advent (current year) ─────────────────────────────────────────────────
    elif advent_start_next <= d <= date(year, 12, 31):
        season = "Advent"
        color = "Purple"
        days_in = (d - advent_start_next).days
        week = days_in // 7 + 1
        if week == 3 and weekday_name == "Sunday":
            color = "Rose"
        if d == date(year, 12, 25):
            season = "Christmas"
            color = feast_color or "White"

    # Override color with fixed feast color if feast outranks season
    if feast_color:
        color = feast_color

    # ── Build display string ─────────────────────────────────────────────────
    ord_week = _ordinal(week)
    if season == "Advent":
        display = f"{ord_week} Week of Advent — {weekday_name}"
        if weekday_name == "Sunday":
            display = f"{ord_week} Sunday of Advent"
    elif season == "Christmas":
        display = f"Christmas Time — {weekday_name}"
    elif season == "Lent":
        display = f"{ord_week} Week of Lent — {weekday_name}"
        if weekday_name == "Sunday":
            display = f"{ord_week} Sunday of Lent"
        if d == ash_wednesday:
            display = "Ash Wednesday"
    elif season == "Holy Week":
        display = feast_name or f"Holy Week — {weekday_name}"
    elif season == "Easter":
        display = f"{ord_week} Week of Easter — {weekday_name}"
        if weekday_name == "Sunday":
            display = f"{ord_week} Sunday of Easter"
        if d == pentecost:
            display = "Pentecost Sunday"
    elif season == "Ordinary Time":
        display = f"{ord_week} Week in Ordinary Time — {weekday_name}"
        if weekday_name == "Sunday":
            display = f"{ord_week} Sunday in Ordinary Time"
    else:
        display = f"{season} — {weekday_name}"

    # Override display with feast name for solemnities
    if feast_name and season not in ("Lent", "Holy Week", "Advent"):
        display = feast_name

    lit_year = _liturgical_year(year if d >= advent_start_prev else year - 1)

    return LiturgicalDay(
        date=d,
        season=season,
        week=week,
        weekday_name=weekday_name,
        color=color,
        display=display,
        feast=feast_name,
        liturgical_year=lit_year,
    )


# ── Quick test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from datetime import date
    test_dates = [
        date(2026, 2, 18),   # Ash Wednesday
        date(2026, 2, 15),   # 6th Sunday Ordinary Time
        date(2026, 12, 25),  # Christmas
        date(2026, 4, 5),    # Easter 2026
        date(2026, 11, 29),  # Advent I
    ]
    for td in test_dates:
        ld = get_liturgical_day(td)
        print(f"{td}  →  {ld.display}  [{ld.color}]  Year {ld.liturgical_year}")
