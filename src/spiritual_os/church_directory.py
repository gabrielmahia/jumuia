"""
Global Church Directory

Find Catholic churches anywhere in the world.

Solves the "Bhutan Problem": How do you find the 7 Catholic parishes
in a country with 0.1% Catholic population and no online presence?

Data sources:
- GCatholic.org (comprehensive global directory)
- User submissions (crowdsourced)
- Diocesan registrations
- Parish self-registration

Coverage goal: 200+ countries, 100,000+ parishes
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum
from datetime import time


class MassLanguage(Enum):
    """Common Mass languages"""
    ENGLISH = "English"
    SPANISH = "Spanish"
    LATIN = "Latin"
    SWAHILI = "Swahili"
    FRENCH = "French"
    PORTUGUESE = "Portuguese"
    ITALIAN = "Italian"
    GERMAN = "German"
    POLISH = "Polish"
    TAGALOG = "Tagalog"
    ARABIC = "Arabic"
    HINDI = "Hindi"
    CHINESE = "Chinese"
    VIETNAMESE = "Vietnamese"
    OTHER = "Other"


class ChurchType(Enum):
    """Type of Catholic church"""
    PARISH = "Parish"
    CATHEDRAL = "Cathedral"
    BASILICA = "Basilica"
    SHRINE = "Shrine"
    CHAPEL = "Chapel"
    MISSION = "Mission Station"
    MONASTERY = "Monastery"
    CONVENT = "Convent"


class WelcomeLevel(Enum):
    """How welcoming is the parish?"""
    VERY_WELCOMING = "Very Welcoming"
    WELCOMING = "Welcoming"
    FORMAL = "Formal"
    TRADITIONAL = "Traditional"
    UNKNOWN = "Unknown"


@dataclass
class MassSchedule:
    """Mass times for a parish"""
    sunday_times: List[str]  # ["7:00 AM", "9:00 AM", "11:00 AM", "5:00 PM"]
    weekday_times: List[str]  # ["6:30 AM", "12:10 PM"]
    saturday_vigil: Optional[str]  # "5:30 PM"
    holy_days: Optional[str]  # "As announced"
    confession_times: List[str]  # ["Saturday 4:00-5:00 PM", "By appointment"]
    adoration_times: Optional[str]  # "First Friday 7:00 PM - Saturday 7:00 AM"


@dataclass
class ChurchContact:
    """Contact information for a church"""
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    facebook: Optional[str]
    whatsapp: Optional[str]  # Important for Africa/Asia


@dataclass
class Church:
    """
    Individual Catholic church/parish
    
    Comprehensive data model for global church directory.
    """
    # Identification
    id: str
    name: str
    type: ChurchType
    
    # Location
    country: str
    region: Optional[str]  # State/Province
    city: str
    address: str
    latitude: float
    longitude: float
    
    # Diocese
    diocese: str
    archdiocese: Optional[str]
    bishop: Optional[str]
    
    # Parish Leadership
    pastor: Optional[str]
    associate_pastors: List[str]
    deacons: List[str]
    
    # Mass & Services
    mass_schedule: MassSchedule
    mass_languages: List[MassLanguage]
    
    # Community
    registered_families: Optional[int]
    average_sunday_attendance: Optional[int]
    ethnic_communities: List[str]  # ["Filipino", "Nigerian", "Mexican"]
    special_ministries: List[str]  # ["Young adults", "Grief support", "RCIA"]
    
    # Welcome & Accessibility
    welcome_level: WelcomeLevel
    lgbtq_welcoming: Optional[bool]
    wheelchair_accessible: bool
    parking_available: bool
    nursery_available: bool
    
    # Contact
    contact: ChurchContact
    
    # Metadata
    established_year: Optional[int]
    architectural_style: Optional[str]
    patron_saint: Optional[str]
    notes: Optional[str]
    last_updated: str
    verified: bool  # Has parish confirmed this info?


# ============================================================================
# DEMO DATA - GLOBAL COVERAGE
# ============================================================================

# Example: Bhutan (7 parishes, all under Darjeeling Diocese, India)
BHUTAN_CHURCHES = [
    Church(
        id="church_bhutan_001",
        name="St. Mary's Church",
        type=ChurchType.PARISH,
        country="Bhutan",
        region="Thimphu District",
        city="Thimphu",
        address="Chang Lam, near Clock Tower Square",
        latitude=27.4712,
        longitude=89.6339,
        diocese="Darjeeling",
        archdiocese=None,
        bishop="Bishop Stephen Lepcha",
        pastor="Fr. Benedict D'Souza",
        associate_pastors=[],
        deacons=[],
        mass_schedule=MassSchedule(
            sunday_times=["10:00 AM"],
            weekday_times=[],
            saturday_vigil=None,
            holy_days="As announced",
            confession_times=["By appointment"],
            adoration_times=None
        ),
        mass_languages=[MassLanguage.ENGLISH, MassLanguage.HINDI],
        registered_families=30,
        average_sunday_attendance=100,
        ethnic_communities=["Indian expats", "Bhutanese converts", "Filipino workers"],
        special_ministries=["Catechism for children"],
        welcome_level=WelcomeLevel.VERY_WELCOMING,
        lgbtq_welcoming=None,
        wheelchair_accessible=False,
        parking_available=False,
        nursery_available=False,
        contact=ChurchContact(
            phone="+975-2-322-743",
            email="stmarysthimphu@gmail.com",
            website=None,
            facebook=None,
            whatsapp="+975-77-123456"
        ),
        established_year=1985,
        architectural_style="Simple modern",
        patron_saint="Our Lady of Perpetual Help",
        notes="Small but vibrant community. Visitors always welcome. Contact priest in advance if possible.",
        last_updated="2026-02-13",
        verified=False
    )
]

# Example: Kenya - Consolata Shrine (from earlier context)
KENYA_CHURCHES = [
    Church(
        id="church_kenya_001",
        name="Consolata Shrine",
        type=ChurchType.SHRINE,
        country="Kenya",
        region="Nairobi County",
        city="Nairobi",
        address="Westlands, along Waiyaki Way",
        latitude=-1.2667,
        longitude=36.8000,
        diocese="Archdiocese of Nairobi",
        archdiocese="Nairobi",
        bishop="Archbishop Philip Anyolo",
        pastor="Fr. James Odhiambo",
        associate_pastors=["Fr. Peter Kamau", "Fr. David Mwangi"],
        deacons=["Deacon John Karanja"],
        mass_schedule=MassSchedule(
            sunday_times=["6:30 AM", "8:00 AM", "10:00 AM", "12:00 PM", "5:30 PM"],
            weekday_times=["6:30 AM", "12:10 PM", "5:30 PM"],
            saturday_vigil="5:30 PM",
            holy_days="As announced",
            confession_times=["Saturday 4:00-5:00 PM", "Daily after Mass"],
            adoration_times="24/7 Perpetual Adoration Chapel"
        ),
        mass_languages=[MassLanguage.ENGLISH, MassLanguage.SWAHILI],
        registered_families=2500,
        average_sunday_attendance=3500,
        ethnic_communities=["Kikuyu", "Luo", "Luhya", "International"],
        special_ministries=[
            "Small Christian Communities (45 SCCs)",
            "Youth Ministry",
            "Consolata Missionaries",
            "Shrine bookstore",
            "Counseling center"
        ],
        welcome_level=WelcomeLevel.VERY_WELCOMING,
        lgbtq_welcoming=None,
        wheelchair_accessible=True,
        parking_available=True,
        nursery_available=True,
        contact=ChurchContact(
            phone="+254-20-444-7479",
            email="info@consolatashrine.org",
            website="https://consolatashrine.org",
            facebook="ConsolataShrineNairobi",
            whatsapp="+254-722-123456"
        ),
        established_year=1955,
        architectural_style="Modernist with African motifs",
        patron_saint="Our Lady Consolata",
        notes="Major pilgrimage site in East Africa. Very active SCCs. Bookstore with Catholic literature.",
        last_updated="2026-02-13",
        verified=True
    )
]

# Demo church database
DEMO_CHURCHES = BHUTAN_CHURCHES + KENYA_CHURCHES


class ChurchDirectory:
    """
    Global church directory with search
    """
    
    @staticmethod
    def search_by_location(country: str, city: Optional[str] = None) -> List[Church]:
        """Find churches by location"""
        results = [c for c in DEMO_CHURCHES if c.country.lower() == country.lower()]
        
        if city:
            results = [c for c in results if c.city.lower() == city.lower()]
        
        return results
    
    @staticmethod
    def search_by_coordinates(lat: float, lon: float, radius_km: float = 50) -> List[Church]:
        """Find churches near coordinates (simplified)"""
        # Simplified distance calculation (would use proper geospatial in production)
        results = []
        for church in DEMO_CHURCHES:
            # Rough approximation: 1 degree ≈ 111 km
            lat_diff = abs(church.latitude - lat)
            lon_diff = abs(church.longitude - lon)
            distance = ((lat_diff ** 2) + (lon_diff ** 2)) ** 0.5 * 111
            
            if distance <= radius_km:
                results.append(church)
        
        return results
    
    @staticmethod
    def search_by_language(language: MassLanguage) -> List[Church]:
        """Find churches offering Mass in specific language"""
        return [c for c in DEMO_CHURCHES if language in c.mass_languages]
    
    @staticmethod
    def search_by_name(query: str) -> List[Church]:
        """Search churches by name"""
        query_lower = query.lower()
        return [c for c in DEMO_CHURCHES if query_lower in c.name.lower()]
