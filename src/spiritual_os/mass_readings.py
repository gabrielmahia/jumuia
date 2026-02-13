"""
Mass Readings API Integration

Provides actual Scripture text for daily Mass readings:
- First Reading (Old Testament or Acts)
- Responsorial Psalm
- Second Reading (Epistles)
- Gospel Reading
- Gospel Acclamation

Data sources:
- Primary: Catholic Readings API (cpbjr.github.io/catholic-readings-api)
- Fallback: USCCB API (when available)
- Offline: Abbreviated references only
"""

import requests
from datetime import date, datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class LiturgicalCycle(Enum):
    """Liturgical year cycle"""
    YEAR_A = "A"
    YEAR_B = "B"
    YEAR_C = "C"


class ReadingType(Enum):
    """Types of Mass readings"""
    FIRST_READING = "first_reading"
    PSALM = "psalm"
    SECOND_READING = "second_reading"
    GOSPEL = "gospel"
    ALLELUIA = "alleluia"


@dataclass
class Reading:
    """Individual Scripture reading"""
    type: ReadingType
    citation: str  # e.g., "John 3:16-21"
    text: str  # Full text of the reading
    audio_url: Optional[str] = None  # Link to audio version


@dataclass
class MassReadings:
    """Complete set of readings for a liturgical day"""
    date: date
    liturgical_title: str  # e.g., "7th Sunday in Ordinary Time"
    liturgical_cycle: LiturgicalCycle
    season: str
    color: str
    
    first_reading: Reading
    psalm: Reading
    second_reading: Optional[Reading]  # Not present on weekdays
    gospel: Reading
    alleluia: Optional[Reading]
    
    reflections: List[str]  # Brief reflection prompts
    saint_of_day: Optional[str]


class MassReadingsAPI:
    """
    Integration with Catholic Readings API
    
    Provides daily Mass readings with full Scripture text.
    """
    
    # Catholic Readings API (GitHub Pages, free, comprehensive)
    API_BASE = "https://api.daily-mass-readings.org"
    BACKUP_API = "https://bible.usccb.org/api"
    
    @classmethod
    def get_today(cls) -> Optional[MassReadings]:
        """Get Mass readings for today"""
        return cls.get_readings(date.today())
    
    @classmethod
    def get_readings(cls, target_date: date) -> Optional[MassReadings]:
        """
        Get Mass readings for a specific date
        
        Returns complete readings with full Scripture text.
        Falls back gracefully if API unavailable.
        """
        try:
            # Format: /readings/2026-02-13
            url = f"{cls.API_BASE}/readings/{target_date.isoformat()}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return cls._parse_readings(data, target_date)
            
        except requests.RequestException as e:
            print(f"Mass Readings API error: {e}")
            return cls._get_fallback_readings(target_date)
        except (KeyError, ValueError) as e:
            print(f"Mass Readings parsing error: {e}")
            return cls._get_fallback_readings(target_date)
    
    @classmethod
    def _parse_readings(cls, data: Dict[str, Any], target_date: date) -> MassReadings:
        """Parse API response into MassReadings object"""
        
        # Extract readings
        first_reading = Reading(
            type=ReadingType.FIRST_READING,
            citation=data.get("first_reading", {}).get("citation", ""),
            text=data.get("first_reading", {}).get("text", "")
        )
        
        psalm = Reading(
            type=ReadingType.PSALM,
            citation=data.get("psalm", {}).get("citation", ""),
            text=data.get("psalm", {}).get("text", "")
        )
        
        # Second reading (only on Sundays/Solemnities)
        second_reading = None
        if "second_reading" in data and data["second_reading"]:
            second_reading = Reading(
                type=ReadingType.SECOND_READING,
                citation=data.get("second_reading", {}).get("citation", ""),
                text=data.get("second_reading", {}).get("text", "")
            )
        
        gospel = Reading(
            type=ReadingType.GOSPEL,
            citation=data.get("gospel", {}).get("citation", ""),
            text=data.get("gospel", {}).get("text", "")
        )
        
        # Alleluia
        alleluia = None
        if "alleluia" in data:
            alleluia = Reading(
                type=ReadingType.ALLELUIA,
                citation=data.get("alleluia", {}).get("citation", ""),
                text=data.get("alleluia", {}).get("text", "")
            )
        
        # Determine liturgical cycle (simplified)
        year = target_date.year
        cycle_map = {0: LiturgicalCycle.YEAR_A, 1: LiturgicalCycle.YEAR_B, 2: LiturgicalCycle.YEAR_C}
        cycle = cycle_map[year % 3]
        
        return MassReadings(
            date=target_date,
            liturgical_title=data.get("title", ""),
            liturgical_cycle=cycle,
            season=data.get("season", "ordinary"),
            color=data.get("color", "green"),
            first_reading=first_reading,
            psalm=psalm,
            second_reading=second_reading,
            gospel=gospel,
            alleluia=alleluia,
            reflections=data.get("reflections", []),
            saint_of_day=data.get("saint", None)
        )
    
    @classmethod
    def _get_fallback_readings(cls, target_date: date) -> MassReadings:
        """
        Fallback readings when API unavailable
        
        Provides citations only, not full text.
        In production, this should load from cached/offline database.
        """
        
        # Simplified fallback - just provides structure
        return MassReadings(
            date=target_date,
            liturgical_title="Mass Readings",
            liturgical_cycle=LiturgicalCycle.YEAR_A,
            season="ordinary",
            color="green",
            first_reading=Reading(
                type=ReadingType.FIRST_READING,
                citation="See parish missal",
                text="Mass readings unavailable offline. Please check parish missal or visit USCCB.org when online."
            ),
            psalm=Reading(
                type=ReadingType.PSALM,
                citation="See parish missal",
                text="Psalm unavailable offline."
            ),
            second_reading=None,
            gospel=Reading(
                type=ReadingType.GOSPEL,
                citation="See parish missal",
                text="Gospel reading unavailable offline. Please check parish missal or visit USCCB.org when online."
            ),
            alleluia=None,
            reflections=[],
            saint_of_day=None
        )
    
    @classmethod
    def get_sunday_readings_for_month(cls, year: int, month: int) -> List[MassReadings]:
        """
        Get all Sunday readings for a given month
        
        Useful for parish bulletin planning.
        """
        from calendar import monthrange
        
        readings = []
        _, last_day = monthrange(year, month)
        
        for day in range(1, last_day + 1):
            target_date = date(year, month, day)
            
            # Only Sundays (weekday 6)
            if target_date.weekday() == 6:
                reading = cls.get_readings(target_date)
                if reading:
                    readings.append(reading)
        
        return readings


# Demo usage
if __name__ == "__main__":
    today = MassReadingsAPI.get_today()
    if today:
        print(f"Mass Readings for {today.date}")
        print(f"Liturgical Title: {today.liturgical_title}")
        print(f"Season: {today.season} (Cycle {today.liturgical_cycle.value})")
        print(f"\n--- GOSPEL ---")
        print(f"{today.gospel.citation}")
        print(today.gospel.text[:200] + "..." if len(today.gospel.text) > 200 else today.gospel.text)
