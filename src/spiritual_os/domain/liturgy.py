"""
Liturgy Module - Liturgical season awareness and feast day tracking
"""

from datetime import datetime, date
from enum import Enum
from typing import Optional, List


class LiturgicalSeason(Enum):
    """Catholic liturgical seasons"""
    ADVENT = "Advent"
    CHRISTMAS = "Christmas"
    EPIPHANY = "Epiphany"
    LENT = "Lent"
    EASTER = "Easter"
    ORDINARY = "Ordinary Time"


@dataclass
class FeastDay:
    """Feast or solemnity in the Church calendar"""
    name: str
    date_str: str  # MM-DD format
    season: str
    liturgical_color: str  # white, red, purple, green
    rank: str  # solemnity, feast, memorial, optional memorial
    description: str = ""
    
    def is_today(self) -> bool:
        """Check if feast is today"""
        today = date.today()
        month, day = map(int, self.date_str.split("-"))
        return today.month == month and today.day == day


class LiturgyCalendar:
    """Gregorian/Church calendar context"""
    
    # Minimal feast day dataset (extensible)
    MAJOR_FEASTS = [
        FeastDay("Solemnity of Mary", "01-01", "Christmas", "white", "solemnity"),
        FeastDay("Candlemas", "02-02", "Epiphany", "white", "feast"),
        FeastDay("Ash Wednesday", "varies", "Lent", "purple", "solemnity"),
        FeastDay("Saint Patrick", "03-17", "Lent", "green", "memorial"),
        FeastDay("Annunciation", "03-25", "Lent/Easter", "white", "solemnity"),
        FeastDay("Palm Sunday", "varies", "Lent", "red", "solemnity"),
        FeastDay("Easter Sunday", "varies", "Easter", "white", "solemnity"),
        FeastDay("Ascension", "varies", "Easter", "white", "solemnity"),
        FeastDay("Pentecost", "varies", "Easter", "red", "solemnity"),
        FeastDay("Sacred Heart", "varies", "Ordinary", "white", "solemnity"),
        FeastDay("Saints Peter & Paul", "06-29", "Ordinary", "red", "solemnity"),
        FeastDay("Assumption of Mary", "08-15", "Ordinary", "white", "solemnity"),
        FeastDay("All Saints", "11-01", "Ordinary", "white", "solemnity"),
        FeastDay("All Souls", "11-02", "Ordinary", "black", "solemnity"),
        FeastDay("Immaculate Conception", "12-08", "Advent", "white", "solemnity"),
        FeastDay("Christmas", "12-25", "Christmas", "white", "solemnity"),
    ]
    
    @staticmethod
    def current_season() -> LiturgicalSeason:
        """Determine current liturgical season"""
        today = date.today()
        month = today.month
        
        # Simplified season determination
        if month in [11, 12] and month == 12 and today.day < 25:
            return LiturgicalSeason.ADVENT
        elif month in [12, 1] and (month == 12 or today.day <= 6):
            return LiturgicalSeason.CHRISTMAS
        elif month in [1, 2]:
            return LiturgicalSeason.EPIPHANY
        elif month in [2, 3, 4]:
            return LiturgicalSeason.LENT
        elif month in [3, 4, 5]:
            return LiturgicalSeason.EASTER
        else:
            return LiturgicalSeason.ORDINARY
    
    @staticmethod
    def current_color() -> str:
        """Liturgical color for today"""
        season = LiturgyCalendar.current_season()
        colors = {
            LiturgicalSeason.ADVENT: "purple",
            LiturgicalSeason.CHRISTMAS: "white",
            LiturgicalSeason.EPIPHANY: "white",
            LiturgicalSeason.LENT: "purple",
            LiturgicalSeason.EASTER: "white",
            LiturgicalSeason.ORDINARY: "green"
        }
        return colors.get(season, "green")
    
    @staticmethod
    def today_feast() -> Optional[FeastDay]:
        """Get today's feast if any"""
        for feast in LiturgyCalendar.MAJOR_FEASTS:
            if feast.is_today():
                return feast
        return None
    
    @staticmethod
    def upcoming_feasts(days_ahead: int = 14) -> List[FeastDay]:
        """Get upcoming major feasts"""
        # Simplified: just return major feasts
        return LiturgyCalendar.MAJOR_FEASTS


def season_description() -> str:
    """Human-readable season description"""
    season = LiturgyCalendar.current_season()
    descriptions = {
        LiturgicalSeason.ADVENT: "Waiting with longing for Christ's coming",
        LiturgicalSeason.CHRISTMAS: "Celebrating Christ's incarnation",
        LiturgicalSeason.EPIPHANY: "Revealing Christ to all nations",
        LiturgicalSeason.LENT: "Preparing through prayer, fasting, almsgiving",
        LiturgicalSeason.EASTER: "Celebrating Christ's resurrection",
        LiturgicalSeason.ORDINARY: "Living out discipleship in ordinary time"
    }
    return descriptions.get(season, "")


from dataclasses import dataclass
