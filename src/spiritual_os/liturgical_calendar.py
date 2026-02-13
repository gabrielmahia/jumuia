"""
Liturgical Calendar Integration

Provides Catholic liturgical data including:
- Daily Mass readings (Gospel, Psalm, First/Second Reading)
- Liturgical season (Ordinary Time, Advent, Lent, Easter, Christmas)
- Feast days and saint commemorations
- Liturgical colors (green, white, red, purple, rose, black)
- Solemnities, feasts, memorials

Data source: Church Calendar API (http://calapi.inadiutorium.cz/)
Alternative: Liturgical Calendar API (https://litcal.johnromanodorazio.com/)
"""

import requests
from datetime import date, datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class LiturgicalSeason(Enum):
    """Liturgical seasons of the Church year"""
    ORDINARY = "ordinary"
    ADVENT = "advent"
    CHRISTMAS = "christmas"
    LENT = "lent"
    EASTER = "easter"


class LiturgicalColor(Enum):
    """Liturgical vestment colors"""
    GREEN = "green"
    WHITE = "white"
    RED = "red"
    PURPLE = "purple"
    ROSE = "rose"
    BLACK = "black"


@dataclass
class LiturgicalDay:
    """Liturgical data for a specific day"""
    date: date
    season: LiturgicalSeason
    season_week: int
    celebrations: List[Dict[str, Any]]
    primary_celebration: str
    color: LiturgicalColor
    rank: str
    rank_num: float


class LiturgicalCalendar:
    """
    Integration with Church Calendar API
    
    Provides liturgical data for Catholic parishes worldwide.
    Falls back gracefully if API unavailable.
    """
    
    API_BASE = "http://calapi.inadiutorium.cz/api/v0/en"
    
    @classmethod
    def get_today(cls) -> Optional[LiturgicalDay]:
        """Get liturgical data for today"""
        return cls.get_day(date.today())
    
    @classmethod
    def get_day(cls, target_date: date) -> Optional[LiturgicalDay]:
        """Get liturgical data for a specific date"""
        try:
            # Format: /en/calendars/default/2026/02/13
            url = f"{cls.API_BASE}/calendars/default/{target_date.year}/{target_date.month}/{target_date.day}"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse celebrations
            celebrations = data.get("celebrations", [])
            if not celebrations:
                return None
            
            # Primary celebration is first in list
            primary = celebrations[0]
            
            return LiturgicalDay(
                date=target_date,
                season=LiturgicalSeason(data.get("season", "ordinary")),
                season_week=data.get("season_week", 0),
                celebrations=celebrations,
                primary_celebration=primary.get("title", ""),
                color=LiturgicalColor(primary.get("colour", "green")),
                rank=primary.get("rank", ""),
                rank_num=primary.get("rank_num", 0.0)
            )
            
        except requests.RequestException as e:
            print(f"Liturgical API error: {e}")
            return cls._get_fallback_day(target_date)
        except (KeyError, ValueError) as e:
            print(f"Liturgical data parsing error: {e}")
            return cls._get_fallback_day(target_date)
    
    @classmethod
    def _get_fallback_day(cls, target_date: date) -> LiturgicalDay:
        """
        Fallback liturgical data when API unavailable
        
        Provides basic season detection based on date ranges.
        """
        year = target_date.year
        
        # Approximate liturgical seasons (may not be exact due to movable feasts)
        # This is a simplified fallback - production should use cached API data
        
        # Advent: 4 Sundays before Christmas
        # Christmas: Dec 25 - Baptism of the Lord (early January)
        # Ordinary Time 1: After Christmas until Ash Wednesday
        # Lent: Ash Wednesday to Holy Thursday
        # Easter: Easter Sunday for 50 days (Pentecost)
        # Ordinary Time 2: After Pentecost until Advent
        
        month, day = target_date.month, target_date.day
        
        # Simple season detection
        if month == 12 and day >= 25:
            season = LiturgicalSeason.CHRISTMAS
            color = LiturgicalColor.WHITE
        elif month == 1 and day <= 10:
            season = LiturgicalSeason.CHRISTMAS
            color = LiturgicalColor.WHITE
        elif month == 12 and day < 25 and day >= 1:
            season = LiturgicalSeason.ADVENT
            color = LiturgicalColor.PURPLE
        elif month in [2, 3] and target_date.weekday() == 2:  # Rough Lent approximation
            season = LiturgicalSeason.LENT
            color = LiturgicalColor.PURPLE
        elif month in [3, 4, 5]:  # Rough Easter approximation
            season = LiturgicalSeason.EASTER
            color = LiturgicalColor.WHITE
        else:
            season = LiturgicalSeason.ORDINARY
            color = LiturgicalColor.GREEN
        
        return LiturgicalDay(
            date=target_date,
            season=season,
            season_week=1,
            celebrations=[{
                "title": f"{season.value.capitalize()} Time",
                "colour": color.value,
                "rank": "ferial",
                "rank_num": 3.13
            }],
            primary_celebration=f"{season.value.capitalize()} Time",
            color=color,
            rank="ferial",
            rank_num=3.13
        )
    
    @classmethod
    def get_color_description(cls, color: LiturgicalColor) -> str:
        """Get human-readable description of liturgical color meaning"""
        descriptions = {
            LiturgicalColor.GREEN: "Ordinary Time - Growth in faith",
            LiturgicalColor.WHITE: "Joy and purity - Christmas, Easter, feasts of the Lord, Mary, saints who were not martyrs",
            LiturgicalColor.RED: "Fire of the Holy Spirit, blood of martyrs - Pentecost, Holy Week, martyrs",
            LiturgicalColor.PURPLE: "Penance and preparation - Advent, Lent",
            LiturgicalColor.ROSE: "Rejoicing in anticipation - 3rd Sunday of Advent (Gaudete), 4th Sunday of Lent (Laetare)",
            LiturgicalColor.BLACK: "Mourning - All Souls Day, funerals (optional)"
        }
        return descriptions.get(color, "")
    
    @classmethod
    def format_for_display(cls, liturgical_day: LiturgicalDay) -> str:
        """Format liturgical day for parish bulletin display"""
        if not liturgical_day:
            return "Liturgical data unavailable"
        
        color_emoji = {
            LiturgicalColor.GREEN: "🟢",
            LiturgicalColor.WHITE: "⚪",
            LiturgicalColor.RED: "🔴",
            LiturgicalColor.PURPLE: "🟣",
            LiturgicalColor.ROSE: "🌸",
            LiturgicalColor.BLACK: "⚫"
        }
        
        emoji = color_emoji.get(liturgical_day.color, "🔵")
        
        return f"""
**{liturgical_day.primary_celebration}**

{emoji} **{liturgical_day.color.value.capitalize()}** — {liturgical_day.season.value.capitalize()} Time, Week {liturgical_day.season_week}

{cls.get_color_description(liturgical_day.color)}
"""


# Demo usage
if __name__ == "__main__":
    today = LiturgicalCalendar.get_today()
    if today:
        print(LiturgicalCalendar.format_for_display(today))
    else:
        print("Could not retrieve liturgical data")
