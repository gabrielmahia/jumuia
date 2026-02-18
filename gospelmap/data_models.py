"""
GospelMap Data Models
All core entities and relationships for the global Catholic ecosystem
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime


class WelcomeLevel(Enum):
    """LGBTQ+ and other welcome indices"""
    ACTIVELY_HOSTILE = 0
    UNWELCOMING = 2
    NEUTRAL = 5
    WELCOMING = 7
    ENTHUSIASTICALLY_AFFIRMING = 9
    LEADERSHIP_AFFIRMING = 10


class TransparencyLevel(Enum):
    """Financial and institutional transparency"""
    COMPLETELY_OPAQUE = 0
    MINIMAL = 2
    SOME_DISCLOSURE = 5
    LARGELY_TRANSPARENT = 7
    FULLY_TRANSPARENT = 10


class JusticeLevel(Enum):
    """Active justice engagement"""
    NONE = 0
    MINIMAL = 2
    MODERATE = 5
    ACTIVE = 7
    RADICAL = 10


@dataclass
class Parish:
    """Individual parish profile"""
    id: str
    name: str
    diocese_id: str
    country: str
    latitude: float
    longitude: float
    founded_year: int
    
    # Accessibility
    languages_spoken: List[str]  # ["Spanish", "English", "Swahili"]
    wheelchair_accessible: bool
    hearing_loop: bool
    nursery_available: bool
    
    # Welcome Indices (0-10)
    lgbtq_welcome: float
    divorced_remarried_welcome: float
    interfaith_welcome: float
    immigrant_refugee_welcome: float
    poor_welcome: float  # Financial accessibility
    women_leadership_pct: float
    youth_engagement_pct: float
    
    # Sacraments
    masses_per_week: int
    confession_hours_per_week: float
    mass_languages: List[str]
    
    # Material Aid (Real-time)
    food_pantry: Optional[Dict] = None  # {"active": True, "families_served": 500, "days_open": ["Mon", "Wed", "Fri"]}
    homeless_shelter: Optional[Dict] = None  # {"beds": 30, "occupancy": 28}
    medical_clinic: Optional[Dict] = None  # {"hours": "Tue-Thu 2pm-6pm", "services": [...]}
    
    # Justice Work (Real-time)
    active_campaigns: List[str] = field(default_factory=list)  # Campaign IDs
    justice_engagement_pct: float = 0  # % of parishioners in justice work
    
    # Financial Transparency
    budget_public: bool = False
    annual_budget: Optional[float] = None
    budget_breakdown: Optional[Dict] = None  # {"pastoral": 45, "admin": 12, "charitable": 43}
    overhead_pct: float = 0
    
    # Community
    active_parishioners: int = 0
    total_parishioners: int = 0
    recent_reviews: List[Dict] = field(default_factory=list)  # {"rating": 8, "text": "...", "date": "2024-01-15"}
    
    # Indices (calculated)
    pastoral_crisis_index: float = 5.0  # 0-10, 10 is crisis
    material_crisis_index: float = 5.0
    justice_alignment_index: float = 5.0
    transparency_index: float = 5.0
    ecosystem_health_score: float = 5.0  # Composite
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Bishop:
    """Bishop profile with accountability tracking"""
    id: str
    name: str
    diocese_id: str
    country: str
    age: int
    ordination_year: int
    
    # Demographics
    nationality: str
    ethnic_background: str
    ordination_age: int
    
    # Accountability
    abuse_allegations_count: int = 0
    abuse_allegations: List[Dict] = field(default_factory=list)  # {"year": 1998, "status": "settled", "victim_support": True}
    cases_transparent: bool = False
    
    # Financial Transparency
    diocese_budget_public: bool = False
    diocese_financial_transparency: float = 5.0  # 0-10
    
    # Leadership Diversity
    women_in_leadership_pct: float = 0
    minority_clergy_pct: float = 0
    actively_lgbtq_inclusive: bool = False
    
    # Synodality
    listening_sessions_held: int = 0
    changes_from_listening: List[str] = field(default_factory=list)
    synodality_score: float = 5.0  # 0-10
    
    # Accountability Score (0-10)
    accountability_score: float = 5.0
    transparency_score: float = 5.0
    
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Diocese:
    """Diocese profile (collection of parishes)"""
    id: str
    name: str
    bishop_id: str
    country: str
    catholic_population: int
    priests_count: int
    priest_vacancies: int
    
    # Transparency
    budget_public: bool = False
    annual_budget: Optional[float] = None
    transparency_score: float = 5.0  # 0-10
    
    # Parishes
    parish_count: int = 0
    parishes: List[str] = field(default_factory=list)  # Parish IDs
    
    # Indices (aggregate)
    avg_parish_welcome: float = 5.0
    avg_parish_transparency: float = 5.0
    avg_parish_justice: float = 5.0
    avg_ecosystem_health: float = 5.0
    
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class JusticeCampaign:
    """Justice campaign (living wage, refugee rights, housing, etc.)"""
    id: str
    name: str
    campaign_type: str  # "living_wage", "refugee_rights", "housing", "climate", etc.
    countries: List[str]
    
    # Impact
    workers_affected: int = 0
    parishes_involved: int = 0
    policy_wins: int = 0
    impact_description: str = ""
    
    # Regional Progress
    regions: Dict[str, Dict] = field(default_factory=dict)  # {
    #     "Kenya-Kiambu": {"status": "WON", "workers": 800, "wage_increase_pct": 25},
    #     "Kenya-Nyeri": {"status": "WON", "workers": 600, "wage_increase_pct": 28},
    #     "Kenya-Murang'a": {"status": "negotiating", "workers": 500, "progress": 0.6}
    # }
    
    # Coordination
    partner_campaigns: List[str] = field(default_factory=list)  # Cross-continent coordination
    coalition_partners: List[str] = field(default_factory=list)  # NGO partners
    
    # Real-time
    status: str = "active"  # "active", "won", "paused", "archived"
    next_actions: List[str] = field(default_factory=list)  # Upcoming events
    
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class DiasporaEthnicity:
    """Diaspora community mapping by ethnicity/language"""
    id: str
    name: str  # "Filipino", "Nigerian", "Korean", etc.
    primary_language: str
    origin_country: str
    
    # Global Distribution
    total_population: int
    countries_present: List[str]
    major_concentrations: Dict[str, int] = field(default_factory=dict)  # {"Philippines": 87000000, "Middle East": 3200000}
    
    # Parishes/Communities
    parishes_with_language: List[str] = field(default_factory=list)  # Parish IDs
    cultural_organizations: List[str] = field(default_factory=list)
    
    # Justice Networks
    specific_justice_campaigns: List[str] = field(default_factory=list)  # e.g., nurse rights for Filipinos
    
    # Integration Support
    support_services: List[str] = field(default_factory=list)  # ["housing", "job_placement", "legal_aid"]
    
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class UserProfile:
    """Individual user profile (private, encrypted)"""
    id: str
    email: str
    
    # Spiritual Journey
    journey_stage: str  # "exploring", "returning", "lifelong", "converting", "questioning"
    
    # Life Context
    languages: List[str]
    is_lgbtq: bool = False
    is_divorced_remarried: bool = False
    is_interfaith: bool = False
    is_refugee_migrant: bool = False
    is_elderly: bool = False
    is_young_parent: bool = False
    is_single: bool = False
    is_economically_marginalized: bool = False
    
    # Values
    values: List[str] = field(default_factory=list)  # ["social_justice", "tradition", "community", "intellectual", "environmental"]
    
    # Preferences
    preferred_liturgy: Optional[str] = None  # "traditional", "progressive", "contemplative"
    
    # Recommended Parishes
    recommended_parishes: List[str] = field(default_factory=list)  # Top 3-5 matching parishes
    
    # Activity
    joined_campaigns: List[str] = field(default_factory=list)
    parishes_visited: List[str] = field(default_factory=list)
    formation_progress: Dict = field(default_factory=dict)
    
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CrisisSignal:
    """Real-time crisis detection and response"""
    id: str
    signal_type: str  # "natural_disaster", "abuse_allegation", "priest_vacancy_crisis", "refugee_surge", etc.
    location: str
    latitude: float
    longitude: float
    severity: float  # 0-10
    
    # Context
    affected_parishes: List[str] = field(default_factory=list)
    affected_population: int = 0
    description: str = ""
    
    # Response
    resources_needed: List[str] = field(default_factory=list)  # ["shelter", "food", "medical", "volunteers"]
    response_status: str = "detected"  # "detected", "coordinating", "responding", "resolved"
    coordinating_parishes: List[str] = field(default_factory=list)
    
    # Real-time Data
    satellite_data: Optional[Dict] = None  # From MODIS, Landsat
    news_mentions: int = 0
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class FormationModule:
    """Spiritual formation pathway"""
    id: str
    title: str
    description: str
    journey_stage: str  # "exploring", "committed", "leader"
    language: str
    
    # Content
    content_type: str  # "video", "article", "book", "class", "retreat"
    duration_hours: float
    difficulty_level: str  # "beginner", "intermediate", "advanced"
    
    # Learning Path
    prerequisites: List[str] = field(default_factory=list)
    next_modules: List[str] = field(default_factory=list)
    
    # Availability
    online_available: bool = True
    in_person_locations: List[str] = field(default_factory=list)
    
    # Justice Integration
    justice_components: List[str] = field(default_factory=list)
    
    created_at: datetime = field(default_factory=datetime.now)


# Summary Stats
@dataclass
class GlobalStats:
    """Global platform statistics"""
    total_parishes: int = 0
    total_dioceses: int = 0
    total_bishops: int = 0
    total_users: int = 0
    total_justice_campaigns: int = 0
    
    # Coverage
    countries_covered: int = 0
    languages_supported: int = 0
    diaspora_communities: int = 0
    
    # Impact
    workers_benefited: int = 0
    policy_wins: int = 0
    refugees_matched: int = 0
    campaigns_coordinated: int = 0
    
    # Health
    avg_ecosystem_health: float = 5.0
    avg_transparency: float = 5.0
    avg_welcome: float = 5.0
    avg_justice_engagement: float = 3.0  # Historically low
    
    updated_at: datetime = field(default_factory=datetime.now)

