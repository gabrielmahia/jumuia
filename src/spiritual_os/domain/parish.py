"""
Parish Module - Parish-facing utilities and coordination (Layer A)
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ParishEvent:
    """Parish event or announcement"""
    name: str
    date: str  # ISO format
    time: str
    location: str
    description: str = ""
    ministry: str = ""  # sacrament, formation, justice, community


@dataclass
class ParishBulletin:
    """Parish bulletin - announcements and schedule"""
    name: str
    date: str
    announcements: List[str] = field(default_factory=list)
    events: List[ParishEvent] = field(default_factory=list)
    mass_schedule: dict = field(default_factory=dict)  # day -> times
    
    def add_announcement(self, text: str):
        """Add announcement"""
        self.announcements.append(text)
    
    def add_event(self, event: ParishEvent):
        """Add event"""
        self.events.append(event)


@dataclass
class Parish:
    """Parish entity for coordination"""
    name: str
    diocese: str
    address: str = ""
    phone: str = ""
    email: str = ""
    website: str = ""
    
    # Utilities
    bulletin: Optional[ParishBulletin] = None
    
    # Transparency (aggregated, no personal data)
    active_members_count: int = 0
    weekly_attendance: int = 0
    justice_initiatives: List[str] = field(default_factory=list)
    
    def set_bulletin(self, bulletin: ParishBulletin):
        """Load parish bulletin from CSV/JSON"""
        self.bulletin = bulletin
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "diocese": self.diocese,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "active_members_count": self.active_members_count,
            "weekly_attendance": self.weekly_attendance,
            "justice_initiatives": self.justice_initiatives
        }


def parse_bulletin_markdown(markdown_text: str) -> ParishBulletin:
    """Parse parish bulletin from markdown"""
    # Simplified: real implementation would parse MD structure
    bulletin = ParishBulletin(
        name="Parish Bulletin",
        date=""
    )
    return bulletin
