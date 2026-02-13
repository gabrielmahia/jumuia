"""
Small Christian Communities (SCCs) Domain Models

SCCs are the foundational pastoral structure for Catholic parishes in Eastern Africa.
Kenya alone has 45,000+ SCCs as the primary way of "being Church" at grassroots level.

Key features:
- Zone/Deanery hierarchical organization
- Meeting schedules and scripture reflection
- Coordinator roles and contact management
- Ministry coordination (prayer, social action, formation)
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime, time
from enum import Enum


class SCCMinistry(Enum):
    """Ministry areas within an SCC"""
    PRAYER = "prayer"
    SOCIAL_ACTION = "social_action"
    FORMATION = "formation"
    EVANGELIZATION = "evangelization"
    YOUTH = "youth"
    FAMILY = "family"


class MeetingFrequency(Enum):
    """How often an SCC meets"""
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


@dataclass
class SCCCoordinator:
    """Leadership of an SCC"""
    name: str
    contact_phone: str
    contact_email: Optional[str]
    role: str  # "Coordinator", "Vice Coordinator", "Secretary", "Treasurer"
    member_since: datetime
    term_start: datetime
    term_end: Optional[datetime]


@dataclass
class SCCMeeting:
    """Record of an SCC meeting"""
    date: datetime
    attendance_count: int
    reflection_passage: str  # Scripture reference
    discussion_summary: Optional[str]
    prayer_requests: List[str]
    action_items: List[str]
    next_meeting_date: datetime


@dataclass
class SmallChristianCommunity:
    """
    Small Christian Community (SCC) / Basic Christian Community (BCC)
    
    The primary pastoral structure for parish life in Eastern Africa.
    Usually 10-20 families meeting regularly for prayer, scripture reflection,
    and social action in their neighborhood.
    """
    # Identification
    id: str
    name: str
    parish_id: str
    zone_id: Optional[str]  # Geographic zone within parish
    deanery_id: Optional[str]  # May belong to multi-parish deanery
    
    # Location
    location_description: str  # e.g., "Westlands, near Sarit Centre"
    meeting_place: str  # e.g., "John's home", "Church hall"
    neighborhood: str
    
    # Membership
    family_count: int
    active_members_count: int
    youth_count: int
    children_count: int
    
    # Leadership
    coordinators: List[SCCCoordinator]
    
    # Meeting schedule
    meeting_frequency: MeetingFrequency
    meeting_day: str  # e.g., "Thursday"
    meeting_time: time
    
    # Activity tracking
    meetings_this_year: int
    last_meeting_date: Optional[datetime]
    upcoming_meeting_date: Optional[datetime]
    
    # Ministry focus areas
    active_ministries: List[SCCMinistry]
    
    # Community characteristics
    language_primary: str  # e.g., "English", "Swahili", "Kikuyu"
    special_focus: Optional[str]  # e.g., "Youth", "Elderly", "Families with young children"
    
    # Contact
    contact_person: str
    contact_phone: str
    
    # Formation
    uses_lumko_method: bool  # Lumko pastoral method popular in Africa
    scripture_reflection_method: str  # e.g., "7-step method", "Lectio Divina"
    
    # Social action
    social_projects: List[str]  # e.g., ["Food bank", "School fees support", "Visiting sick"]
    
    # Metadata
    established_date: datetime
    is_active: bool
    notes: Optional[str]


@dataclass
class Zone:
    """
    Geographic zone grouping several SCCs within a parish
    
    Typical parish structure:
    Parish → 4-8 Zones → 5-10 SCCs per Zone
    """
    id: str
    name: str
    parish_id: str
    coordinator_name: str
    coordinator_contact: str
    scc_count: int
    total_families: int
    geographic_area: str
    established_date: datetime


@dataclass
class SCCReflectionGuide:
    """
    Scripture reflection guide for SCC meetings
    
    Based on Lumko method or similar structured reflection processes
    popular in African SCCs.
    """
    id: str
    date: datetime
    scripture_reference: str
    liturgical_context: str  # Link to liturgical calendar
    
    # 7-step Lumko method
    step_1_welcome: str
    step_2_psalm_hymn: str
    step_3_gospel_reading: str
    step_4_meditation_silence: str
    step_5_sharing_reflection: str
    step_6_action_commitment: str
    step_7_prayer_sending: str
    
    # Additional resources
    questions_for_reflection: List[str]
    connection_to_daily_life: str
    action_suggestions: List[str]


# Sample data for demo
DEMO_SCC = SmallChristianCommunity(
    id="scc_001",
    name="St. Francis SCC",
    parish_id="parish_001",
    zone_id="zone_west",
    deanery_id=None,
    location_description="Westlands, near Sarit Centre",
    meeting_place="Rotating homes",
    neighborhood="Westlands",
    family_count=15,
    active_members_count=28,
    youth_count=12,
    children_count=18,
    coordinators=[
        SCCCoordinator(
            name="Mary Wanjiru",
            contact_phone="+254-722-123456",
            contact_email="mary.w@example.com",
            role="Coordinator",
            member_since=datetime(2018, 3, 15),
            term_start=datetime(2024, 1, 1),
            term_end=datetime(2026, 12, 31)
        )
    ],
    meeting_frequency=MeetingFrequency.WEEKLY,
    meeting_day="Thursday",
    meeting_time=time(19, 0),  # 7:00 PM
    meetings_this_year=42,
    last_meeting_date=datetime(2026, 2, 6),
    upcoming_meeting_date=datetime(2026, 2, 13),
    active_ministries=[
        SCCMinistry.PRAYER,
        SCCMinistry.SOCIAL_ACTION,
        SCCMinistry.FORMATION
    ],
    language_primary="English",
    special_focus="Young families",
    contact_person="Mary Wanjiru",
    contact_phone="+254-722-123456",
    uses_lumko_method=True,
    scripture_reflection_method="7-step Lumko method",
    social_projects=[
        "School fees support for 3 families",
        "Monthly visit to elderly parishioners",
        "Food collection for parish food bank"
    ],
    established_date=datetime(2015, 6, 1),
    is_active=True,
    notes="Very active community, strong youth participation"
)


DEMO_ZONE = Zone(
    id="zone_west",
    name="Western Zone",
    parish_id="parish_001",
    coordinator_name="James Odhiambo",
    coordinator_contact="+254-733-234567",
    scc_count=8,
    total_families=120,
    geographic_area="Westlands, Parklands, Highridge areas",
    established_date=datetime(2010, 1, 1)
)
