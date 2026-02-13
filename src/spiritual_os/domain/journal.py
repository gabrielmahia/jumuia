"""
Journaling Module - Spiritual reflection templates and journal entries
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class JournalEntry:
    """A spiritual journal entry"""
    date: str  # ISO format
    template_type: str  # examen, lectio_divina, hardening_healing, fatigue_warning
    title: str = ""
    content: str = ""
    reflection: str = ""
    insights: List[str] = field(default_factory=list)
    prayer: str = ""
    
    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "template_type": self.template_type,
            "title": self.title,
            "content": self.content,
            "reflection": self.reflection,
            "insights": self.insights,
            "prayer": self.prayer
        }


class JournalTemplate:
    """Guided reflection templates"""
    
    @staticmethod
    def examen_template() -> dict:
        """Ignatian Examen - review of day with God"""
        return {
            "name": "Evening Examen",
            "type": "examen_divina",
            "prompts": [
                "1. Presence: How was God present in my day?",
                "2. Review: What moments brought consolation? Desolation?",
                "3. Gratitude: What am I most grateful for today?",
                "4. Sorrow: Where did I fall short of love?",
                "5. Forward: What will I ask God's help for tomorrow?"
            ],
            "time_minutes": 10
        }
    
    @staticmethod
    def lectio_divina_template() -> dict:
        """Lectio Divina - sacred reading"""
        return {
            "name": "Lectio Divina",
            "type": "lectio_divina",
            "prompts": [
                "Lectio (Read): Read passage slowly. What word catches your attention?",
                "Meditatio (Meditate): What is God saying to you through this word?",
                "Oratio (Respond): How do you respond in prayer?",
                "Contemplatio (Contemplate): Rest in God's presence and love."
            ],
            "time_minutes": 20
        }
    
    @staticmethod
    def hardening_healing_template() -> dict:
        """Exploring hardness of heart vs. healing"""
        return {
            "name": "Hardening vs. Healing",
            "type": "hardening_healing",
            "prompts": [
                "Where is my heart hardened? (unforgiveness, bitterness, doubt)",
                "How did this hardening begin?",
                "What would healing look like?",
                "What courage do I need from God?",
                "One step toward healing this week?"
            ],
            "time_minutes": 15
        }
    
    @staticmethod
    def fatigue_warning_template() -> dict:
        """Warning signs of spiritual fatigue"""
        return {
            "name": "Fatigue & Warning Signs",
            "type": "fatigue_warning",
            "prompts": [
                "Do I feel distant from God? How?",
                "Am I experiencing spiritual dryness?",
                "Have I neglected prayer/Scripture/community?",
                "Am I running on willpower instead of grace?",
                "What 'pit' might I be sliding into?",
                "What is one way to return to God today?"
            ],
            "time_minutes": 10
        }


@dataclass
class Journal:
    """Personal spiritual journal"""
    user_id: str
    entries: List[JournalEntry] = field(default_factory=list)
    
    def add_entry(self, entry: JournalEntry):
        """Add a journal entry"""
        self.entries.append(entry)
    
    def entries_by_type(self, template_type: str) -> List[JournalEntry]:
        """Get entries by template type"""
        return [e for e in self.entries if e.template_type == template_type]
    
    def recent_entries(self, days: int = 30) -> List[JournalEntry]:
        """Get recent entries"""
        # Simplified: would filter by date in real implementation
        return self.entries[-days:]
    
    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "entries": [e.to_dict() for e in self.entries]
        }
