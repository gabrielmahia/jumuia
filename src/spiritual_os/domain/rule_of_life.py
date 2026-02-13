"""
Rule of Life Module - Personal spiritual practice builder
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import time


@dataclass
class RuleEntry:
    """Single practice in a Rule of Life"""
    name: str
    category: str  # prayer, scripture, examen, virtue, fasting, mercy
    duration_minutes: int
    frequency: str  # daily, weekly, seasonal
    time_of_day: Optional[str] = None  # morning, midday, evening
    notes: str = ""


@dataclass
class RuleOfLife:
    """Personal Rule of Life - daily/weekly spiritual practice"""
    user_id: str
    title: str = "My Rule of Life"
    entries: List[RuleEntry] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    
    def add_entry(self, entry: RuleEntry):
        """Add practice to rule"""
        self.entries.append(entry)
    
    def daily_practices(self) -> List[RuleEntry]:
        """Get all daily practices"""
        return [e for e in self.entries if e.frequency == "daily"]
    
    def weekly_practices(self) -> List[RuleEntry]:
        """Get all weekly practices"""
        return [e for e in self.entries if e.frequency == "weekly"]
    
    def by_category(self, category: str) -> List[RuleEntry]:
        """Get practices by category"""
        return [e for e in self.entries if e.category == category]
    
    def total_daily_minutes(self) -> int:
        """Calculate total daily commitment"""
        return sum(e.duration_minutes for e in self.daily_practices())
    
    def to_dict(self) -> dict:
        """Serialize to dict for storage"""
        return {
            "user_id": self.user_id,
            "title": self.title,
            "entries": [
                {
                    "name": e.name,
                    "category": e.category,
                    "duration_minutes": e.duration_minutes,
                    "frequency": e.frequency,
                    "time_of_day": e.time_of_day,
                    "notes": e.notes
                }
                for e in self.entries
            ],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


def generate_rule_template() -> RuleOfLife:
    """Generate a suggested Rule of Life template"""
    rule = RuleOfLife(user_id="default")
    
    # Morning prayer
    rule.add_entry(RuleEntry(
        name="Morning Prayer",
        category="prayer",
        duration_minutes=15,
        frequency="daily",
        time_of_day="morning",
        notes="Begins the day with intention"
    ))
    
    # Scripture reading
    rule.add_entry(RuleEntry(
        name="Scripture (Lectio Divina)",
        category="scripture",
        duration_minutes=20,
        frequency="daily",
        time_of_day="morning",
        notes="Slow reading + reflection"
    ))
    
    # Examen
    rule.add_entry(RuleEntry(
        name="Evening Examen",
        category="examen",
        duration_minutes=10,
        frequency="daily",
        time_of_day="evening",
        notes="Review day: grace noticed, sin confessed"
    ))
    
    # Virtue practice
    rule.add_entry(RuleEntry(
        name="Virtue Practice",
        category="virtue",
        duration_minutes=5,
        frequency="daily",
        notes="Focus on one virtue weekly (humility, charity, justice)"
    ))
    
    # Works of mercy
    rule.add_entry(RuleEntry(
        name="Work of Mercy",
        category="mercy",
        duration_minutes=30,
        frequency="weekly",
        notes="Corporal or spiritual mercy"
    ))
    
    # Fasting/abstinence
    rule.add_entry(RuleEntry(
        name="Fasting/Abstinence",
        category="fasting",
        duration_minutes=0,
        frequency="weekly",
        notes="Friday or season-appropriate"
    ))
    
    return rule
