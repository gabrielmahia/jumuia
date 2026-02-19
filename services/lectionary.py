"""
Catholic Lectionary Service
============================
Provides real liturgical readings based on:
- Year cycle (A/B/C) — 3-year cycle for Sundays
- Weekday cycle (I/II) — 2-year cycle for weekdays
- Liturgical season — Advent, Christmas, Lent, Easter, Ordinary Time
- Major feast days — override ordinary readings

This is not a complete lectionary database (that would require licensing).
It provides the correct scripture references so parishioners can look up
the text in any Bible or on universalis.com / usccb.org.

For USSD: returns short reference (fits 182 char limit)
For app: returns full reference + context
"""

from datetime import date, timedelta
from typing import Tuple


# ── YEAR CYCLE ────────────────────────────────────────────────────────────────

def _sunday_cycle(year: int) -> str:
    """Returns 'A', 'B', or 'C' for the liturgical year starting in Advent."""
    # Liturgical year starts in Advent (late Nov/early Dec)
    # Year A: 2023-24, 2026-27, 2029-30 (year % 3 == 1 for the calendar year of Advent start)
    # Simple rule: liturgical year N uses cycle based on N % 3
    # 2025-26 = Year C, 2026-27 = Year A, 2027-28 = Year B
    cycles = {0: "B", 1: "C", 2: "A"}
    return cycles[year % 3]


def _weekday_cycle(year: int) -> str:
    """Returns 'I' (odd years) or 'II' (even years) for weekday cycle."""
    return "I" if year % 2 == 1 else "II"


# ── LITURGICAL CALENDAR ───────────────────────────────────────────────────────

def _easter(year: int) -> date:
    """Compute Easter Sunday using Butcher's algorithm."""
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


def _advent_start(year: int) -> date:
    """First Sunday of Advent (4 Sundays before Christmas)."""
    christmas = date(year, 12, 25)
    # Sunday on or before Dec 3 (closest Sunday before Dec 25 minus 3 weeks)
    days_to_sunday = christmas.weekday() + 1  # days since last Sunday
    if days_to_sunday == 7:
        days_to_sunday = 0
    fourth_sunday_before = christmas - timedelta(days=days_to_sunday + 21)
    return fourth_sunday_before


def _liturgical_season(today: date) -> Tuple[str, int]:
    """
    Returns (season, week_number).
    Seasons: Advent, Christmas, Lent, Easter, Ordinary
    """
    year = today.year
    easter = _easter(year)
    advent = _advent_start(year)
    prev_advent = _advent_start(year - 1)
    prev_easter = _easter(year - 1)

    # Ash Wednesday = 46 days before Easter
    ash_wednesday = easter - timedelta(days=46)
    # Pentecost = 49 days after Easter
    pentecost = easter + timedelta(days=49)
    # Christmas season ends Baptism of the Lord (Sunday after Jan 6, or Jan 13 if Jan 6 is Sunday)
    epiphany = date(year, 1, 6)
    baptism_of_lord = epiphany + timedelta(days=(7 - epiphany.weekday()) % 7 or 7)

    if prev_advent <= today < date(year, 1, 6):
        # Christmas season (Dec Advent ended, into Christmas)
        return "Christmas", 0
    elif today <= baptism_of_lord:
        return "Christmas", 0
    elif baptism_of_lord < today < ash_wednesday:
        weeks = (today - baptism_of_lord).days // 7 + 1
        return "Ordinary", weeks
    elif ash_wednesday <= today < easter:
        weeks = (today - ash_wednesday).days // 7 + 1
        return "Lent", weeks
    elif easter <= today <= pentecost:
        weeks = (today - easter).days // 7 + 1
        return "Easter", weeks
    elif pentecost < today < advent:
        weeks = (today - pentecost).days // 7 + 34  # continues from week 34ish
        return "Ordinary", min(weeks, 34)
    else:
        weeks = (today - advent).days // 7 + 1
        return "Advent", weeks


# ── MAJOR FEAST DAYS ──────────────────────────────────────────────────────────
# Fixed feasts that override ordinary readings
FIXED_FEASTS = {
    (1, 1):  ("Solemnity of Mary", "Num 6:22-27", "Gal 4:4-7", "Lk 2:16-21"),
    (1, 6):  ("Epiphany", "Is 60:1-6", "Eph 3:2-3,5-6", "Mt 2:1-12"),
    (2, 2):  ("Presentation of the Lord", "Mal 3:1-4", "Heb 2:14-18", "Lk 2:22-40"),
    (3, 19): ("St Joseph", "2 Sam 7:4-16", "Rom 4:13-18", "Mt 1:16-24"),
    (3, 25): ("Annunciation", "Is 7:10-14", "Heb 10:4-10", "Lk 1:26-38"),
    (8, 15): ("Assumption of Mary", "Rev 11:19;12:1-6,10", "1 Cor 15:20-27", "Lk 1:39-56"),
    (11, 1): ("All Saints", "Rev 7:2-4,9-14", "1 Jn 3:1-3", "Mt 5:1-12"),
    (11, 2): ("All Souls", "Is 25:6-9", "Rom 8:14-23", "Jn 6:37-40"),
    (12, 8): ("Immaculate Conception", "Gen 3:9-15,20", "Eph 1:3-6,11-12", "Lk 1:26-38"),
    (12, 25):("Christmas — Midnight", "Is 9:1-6", "Tit 2:11-14", "Lk 2:1-14"),
}

# Easter-relative feasts
def _moveable_feasts(year: int) -> dict:
    easter = _easter(year)
    ash = easter - timedelta(days=46)
    return {
        ash:                      ("Ash Wednesday", "Jl 2:12-18", "2 Cor 5:20-6:2", "Mt 6:1-6,16-18"),
        easter - timedelta(days=7):("Palm Sunday", "Is 50:4-7", "Phil 2:6-11", "Lk 22-23"),
        easter - timedelta(days=3):("Holy Thursday", "Ex 12:1-8,11-14", "1 Cor 11:23-26", "Jn 13:1-15"),
        easter - timedelta(days=2):("Good Friday", "Is 52:13-53:12", "Heb 4:14-16;5:7-9", "Jn 18-19"),
        easter:                   ("Easter Sunday", "Acts 10:34,37-43", "Col 3:1-4", "Jn 20:1-9"),
        easter + timedelta(days=39):("Ascension", "Acts 1:1-11", "Eph 1:17-23", "Lk 24:46-53"),
        easter + timedelta(days=49):("Pentecost", "Acts 2:1-11", "1 Cor 12:3-7,12-13", "Jn 20:19-23"),
    }


# ── WEEKDAY READINGS BY SEASON ────────────────────────────────────────────────
# Simplified weekday references — full weekday lectionary has 730 entries
# We provide the liturgical week and season so parishioners can look up the rest

WEEKDAY_BOOKS = {
    "Advent": {
        1: ("Is 2:1-5", "Mt 8:5-11"), 2: ("Is 11:1-10", "Lk 10:21-24"),
        3: ("Is 25:6-10", "Mt 11:25-30"), 4: ("Zeph 3:14-18", "Lk 1:39-45"),
    },
    "Lent": {
        1: ("Lev 19:1-2,11-18", "Mt 25:31-46"), 2: ("Dan 9:4-10", "Lk 6:36-38"),
        3: ("2 Kgs 5:1-15", "Lk 4:24-30"), 4: ("Is 65:17-21", "Jn 4:43-54"),
        5: ("Jer 31:31-34", "Jn 8:1-11"),
    },
    "Easter": {
        1: ("Acts 2:14,22-33", "Jn 20:11-18"), 2: ("Acts 4:32-37", "Jn 3:7-15"),
        3: ("Acts 5:27-33", "Jn 3:31-36"), 4: ("Acts 11:1-18", "Jn 10:1-10"),
        5: ("Acts 14:5-18", "Jn 14:21-26"), 6: ("Acts 16:11-15", "Jn 15:26-16:4"),
        7: ("Acts 20:17-27", "Jn 17:1-11"),
    },
}


# ── SUNDAY READINGS (abbreviated — key Sundays per cycle) ─────────────────────
# Structure: cycle → season → week → (first, second, gospel)
SUNDAY_READINGS = {
    "A": {
        "Advent": {
            1: ("Is 2:1-5", "Rom 13:11-14", "Mt 24:37-44"),
            2: ("Is 11:1-10", "Rom 15:4-9", "Mt 3:1-12"),
            3: ("Is 35:1-6,10", "Jas 5:7-10", "Mt 11:2-11"),
            4: ("Is 7:10-14", "Rom 1:1-7", "Mt 1:18-24"),
        },
        "Lent": {
            1: ("Gen 2:7-9;3:1-7", "Rom 5:12-19", "Mt 4:1-11"),
            2: ("Gen 12:1-4", "2 Tim 1:8-10", "Mt 17:1-9"),
            3: ("Ex 17:3-7", "Rom 5:1-2,5-8", "Jn 4:5-42"),
            4: ("1 Sam 16:1,6-7,10-13", "Eph 5:8-14", "Jn 9:1-41"),
            5: ("Ezek 37:12-14", "Rom 8:8-11", "Jn 11:1-45"),
        },
        "Easter": {
            1: ("Acts 10:34,37-43", "Col 3:1-4", "Jn 20:1-9"),
            2: ("Acts 2:42-47", "1 Pet 1:3-9", "Jn 20:19-31"),
            3: ("Acts 2:14,22-28", "1 Pet 1:17-21", "Lk 24:13-35"),
            4: ("Acts 2:14,36-41", "1 Pet 2:20-25", "Jn 10:1-10"),
            5: ("Acts 6:1-7", "1 Pet 2:4-9", "Jn 14:1-12"),
            6: ("Acts 8:5-8,14-17", "1 Pet 3:15-18", "Jn 14:15-21"),
            7: ("Acts 1:12-14", "1 Pet 4:13-16", "Jn 17:1-11"),
        },
        "Ordinary": {
            2: ("Is 49:3,5-6", "1 Cor 1:1-3", "Jn 1:29-34"),
            3: ("Is 8:23-9:3", "1 Cor 1:10-13,17", "Mt 4:12-23"),
            5: ("Is 58:7-10", "1 Cor 2:1-5", "Mt 5:13-16"),
            6: ("Sir 15:15-20", "1 Cor 2:6-10", "Mt 5:17-37"),
            8: ("Is 49:14-15", "1 Cor 4:1-5", "Mt 6:24-34"),
            10: ("Hos 6:3-6", "Rom 4:18-25", "Mt 9:9-13"),
            15: ("Is 55:10-11", "Rom 8:18-23", "Mt 13:1-23"),
            17: ("1 Kgs 3:5,7-12", "Rom 8:28-30", "Mt 13:44-52"),
            20: ("Is 56:1,6-7", "Rom 11:13-15,29-32", "Mt 15:21-28"),
            25: ("Is 55:6-9", "Phil 1:20-24,27", "Mt 20:1-16"),
            30: ("Ex 22:20-26", "1 Thes 1:5-10", "Mt 22:34-40"),
        },
    },
    "B": {
        "Advent": {
            1: ("Is 63:16-17,19;64:2-7", "1 Cor 1:3-9", "Mk 13:33-37"),
            2: ("Is 40:1-5,9-11", "2 Pet 3:8-14", "Mk 1:1-8"),
            3: ("Is 61:1-2,10-11", "1 Thes 5:16-24", "Jn 1:6-8,19-28"),
            4: ("2 Sam 7:1-5,8-12,14,16", "Rom 16:25-27", "Lk 1:26-38"),
        },
        "Lent": {
            1: ("Gen 9:8-15", "1 Pet 3:18-22", "Mk 1:12-15"),
            2: ("Gen 22:1-2,9-13,15-18", "Rom 8:31-34", "Mk 9:2-10"),
            3: ("Ex 20:1-17", "1 Cor 1:22-25", "Jn 2:13-25"),
            4: ("2 Chr 36:14-16,19-23", "Eph 2:4-10", "Jn 3:14-21"),
            5: ("Jer 31:31-34", "Heb 5:7-9", "Jn 12:20-33"),
        },
        "Easter": {
            1: ("Acts 10:34,37-43", "Col 3:1-4", "Mk 16:1-6"),
            2: ("Acts 4:32-35", "1 Jn 5:1-6", "Jn 20:19-31"),
            3: ("Acts 3:13-15,17-19", "1 Jn 2:1-5", "Lk 24:35-48"),
            4: ("Acts 4:8-12", "1 Jn 3:1-2", "Jn 10:11-18"),
            5: ("Acts 9:26-31", "1 Jn 3:18-24", "Jn 15:1-8"),
            6: ("Acts 10:25-26,34-35,44-48", "1 Jn 4:7-10", "Jn 15:9-17"),
            7: ("Acts 1:15-17,20-26", "1 Jn 4:11-16", "Jn 17:11-19"),
        },
        "Ordinary": {
            3: ("Jon 3:1-5,10", "1 Cor 7:29-31", "Mk 1:14-20"),
            5: ("Job 7:1-4,6-7", "1 Cor 9:16-19,22-23", "Mk 1:29-39"),
            10: ("Gen 3:9-15", "2 Cor 4:13-5:1", "Mk 3:20-35"),
            16: ("Jer 23:1-6", "Eph 2:13-18", "Mk 6:30-34"),
            25: ("Wis 2:12,17-20", "Jas 3:16-4:3", "Mk 9:30-37"),
            30: ("Jer 31:7-9", "Heb 5:1-6", "Mk 10:46-52"),
        },
    },
    "C": {
        "Advent": {
            1: ("Jer 33:14-16", "1 Thes 3:12-4:2", "Lk 21:25-28,34-36"),
            2: ("Bar 5:1-9", "Phil 1:4-6,8-11", "Lk 3:1-6"),
            3: ("Zeph 3:14-18", "Phil 4:4-7", "Lk 3:10-18"),
            4: ("Mic 5:1-4", "Heb 10:5-10", "Lk 1:39-45"),
        },
        "Lent": {
            1: ("Deut 26:4-10", "Rom 10:8-13", "Lk 4:1-13"),
            2: ("Gen 15:5-12,17-18", "Phil 3:17-4:1", "Lk 9:28-36"),
            3: ("Ex 3:1-8,13-15", "1 Cor 10:1-6,10-12", "Lk 13:1-9"),
            4: ("Jos 5:9,10-12", "2 Cor 5:17-21", "Lk 15:1-3,11-32"),
            5: ("Is 43:16-21", "Phil 3:8-14", "Jn 8:1-11"),
        },
        "Easter": {
            1: ("Acts 10:34,37-43", "Col 3:1-4", "Jn 20:1-9"),
            2: ("Acts 5:12-16", "Rev 1:9-11,12-13,17-19", "Jn 20:19-31"),
            3: ("Acts 5:27-32,40-41", "Rev 5:11-14", "Jn 21:1-19"),
            4: ("Acts 13:14,43-52", "Rev 7:9,14-17", "Jn 10:27-30"),
            5: ("Acts 14:21-27", "Rev 21:1-5", "Jn 13:31-35"),
            6: ("Acts 15:1-2,22-29", "Rev 21:10-14,22-23", "Jn 14:23-29"),
            7: ("Acts 7:55-60", "Rev 22:12-14,16-17,20", "Jn 17:20-26"),
        },
        "Ordinary": {
            2: ("Is 62:1-5", "1 Cor 12:4-11", "Jn 2:1-11"),
            3: ("Neh 8:2-4,5-6,8-10", "1 Cor 12:12-30", "Lk 1:1-4;4:14-21"),
            5: ("Is 6:1-2,3-8", "1 Cor 15:1-11", "Lk 5:1-11"),
            6: ("Jer 17:5-8", "1 Cor 15:12,16-20", "Lk 6:17,20-26"),
            10: ("1 Kgs 17:17-24", "Gal 1:11-19", "Lk 7:11-17"),
            15: ("Deut 30:10-14", "Col 1:15-20", "Lk 10:25-37"),
            19: ("Wis 18:6-9", "Heb 11:1-2,8-19", "Lk 12:32-48"),
            24: ("Ex 32:7-11,13-14", "1 Tim 1:12-17", "Lk 15:1-32"),
            28: ("2 Kgs 5:14-17", "2 Tim 2:8-13", "Lk 17:11-19"),
            33: ("Mal 3:19-20", "2 Thes 3:7-12", "Lk 21:5-19"),
        },
    },
}


# ── PUBLIC API ────────────────────────────────────────────────────────────────

def get_reading(today: date = None) -> dict:
    """
    Returns today's liturgical reading information.
    
    Returns dict with:
        feast:    feast name if applicable, else None
        season:   liturgical season
        week:     week number in season
        cycle:    A/B/C (Sunday) or I/II (weekday)
        readings: list of scripture references
        short:    compact string for USSD (fits 182 chars)
        link:     URL to full readings online
    """
    if today is None:
        today = date.today()

    year = today.year
    season, week = _liturgical_season(today)
    sunday_cycle = _sunday_cycle(year)
    weekday_cycle = _weekday_cycle(year)
    is_sunday = today.weekday() == 6

    # Check fixed feasts first
    feast_key = (today.month, today.day)
    if feast_key in FIXED_FEASTS:
        name, first, second, gospel = FIXED_FEASTS[feast_key]
        refs = [first, second, gospel] if second else [first, gospel]
        short = f"{name}\n{first} · {gospel}"
        return {
            "feast": name, "season": season, "week": week,
            "cycle": sunday_cycle, "readings": refs,
            "short": short[:175],
            "link": "usccb.org/bible/readings"
        }

    # Check moveable feasts
    moveable = _moveable_feasts(year)
    if today in moveable:
        name, first, second, gospel = moveable[today]
        refs = [first, second, gospel] if second else [first, gospel]
        short = f"{name}\n{first} · {gospel}"
        return {
            "feast": name, "season": season, "week": week,
            "cycle": sunday_cycle, "readings": refs,
            "short": short[:175],
            "link": "usccb.org/bible/readings"
        }

    # Sunday readings
    if is_sunday:
        cycle_readings = SUNDAY_READINGS.get(sunday_cycle, {})
        season_readings = cycle_readings.get(season, {})
        # Find closest week
        available_weeks = sorted(season_readings.keys())
        closest = min(available_weeks, key=lambda w: abs(w - week), default=None) if available_weeks else None

        if closest:
            first, second, gospel = season_readings[closest]
            short = (f"Year {sunday_cycle} · {season} Wk{week}\n"
                    f"{first} | {second}\nGospel: {gospel}")
            return {
                "feast": None,
                "season": season, "week": week, "cycle": sunday_cycle,
                "readings": [first, second, gospel],
                "short": short[:175],
                "link": "usccb.org/bible/readings"
            }

    # Weekday readings
    day_name = today.strftime("%A")
    season_weekdays = WEEKDAY_BOOKS.get(season, {})
    closest_week = min(season_weekdays.keys(), key=lambda w: abs(w-week), default=1) if season_weekdays else 1
    
    if season_weekdays and closest_week in season_weekdays:
        first, gospel = season_weekdays[closest_week]
        short = (f"{day_name} · {season} Wk{week} (Yr {weekday_cycle})\n"
                f"{first}\nGospel: {gospel}")
    else:
        short = (f"{day_name} · {season} Week {week}\n"
                f"Year {weekday_cycle} weekday readings\n"
                f"See: usccb.org/bible/readings")
    
    readings = list(season_weekdays.get(closest_week, ("See usccb.org",)))
    return {
        "feast": None,
        "season": season, "week": week, "cycle": weekday_cycle,
        "readings": readings,
        "short": short[:175],
        "link": "usccb.org/bible/readings"
    }


def ussd_reading() -> str:
    """Returns reading string formatted for USSD (max 175 chars)."""
    r = get_reading()
    if r["feast"]:
        return f"Feast: {r['feast']}\n{r['short']}"
    return r["short"]


def liturgical_color(season: str) -> str:
    """Returns liturgical color for the season."""
    return {
        "Advent": "Purple / Rose (3rd Sunday)",
        "Christmas": "White",
        "Lent": "Purple / Red (Palm Sunday & Good Friday)",
        "Easter": "White / Gold",
        "Ordinary": "Green",
    }.get(season, "Green")
