"""
Sacraments Module - Sacramental milestones and formation tracker
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class SacramentalMilestone:
    """Record of a sacramental moment or preparation"""
    name: str  # Baptism, Confirmation, First Eucharist, Marriage Prep, RCIA, etc.
    category: str  # initiation, reconciliation, eucharist, orders, marriage, healing
    date_received: Optional[str] = None  # ISO format or blank if not yet
    location: str = ""
    minister: str = ""
    notes: str = ""
    preparation_started: Optional[str] = None
    preparation_completed: Optional[str] = None
    
    def is_received(self) -> bool:
        """Has this sacrament been received?"""
        return self.date_received is not None
    
    def is_preparing(self) -> bool:
        """Currently in preparation?"""
        return self.preparation_started and not self.preparation_completed


@dataclass
class SacramentTracker:
    """Personal record of sacramental life"""
    user_id: str
    milestones: List[SacramentalMilestone] = None
    
    def __post_init__(self):
        if self.milestones is None:
            self.milestones = []
    
    def add_milestone(self, milestone: SacramentalMilestone):
        """Record a sacramental milestone"""
        self.milestones.append(milestone)
    
    def get_initiated(self) -> List[SacramentalMilestone]:
        """Sacraments of initiation (baptism, confirmation, eucharist)"""
        return [m for m in self.milestones if m.category == "initiation"]
    
    def get_reconciliation(self) -> Optional[SacramentalMilestone]:
        """Reconciliation/Penance"""
        for m in self.milestones:
            if m.category == "reconciliation":
                return m
        return None
    
    def get_marriage_info(self) -> Optional[SacramentalMilestone]:
        """Marriage sacrament"""
        for m in self.milestones:
            if m.category == "marriage":
                return m
        return None
    
    def get_in_progress(self) -> List[SacramentalMilestone]:
        """Sacraments currently being prepared"""
        return [m for m in self.milestones if m.is_preparing()]
    
    def to_dict(self) -> dict:
        """Serialize for storage"""
        return {
            "user_id": self.user_id,
            "milestones": [
                {
                    "name": m.name,
                    "category": m.category,
                    "date_received": m.date_received,
                    "location": m.location,
                    "minister": m.minister,
                    "notes": m.notes,
                    "preparation_started": m.preparation_started,
                    "preparation_completed": m.preparation_completed
                }
                for m in self.milestones
            ]
        }


def default_sacrament_template() -> SacramentTracker:
    """Create a template with common Catholic sacraments"""
    tracker = SacramentTracker(user_id="default")
    
    tracker.add_milestone(SacramentalMilestone(
        name="Baptism",
        category="initiation",
        notes="Entry into Church"
    ))
    
    tracker.add_milestone(SacramentalMilestone(
        name="Confirmation",
        category="initiation",
        notes="Strengthening in Holy Spirit"
    ))
    
    tracker.add_milestone(SacramentalMilestone(
        name="Eucharist",
        category="eucharist",
        notes="Ongoing nourishment"
    ))
    
    tracker.add_milestone(SacramentalMilestone(
        name="Reconciliation",
        category="reconciliation",
        notes="Ongoing healing"
    ))
    
    return tracker
