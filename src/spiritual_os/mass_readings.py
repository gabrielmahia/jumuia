"""
Catholic Mass Readings Integration

Provides daily Mass readings (Gospel, Psalm, First Reading, Second Reading)
from the Catholic Lectionary.

Data sources:
- Primary: cpbjr.github.io/catholic-readings-api (USCCB approved)
- Fallback: USCCB.org (official US Conference of Catholic Bishops)
- Cache: Local storage for offline access
"""

import requests
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class Reading:
    """Individual Mass reading"""
    type: str  # "first_reading", "psalm", "second_reading", "gospel"
    citation: str  # e.g., "John 3:16-21"
    text: str
    audio_url: Optional[str] = None


@dataclass
class MassReadings:
    """Complete set of readings for a Mass"""
    date: date
    liturgical_day: str  # e.g., "Second Sunday of Lent"
    first_reading: Reading
    responsorial_psalm: Reading
    second_reading: Optional[Reading]  # Sometimes absent on weekdays
    gospel_acclamation: str
    gospel: Reading
    season: str  # "advent", "christmas", "ordinary", "lent", "easter"
    color: str  # "green", "white", "red", "purple", "rose"


class MassReadingsAPI:
    """
    Integration with Catholic Mass readings APIs
    
    Provides daily Gospel, Psalm, and other readings for Catholic Mass.
    Caches readings locally for offline access.
    """
    
    # Catholic Readings API (GitHub Pages, free, USCCB data)
    PRIMARY_API = "https://cpbjr.github.io/catholic-readings-api"
    
    # Cache directory
    CACHE_DIR = Path(__file__).parent.parent.parent / "data" / "cache" / "readings"
    
    @classmethod
    def get_today(cls) -> Optional[MassReadings]:
        """Get today's Mass readings"""
        return cls.get_readings_for_date(date.today())
    
    @classmethod
    def get_readings_for_date(cls, target_date: date) -> Optional[MassReadings]:
        """
        Get Mass readings for specific date
        
        Strategy:
        1. Check local cache
        2. Fetch from API
        3. Cache for offline use
        4. Return fallback if all fails
        """
        # Try cache first
        cached = cls._get_from_cache(target_date)
        if cached:
            return cached
        
        # Fetch from API
        readings = cls._fetch_from_api(target_date)
        if readings:
            cls._save_to_cache(target_date, readings)
            return readings
        
        # Fallback
        return cls._get_fallback(target_date)
    
    @classmethod
    def _fetch_from_api(cls, target_date: date) -> Optional[MassReadings]:
        """Fetch readings from Catholic Readings API"""
        try:
            # Format: /api/v1/readings/2026/02/13
            url = f"{cls.PRIMARY_API}/api/v1/readings/{target_date.year}/{target_date.month:02d}/{target_date.day:02d}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse response
            return cls._parse_api_response(data, target_date)
            
        except requests.RequestException as e:
            print(f"Mass Readings API error: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"Mass Readings parsing error: {e}")
            return None
    
    @classmethod
    def _parse_api_response(cls, data: Dict, target_date: date) -> MassReadings:
        """Parse API response into MassReadings object"""
        
        # Extract readings
        first = data.get("first_reading", {})
        psalm = data.get("responsorial_psalm", {})
        second = data.get("second_reading")
        gospel = data.get("gospel", {})
        
        return MassReadings(
            date=target_date,
            liturgical_day=data.get("liturgical_day", ""),
            first_reading=Reading(
                type="first_reading",
                citation=first.get("citation", ""),
                text=first.get("text", "")
            ),
            responsorial_psalm=Reading(
                type="psalm",
                citation=psalm.get("citation", ""),
                text=psalm.get("text", "")
            ),
            second_reading=Reading(
                type="second_reading",
                citation=second.get("citation", ""),
                text=second.get("text", "")
            ) if second else None,
            gospel_acclamation=data.get("gospel_acclamation", "Alleluia"),
            gospel=Reading(
                type="gospel",
                citation=gospel.get("citation", ""),
                text=gospel.get("text", "")
            ),
            season=data.get("season", "ordinary"),
            color=data.get("color", "green")
        )
    
    @classmethod
    def _get_from_cache(cls, target_date: date) -> Optional[MassReadings]:
        """Retrieve readings from local cache"""
        try:
            cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_file = cls.CACHE_DIR / f"{target_date.isoformat()}.json"
            
            if cache_file.exists():
                # Check if cache is less than 30 days old
                cache_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
                if cache_age.days < 30:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        return cls._parse_api_response(data, target_date)
            
            return None
        except Exception as e:
            print(f"Cache read error: {e}")
            return None
    
    @classmethod
    def _save_to_cache(cls, target_date: date, readings: MassReadings):
        """Save readings to local cache for offline access"""
        try:
            cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_file = cls.CACHE_DIR / f"{target_date.isoformat()}.json"
            
            # Convert to dict
            data = {
                "liturgical_day": readings.liturgical_day,
                "first_reading": {
                    "citation": readings.first_reading.citation,
                    "text": readings.first_reading.text
                },
                "responsorial_psalm": {
                    "citation": readings.responsorial_psalm.citation,
                    "text": readings.responsorial_psalm.text
                },
                "gospel_acclamation": readings.gospel_acclamation,
                "gospel": {
                    "citation": readings.gospel.citation,
                    "text": readings.gospel.text
                },
                "season": readings.season,
                "color": readings.color
            }
            
            if readings.second_reading:
                data["second_reading"] = {
                    "citation": readings.second_reading.citation,
                    "text": readings.second_reading.text
                }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Cache write error: {e}")
    
    @classmethod
    def _get_fallback(cls, target_date: date) -> MassReadings:
        """
        Fallback readings when API unavailable
        
        Provides generic readings based on liturgical season estimation.
        """
        # Simple season detection (approximate)
        month, day = target_date.month, target_date.day
        
        if month == 12 and day >= 25:
            season, color = "christmas", "white"
        elif month == 1 and day <= 10:
            season, color = "christmas", "white"
        elif month == 12 and day < 25:
            season, color = "advent", "purple"
        elif month in [2, 3]:
            season, color = "lent", "purple"
        elif month in [4, 5]:
            season, color = "easter", "white"
        else:
            season, color = "ordinary", "green"
        
        return MassReadings(
            date=target_date,
            liturgical_day=f"{season.capitalize()} Time",
            first_reading=Reading(
                type="first_reading",
                citation="",
                text="[Readings unavailable - please check internet connection]"
            ),
            responsorial_psalm=Reading(
                type="psalm",
                citation="",
                text="[Psalm unavailable - please check internet connection]"
            ),
            second_reading=None,
            gospel_acclamation="Alleluia",
            gospel=Reading(
                type="gospel",
                citation="",
                text="[Gospel unavailable - please check internet connection]"
            ),
            season=season,
            color=color
        )
    
    @classmethod
    def format_for_bulletin(cls, readings: MassReadings) -> str:
        """Format readings for parish bulletin"""
        bulletin = f"""
**{readings.liturgical_day}**
{readings.date.strftime('%A, %B %d, %Y')}

**First Reading:** {readings.first_reading.citation}
**Responsorial Psalm:** {readings.responsorial_psalm.citation}
"""
        
        if readings.second_reading:
            bulletin += f"**Second Reading:** {readings.second_reading.citation}\n"
        
        bulletin += f"""**Gospel Acclamation:** {readings.gospel_acclamation}
**Gospel:** {readings.gospel.citation}
"""
        
        return bulletin
    
    @classmethod
    def get_gospel_text(cls, readings: MassReadings) -> str:
        """Extract just the Gospel text for reflection"""
        return f"""
**{readings.gospel.citation}**

{readings.gospel.text}
"""


# Demo usage
if __name__ == "__main__":
    readings = MassReadingsAPI.get_today()
    if readings:
        print(MassReadingsAPI.format_for_bulletin(readings))
        print("\n" + "="*70 + "\n")
        print(MassReadingsAPI.get_gospel_text(readings))
