"""
GospelMap Sync Module
Integrates Catholic Network Tools with GospelMap global platform

Syncs local parish data → GospelMap for global discovery
Receives opportunities + campaigns from GospelMap
"""

import requests
import json
from typing import Optional, Dict, List
from datetime import datetime
import streamlit as st


class GospelMapSync:
    """
    Syncs Catholic Network Tools ↔ GospelMap
    """
    
    BASE_URL = "https://gospelmap-api.com"  # Will be https://gospelmap-global.streamlit.app for testing
    
    def __init__(self, api_key: str, parish_id: str):
        self.api_key = api_key
        self.parish_id = parish_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def is_enabled(self) -> bool:
        """Check if GospelMap sync is configured"""
        return bool(self.api_key and self.parish_id)
    
    def push_parish_data(self, parish_data: Dict) -> bool:
        """
        Push local parish data to GospelMap
        Makes parish discoverable globally
        """
        try:
            payload = {
                "parish_id": self.parish_id,
                "name": parish_data.get("name"),
                "diocese": parish_data.get("diocese"),
                "country": parish_data.get("country"),
                "location": parish_data.get("location"),
                "languages": parish_data.get("languages", []),
                
                # Accessibility
                "accessibility": {
                    "wheelchair": parish_data.get("wheelchair_accessible", False),
                    "hearing_loop": parish_data.get("hearing_loop", False),
                    "nursery": parish_data.get("nursery", False)
                },
                
                # Welcome indices (self-reported)
                "welcome": {
                    "lgbtq": parish_data.get("welcome_lgbtq", 5),
                    "divorced": parish_data.get("welcome_divorced", 5),
                    "immigrant": parish_data.get("welcome_immigrant", 5),
                    "poor": parish_data.get("welcome_poor", 5)
                },
                
                # Sacraments
                "sacraments": {
                    "masses_per_week": parish_data.get("masses_per_week", 0),
                    "baptisms_available": parish_data.get("baptisms_available", True),
                    "marriages_available": parish_data.get("marriages_available", True),
                    "confession_hours": parish_data.get("confession_hours", "By appointment")
                },
                
                # Material Aid
                "material_aid": {
                    "food_pantry": parish_data.get("food_pantry"),
                    "homeless_shelter": parish_data.get("homeless_shelter"),
                    "medical_clinic": parish_data.get("medical_clinic")
                },
                
                # Justice Work
                "justice_work": {
                    "active_campaigns": parish_data.get("active_campaigns", []),
                    "volunteers_engaged": parish_data.get("volunteers_engaged", 0),
                    "engagement_pct": parish_data.get("justice_engagement_pct", 0)
                },
                
                # Stewardship/Finances
                "stewardship": {
                    "transparency": parish_data.get("budget_public", False),
                    "monthly_giving": parish_data.get("monthly_giving", 0),
                    "allocation": parish_data.get("budget_allocation", {})
                },
                
                # Volunteer Capacity
                "volunteer_capacity": {
                    "total_volunteers": parish_data.get("total_volunteers", 0),
                    "active_volunteers": parish_data.get("active_volunteers", 0),
                    "can_take_refugees": parish_data.get("can_take_refugees", False),
                    "can_host_events": parish_data.get("can_host_events", False)
                },
                
                "last_updated": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.BASE_URL}/api/v1/parishes/sync",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            return response.status_code in [200, 201]
        
        except Exception as e:
            st.error(f"❌ GospelMap sync failed: {str(e)}")
            return False
    
    def get_global_opportunities(self) -> Optional[Dict]:
        """
        Fetch justice campaigns + opportunities from GospelMap
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/api/v1/parishes/{self.parish_id}/opportunities",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            
            return None
        
        except Exception as e:
            st.warning(f"⚠️ Could not fetch global opportunities: {str(e)}")
            return None
    
    def join_campaign(self, campaign_id: str, volunteers: int) -> bool:
        """
        Join a global justice campaign
        """
        try:
            payload = {
                "parish_id": self.parish_id,
                "campaign_id": campaign_id,
                "volunteers": volunteers,
                "action": "join",
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.BASE_URL}/api/v1/campaigns/{campaign_id}/join",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            return response.status_code in [200, 201]
        
        except Exception as e:
            st.error(f"❌ Could not join campaign: {str(e)}")
            return False
    
    def report_campaign_impact(
        self,
        campaign_id: str,
        workers_helped: int,
        wage_increase_pct: float,
        notes: str
    ) -> bool:
        """
        Report impact from justice campaign to GospelMap
        """
        try:
            payload = {
                "parish_id": self.parish_id,
                "campaign_id": campaign_id,
                "action": "report_impact",
                "data": {
                    "workers_helped": workers_helped,
                    "wage_increase_pct": wage_increase_pct,
                    "notes": notes
                },
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.BASE_URL}/api/v1/campaigns/{campaign_id}/impact",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            return response.status_code in [200, 201]
        
        except Exception as e:
            st.error(f"❌ Could not report impact: {str(e)}")
            return False


# Demo data for testing (when GospelMap not connected)
DEMO_OPPORTUNITIES = {
    "campaigns_to_join": [
        {
            "id": "living-wage-global",
            "name": "Living Wage - East Africa",
            "status": "active",
            "parishes_involved": 150,
            "workers_affected": 5000,
            "volunteers_needed": 50,
            "impact": "26% average wage increase",
            "description": "Coordinating living wage campaigns across tea, coffee, and domestic workers"
        },
        {
            "id": "refugee-rights",
            "name": "Refugee Rights",
            "status": "active",
            "parishes_involved": 89,
            "workers_affected": 12000,
            "volunteers_needed": 30,
            "impact": "Policy wins in 3 countries",
            "description": "Advocating for migrant worker protections and integration support"
        },
        {
            "id": "housing-justice",
            "name": "Housing Justice",
            "status": "active",
            "parishes_involved": 67,
            "workers_affected": 8000,
            "volunteers_needed": 25,
            "impact": "$120M in affordable housing created",
            "description": "Fighting homelessness through community organizing"
        }
    ],
    "nearby_parishes": [
        {
            "id": "all-saints-nairobi",
            "name": "All Saints - Nairobi",
            "distance_km": 12,
            "shared_campaigns": ["living-wage-global"],
            "contact": "pastor@allsaints.co.ke"
        },
        {
            "id": "st-marys-karen",
            "name": "St. Mary's - Karen",
            "distance_km": 8,
            "shared_campaigns": ["housing-justice"],
            "contact": "parish@stmarys-karen.co.ke"
        }
    ],
    "bishop_updates": {
        "diocese": "Archdiocese of Nairobi",
        "accountability_score": 6.8,
        "transparency_trend": "improving",
        "recent_improvements": [
            "Financial transparency increased",
            "New diversity hiring policy",
            "LGBTQ+ welcome statement"
        ],
        "areas_to_work_on": [
            "Abuse prevention training",
            "Lay leadership expansion"
        ]
    },
    "diaspora_networks": [
        {
            "name": "Kenyan Catholics in Diaspora",
            "size": 500000,
            "major_locations": ["USA", "UK", "UAE", "Canada"],
            "justice_work": "Migrant worker support + remittance programs"
        }
    ]
}
