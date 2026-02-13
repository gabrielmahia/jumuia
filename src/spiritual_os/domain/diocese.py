"""
Diocese Module - Diocese-level governance and coordination (Layer B)
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DioceseStats:
    """Aggregate statistics (NO personal data)"""
    total_parishes: int = 0
    total_catholics: int = 0
    weekly_attendance: int = 0
    priests_count: int = 0
    deacons_count: int = 0


@dataclass
class Diocese:
    """Diocese entity for coordination"""
    name: str
    region: str
    bishop_name: str = ""
    contact_email: str = ""
    website: str = ""
    
    # Aggregate data only
    stats: DioceseStats = field(default_factory=DioceseStats)
    
    # Governance
    parishes: List[str] = field(default_factory=list)  # parish names
    justice_priorities: List[str] = field(default_factory=list)
    formation_initiatives: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "region": self.region,
            "bishop_name": self.bishop_name,
            "contact_email": self.contact_email,
            "website": self.website,
            "parishes_count": len(self.parishes),
            "justice_priorities": self.justice_priorities,
            "formation_initiatives": self.formation_initiatives,
            "stats": {
                "total_parishes": self.stats.total_parishes,
                "total_catholics": self.stats.total_catholics,
                "weekly_attendance": self.stats.weekly_attendance,
                "priests": self.stats.priests_count,
                "deacons": self.stats.deacons_count
            }
        }


@dataclass
class DioceseDirectory:
    """Diocese-wide directory and coordination"""
    dioceses: List[Diocese] = field(default_factory=list)
    
    def add_diocese(self, diocese: Diocese):
        """Register a diocese"""
        self.dioceses.append(diocese)
    
    def find_diocese(self, name: str) -> Optional[Diocese]:
        """Lookup diocese by name"""
        for d in self.dioceses:
            if d.name.lower() == name.lower():
                return d
        return None
    
    def parishes_by_diocese(self, diocese_name: str) -> List[str]:
        """Get parishes in a diocese"""
        diocese = self.find_diocese(diocese_name)
        return diocese.parishes if diocese else []
