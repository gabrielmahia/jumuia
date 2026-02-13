"""
Catechist Certification Tracking

Manages certification for lay catechists who teach faith formation in parishes.

Certification levels (typical diocesan structure):
- Basic Certification: Required within first 2 years (48-90 hours)
- Master Certification: For experienced catechists, DREs, principals
- Specialized Certification: High school, special needs, RCIA, etc.

Renewal requirements: Every 3-4 years with continuing formation hours
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, date
from enum import Enum


class CertificationLevel(Enum):
    """Catechist certification tiers"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    MASTER = "master"
    SPECIALIZED = "specialized"


class CertificationStatus(Enum):
    """Current status of certification"""
    IN_PROGRESS = "in_progress"
    ACTIVE = "active"
    RENEWAL_DUE = "renewal_due"
    EXPIRED = "expired"
    SUSPENDED = "suspended"


class CourseCategory(Enum):
    """Required course categories for certification"""
    SACRED_SCRIPTURE = "sacred_scripture"
    DOCTRINE = "doctrine"
    LITURGY_SACRAMENTS = "liturgy_sacraments"
    MORAL_TEACHING = "moral_teaching"
    SOCIAL_TEACHING = "social_teaching"
    CATECHETICAL_METHODS = "catechetical_methods"
    CHILD_DEVELOPMENT = "child_development"
    SPIRITUAL_FORMATION = "spiritual_formation"


@dataclass
class CatechistCourse:
    """Individual course or formation event"""
    id: str
    title: str
    category: CourseCategory
    provider: str  # "Franciscan University", "Diocesan Office", "Catholic Distance University"
    date_completed: datetime
    hours: float
    instructor: Optional[str]
    certificate_number: Optional[str]
    notes: Optional[str]


@dataclass
class ObservationRecord:
    """Classroom observation by Master Catechist or DRE"""
    id: str
    observer_name: str
    observer_role: str  # "Master Catechist", "DRE", "Pastor"
    observation_date: datetime
    class_observed: str  # e.g., "Grade 3 Sacramental Prep"
    strengths_noted: List[str]
    areas_for_growth: List[str]
    overall_rating: str  # "Excellent", "Good", "Needs Improvement"
    recommendations: str
    hours_credited: float


@dataclass
class CatechistCertification:
    """
    Complete certification record for a catechist
    
    Tracks courses, observations, background checks, and renewal status.
    """
    # Personal info
    catechist_id: str
    name: str
    email: str
    phone: str
    parish_id: str
    diocese_id: str
    
    # Certification status
    level: CertificationLevel
    status: CertificationStatus
    current_certificate_number: Optional[str]
    issue_date: Optional[datetime]
    expiration_date: Optional[datetime]
    
    # Formation tracking
    courses_completed: List[CatechistCourse]
    total_formation_hours: float
    spiritual_formation_hours: float  # Separate requirement
    observations_completed: List[ObservationRecord]
    
    # Requirements
    basic_requirements_met: bool
    background_check_date: Optional[datetime]
    background_check_status: str  # "Passed", "Pending", "Failed"
    safe_environment_training_date: Optional[datetime]
    mandated_reporter_training_date: Optional[datetime]
    
    # Renewal
    renewal_hours_required: float  # e.g., 30 hours per 3-year cycle
    renewal_hours_completed: float
    next_renewal_date: Optional[datetime]
    
    # Ministry assignment
    current_assignments: List[str]  # e.g., ["Grade 2 Faith Formation", "RCIA Team"]
    years_serving: float
    
    # Diocesan coordination
    diocese_registration_date: Optional[datetime]
    diocese_approved_by: Optional[str]
    
    # Notes
    specializations: List[str]  # e.g., ["Catechesis of Good Shepherd", "Special Needs"]
    languages_taught: List[str]
    notes: Optional[str]


@dataclass
class CertificationRequirements:
    """
    Diocesan certification requirements structure
    
    Defines what catechists must complete for each level.
    """
    level: CertificationLevel
    total_hours_required: float
    
    # Course requirements by category
    scripture_hours: float
    doctrine_hours: float
    liturgy_hours: float
    moral_teaching_hours: float
    social_teaching_hours: float
    methods_hours: float
    
    # Practical requirements
    observation_hours_required: float
    observation_count_required: int
    spiritual_formation_hours: float
    
    # Safety requirements
    background_check_required: bool
    safe_environment_training_required: bool
    mandated_reporter_training_required: bool
    
    # Renewal
    renewal_cycle_years: int
    renewal_hours_per_cycle: float


# Basic Certification Requirements (typical diocesan standard)
BASIC_CERT_REQUIREMENTS = CertificationRequirements(
    level=CertificationLevel.BASIC,
    total_hours_required=48.0,
    scripture_hours=8.0,
    doctrine_hours=8.0,
    liturgy_hours=6.0,
    moral_teaching_hours=4.0,
    social_teaching_hours=4.0,
    methods_hours=8.0,
    observation_hours_required=6.0,
    observation_count_required=2,
    spiritual_formation_hours=8.0,
    background_check_required=True,
    safe_environment_training_required=True,
    mandated_reporter_training_required=True,
    renewal_cycle_years=3,
    renewal_hours_per_cycle=30.0
)

# Master Certification Requirements
MASTER_CERT_REQUIREMENTS = CertificationRequirements(
    level=CertificationLevel.MASTER,
    total_hours_required=120.0,
    scripture_hours=20.0,
    doctrine_hours=20.0,
    liturgy_hours=15.0,
    moral_teaching_hours=10.0,
    social_teaching_hours=10.0,
    methods_hours=20.0,
    observation_hours_required=15.0,
    observation_count_required=5,
    spiritual_formation_hours=20.0,
    background_check_required=True,
    safe_environment_training_required=True,
    mandated_reporter_training_required=True,
    renewal_cycle_years=4,
    renewal_hours_per_cycle=20.0
)


# Demo data
DEMO_CATECHIST = CatechistCertification(
    catechist_id="cat_001",
    name="Sarah Muthoni",
    email="sarah.m@example.com",
    phone="+254-722-345678",
    parish_id="parish_001",
    diocese_id="diocese_001",
    level=CertificationLevel.BASIC,
    status=CertificationStatus.ACTIVE,
    current_certificate_number="NAI-2024-0156",
    issue_date=datetime(2024, 1, 15),
    expiration_date=datetime(2027, 1, 15),
    courses_completed=[
        CatechistCourse(
            id="course_001",
            title="Introduction to Sacred Scripture",
            category=CourseCategory.SACRED_SCRIPTURE,
            provider="Archdiocese of Nairobi",
            date_completed=datetime(2023, 6, 15),
            hours=8.0,
            instructor="Fr. Peter Kamau",
            certificate_number="SCR-2023-089",
            notes="Excellent participation"
        ),
        CatechistCourse(
            id="course_002",
            title="Catholic Doctrine Fundamentals",
            category=CourseCategory.DOCTRINE,
            provider="Archdiocese of Nairobi",
            date_completed=datetime(2023, 8, 20),
            hours=8.0,
            instructor="Sr. Mary Wanjiku",
            certificate_number="DOC-2023-102",
            notes=None
        )
    ],
    total_formation_hours=52.0,
    spiritual_formation_hours=10.0,
    observations_completed=[
        ObservationRecord(
            id="obs_001",
            observer_name="Margaret Njeri (Master Catechist)",
            observer_role="Master Catechist",
            observation_date=datetime(2023, 10, 5),
            class_observed="Grade 3 First Communion Prep",
            strengths_noted=[
                "Excellent rapport with children",
                "Clear explanations",
                "Good use of visual aids"
            ],
            areas_for_growth=[
                "Classroom management during transitions",
                "More frequent checks for understanding"
            ],
            overall_rating="Good",
            recommendations="Continue developing skills, ready for certification",
            hours_credited=3.0
        )
    ],
    basic_requirements_met=True,
    background_check_date=datetime(2023, 5, 1),
    background_check_status="Passed",
    safe_environment_training_date=datetime(2023, 5, 15),
    mandated_reporter_training_date=datetime(2023, 5, 15),
    renewal_hours_required=30.0,
    renewal_hours_completed=4.0,
    next_renewal_date=datetime(2027, 1, 15),
    current_assignments=[
        "Grade 2 Faith Formation (Sundays 9-10am)",
        "First Communion Preparation"
    ],
    years_serving=3.5,
    diocese_registration_date=datetime(2024, 1, 20),
    diocese_approved_by="Fr. John Omondi, Vicar for Clergy",
    specializations=["Sacramental Preparation"],
    languages_taught=["English", "Swahili"],
    notes="Very dedicated, excellent with young children"
)
