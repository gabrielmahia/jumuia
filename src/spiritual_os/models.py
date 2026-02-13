"""
Database Models for Nested Catholic Spiritual OS
Single database, multiple permission-based views
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class UserRole(Enum):
    """User roles in the system"""
    INDIVIDUAL = "individual"  # Personal formation only
    PARISH_COORDINATOR = "parish_coordinator"  # Manage parish
    DIOCESAN_LEADER = "diocesan_leader"  # Oversee diocese
    GLOBAL_COORDINATOR = "global_coordinator"  # Coordinate justice globally
    CRISIS_RESPONDER = "crisis_responder"  # Emergency response


@dataclass
class User:
    """Individual user"""
    id: str
    name: str
    email: str
    role: UserRole
    parish_id: Optional[str] = None
    diocese_id: Optional[str] = None
    
    # Permission controls
    opt_in_to_parish_aggregates: bool = False
    opt_in_to_diocese_aggregates: bool = False
    opt_in_to_global_aggregates: bool = False
    privacy_level: int = 0  # 0=only me, 1=spiritual director, 2=parish, etc.
    
    # Personal data (private)
    rule_of_life: Dict[str, Any] = field(default_factory=dict)
    journal_entries: List[Dict[str, Any]] = field(default_factory=list)
    sacrament_milestones: List[Dict[str, Any]] = field(default_factory=list)
    
    created_at: str = ""
    updated_at: str = ""
    
    def to_dict(self, visibility_level: str = "self") -> Dict:
        """Serialize based on visibility level"""
        base = {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "parish_id": self.parish_id,
            "diocese_id": self.diocese_id,
        }
        
        if visibility_level == "self":
            # User sees everything about themselves
            return {**base, **{
                "rule_of_life": self.rule_of_life,
                "journal_entries": self.journal_entries,
                "sacrament_milestones": self.sacrament_milestones,
            }}
        
        # Other roles see nothing (aggregates come from Parish)
        return base


@dataclass
class Parish:
    """Parish entity"""
    id: str
    name: str
    diocese_id: str
    coordinator_id: str
    address: str = ""
    phone: str = ""
    email: str = ""
    
    # Operations
    bulletin_text: str = ""
    events: List[Dict[str, Any]] = field(default_factory=list)
    volunteer_signups: List[Dict[str, Any]] = field(default_factory=list)
    
    # AGGREGATES (computed from members, permission-controlled)
    aggregated_members_count: int = 0
    aggregated_formation_participants: int = 0  # People in Rule of Life
    aggregated_avg_practice_minutes: float = 0.0
    aggregated_sacrament_stats: Dict[str, int] = field(default_factory=dict)
    aggregated_justice_campaigns: List[str] = field(default_factory=list)
    aggregated_volunteer_count: int = 0
    
    created_at: str = ""
    updated_at: str = ""
    
    def to_aggregated_dict(self) -> Dict:
        """Return only aggregated data (no personal info)"""
        return {
            "id": self.id,
            "name": self.name,
            "members_count": self.aggregated_members_count,
            "formation_participants": self.aggregated_formation_participants,
            "avg_practice_minutes": self.aggregated_avg_practice_minutes,
            "sacrament_stats": self.aggregated_sacrament_stats,
            "justice_campaigns": self.aggregated_justice_campaigns,
            "volunteer_count": self.aggregated_volunteer_count,
        }


@dataclass
class Diocese:
    """Diocese entity"""
    id: str
    name: str
    bishop_name: str
    region: str
    
    # Operations
    transparency_priorities: List[str] = field(default_factory=list)
    strategic_plan: str = ""
    
    # AGGREGATES (from parishes)
    aggregated_parishes_count: int = 0
    aggregated_total_catholics: int = 0
    aggregated_weekly_attendance: int = 0
    aggregated_formation_participants: int = 0
    aggregated_justice_campaigns: List[str] = field(default_factory=list)
    aggregated_workers_helped: int = 0
    aggregated_policy_wins: int = 0
    
    created_at: str = ""
    updated_at: str = ""
    
    def to_aggregated_dict(self) -> Dict:
        """Return only aggregated data"""
        return {
            "id": self.id,
            "name": self.name,
            "bishop_name": self.bishop_name,
            "parishes_count": self.aggregated_parishes_count,
            "total_catholics": self.aggregated_total_catholics,
            "weekly_attendance": self.aggregated_weekly_attendance,
            "formation_participants": self.aggregated_formation_participants,
            "justice_campaigns": self.aggregated_justice_campaigns,
            "workers_helped": self.aggregated_workers_helped,
            "policy_wins": self.aggregated_policy_wins,
        }


@dataclass
class JusticeCampaign:
    """Global justice campaign (e.g., living wage)"""
    id: str
    name: str
    campaign_type: str  # "living_wage", "refugee_support", "housing", etc.
    description: str = ""
    
    # Which entities are joined
    dioceses_joined: List[str] = field(default_factory=list)  # Diocese IDs
    parishes_joined_count: int = 0  # Count only, not individual IDs
    
    # Aggregated impact
    aggregated_workers_affected: int = 0
    aggregated_wage_increase_percent: float = 0.0
    aggregated_income_increase_dollars: int = 0
    aggregated_policy_wins: int = 0
    
    # Stories (public testimonials)
    success_stories: List[str] = field(default_factory=list)
    
    created_at: str = ""
    updated_at: str = ""
    
    def to_global_dict(self) -> Dict:
        """Return campaign-level aggregates only"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.campaign_type,
            "dioceses_involved": len(self.dioceses_joined),
            "parishes_involved": self.parishes_joined_count,
            "workers_affected": self.aggregated_workers_affected,
            "wage_increase_percent": self.aggregated_wage_increase_percent,
            "income_increase": self.aggregated_income_increase_dollars,
            "policy_wins": self.aggregated_policy_wins,
            "stories": self.success_stories,
        }


@dataclass
class CrisisEvent:
    """Temporary crisis event (auto-purges after 90 days)"""
    id: str
    name: str
    event_type: str  # "drought", "flood", "earthquake", "conflict", etc.
    location: str
    activated_at: str
    expected_duration_days: int = 180
    
    # Crisis-specific data (temporary)
    affected_dioceses: List[str] = field(default_factory=list)
    activated_parishes: List[str] = field(default_factory=list)
    volunteers: List[Dict[str, Any]] = field(default_factory=list)
    resources: List[Dict[str, Any]] = field(default_factory=list)
    needs: List[Dict[str, Any]] = field(default_factory=list)
    
    # Impact
    people_affected: int = 0
    people_receiving_aid: int = 0
    total_funds_raised: int = 0
    
    # Privacy
    auto_delete_date: str = ""
    
    def to_crisis_dict(self) -> Dict:
        """Return crisis data (temporary, aggregated)"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.event_type,
            "location": self.location,
            "activated_at": self.activated_at,
            "dioceses_affected": len(self.affected_dioceses),
            "parishes_activated": len(self.activated_parishes),
            "volunteers_mobilized": len(self.volunteers),
            "people_affected": self.people_affected,
            "people_receiving_aid": self.people_receiving_aid,
            "funds_raised": self.total_funds_raised,
            "auto_delete_at": self.auto_delete_date,
        }


@dataclass
class PermissionContext:
    """What the current user can see"""
    user_id: str
    role: UserRole
    parish_id: Optional[str] = None
    diocese_id: Optional[str] = None
    
    def can_see_personal_data(self, target_user_id: str) -> bool:
        """Can user see target user's personal data?"""
        return target_user_id == self.user_id  # Only yourself
    
    def can_see_parish_aggregates(self, target_parish_id: str) -> bool:
        """Can user see parish aggregates?"""
        if self.role == UserRole.INDIVIDUAL:
            return self.parish_id == target_parish_id  # Your parish only
        elif self.role == UserRole.PARISH_COORDINATOR:
            return self.parish_id == target_parish_id  # Your parish only
        elif self.role == UserRole.DIOCESAN_LEADER:
            return True  # All parishes in your diocese
        else:
            return True  # Coordinators see everything (aggregated)
    
    def can_see_diocese_aggregates(self, target_diocese_id: str) -> bool:
        """Can user see diocese aggregates?"""
        if self.role in [UserRole.INDIVIDUAL, UserRole.PARISH_COORDINATOR]:
            return False  # No direct access
        elif self.role == UserRole.DIOCESAN_LEADER:
            return self.diocese_id == target_diocese_id  # Your diocese only
        else:
            return True  # Global coordinators see everything
    
    def can_see_global_campaigns(self) -> bool:
        """Can user see global campaigns?"""
        return self.role in [UserRole.DIOCESAN_LEADER, UserRole.GLOBAL_COORDINATOR]
    
    def can_activate_crisis(self) -> bool:
        """Can user activate crisis mode?"""
        return self.role in [UserRole.DIOCESAN_LEADER, UserRole.CRISIS_RESPONDER]
