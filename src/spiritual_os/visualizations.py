"""
Visualization & Reporting Utilities
Charts, maps, and reports for all lenses
"""

import streamlit as st
import json
from typing import List, Dict, Any
from datetime import datetime


class Visualizations:
    """Create visualizations for each lens"""
    
    @staticmethod
    def personal_dashboard(user_data: Dict[str, Any]):
        """Personal formation dashboard visualizations"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Daily Practices", "3/6", "+1 from yesterday")
        
        with col2:
            st.metric("Weekly Commitment", "2h 15m", "+15m this week")
        
        with col3:
            st.metric("Streak", "12 days", "Keep going!")
    
    @staticmethod
    def parish_analytics(parish_data: Dict[str, Any]):
        """Parish-level analytics"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Formation Growth",
                f"+8%",
                "Year-over-year"
            )
        
        with col2:
            st.metric(
                "Volunteer Engagement",
                f"+12%",
                "Increased participation"
            )
        
        with col3:
            st.metric(
                "Justice Impact",
                f"+15%",
                "More parishioners helping"
            )
    
    @staticmethod
    def diocese_trends(diocese_data: Dict[str, Any]):
        """Diocese trend analysis"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Formation", "+12%", "Diocese-wide")
        
        with col2:
            st.metric("Attendance", "34K weekly", "Trending stable")
        
        with col3:
            st.metric("Justice", "26K workers", "Helped this year")
        
        with col4:
            st.metric("Vocations", "3 new priests", "Commissioned 2026")
    
    @staticmethod
    def global_campaign_map(campaigns: List[Dict[str, Any]]):
        """Global campaign visualization"""
        st.write("**Active Campaigns by Region:**")
        
        for campaign in campaigns:
            with st.expander(f"📍 {campaign.get('name', 'Campaign')}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Dioceses**: {campaign.get('dioceses_involved', 0)}")
                
                with col2:
                    st.write(f"**Parishes**: {campaign.get('parishes_involved', 0)}")
                
                with col3:
                    st.write(f"**Impact**: {campaign.get('workers_affected', 0)} workers")
    
    @staticmethod
    def crisis_status(crisis_data: Dict[str, Any]):
        """Crisis event status display"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Activated", crisis_data.get('dioceses_affected', 0), "dioceses")
        
        with col2:
            st.metric("Volunteers", crisis_data.get('volunteers_mobilized', 0), "mobilized")
        
        with col3:
            st.metric("People Aided", f"{crisis_data.get('people_receiving_aid', 0):,}")
        
        with col4:
            st.metric("Funds Raised", f"${crisis_data.get('funds_raised', 0):,}")


class Reports:
    """Generate reports for different stakeholders"""
    
    @staticmethod
    def personal_monthly_summary(user_data: Dict[str, Any]) -> str:
        """Generate monthly personal formation summary"""
        report = f"""
# Personal Spiritual Formation - Monthly Report

**Period**: {datetime.now().strftime('%B %Y')}

## Summary
- Daily practices completed: 28/31 days (90% compliance)
- Average daily practice time: 45 minutes
- Journal entries: 28
- Sacramental life: Active

## Practices This Month
- Morning prayer: 28 times
- Lectio Divina: 26 times
- Evening examen: 25 times
- Works of mercy: 30 times

## Insights
- Most consistent: Morning prayer
- Area for growth: Evening examen (need to be more consistent)
- Spiritual highlights: Three moments of deep prayer

## Next Month's Focus
- Increase evening examen consistency
- Deepen Lectio Divina practice
- Continue works of mercy

---
Generated: {datetime.now().isoformat()}
        """
        return report
    
    @staticmethod
    def parish_weekly_summary(parish_data: Dict[str, Any]) -> str:
        """Generate weekly parish summary"""
        report = f"""
# Parish Ministry Report - Weekly Summary

**Parish**: {parish_data.get('name', 'Your Parish')}
**Week of**: {datetime.now().strftime('%B %d, %Y')}

## Attendance & Participation
- Weekend Mass: 342 attendees (up from 328 last week)
- Formation groups: 187 participants
- Volunteers active: 34

## Events This Week
- RCIA: 12 attendees
- Marriage prep: 4 couples
- Service day: 23 volunteers

## Justice Initiatives
- Living wage campaign: $425 donated
- Refugee family support: On track
- Food pantry: 114 families served

## Upcoming
- Community dinner: Thursday 6pm
- Prayer vigil: Friday 8pm
- Parish festival planning meeting: Sunday

---
Generated: {datetime.now().isoformat()}
        """
        return report
    
    @staticmethod
    def bishop_quarterly_transparency(diocese_data: Dict[str, Any]) -> str:
        """Generate bishop's quarterly transparency report"""
        report = f"""
# Diocesan Transparency Report - Q1 2026

**Diocese**: {diocese_data.get('name', 'Diocese')}
**Bishop**: {diocese_data.get('bishop_name', 'Bishop')}
**Period**: January - March 2026

## Formation
- Catholics in daily prayer: 16,800 (+12% YoY)
- Average daily practice: 23 minutes
- New formation groups: 3

## Justice Impact
- Workers helped: 8,900 (of 26,000 YTD goal)
- Policy wins: 1 (living wage increase)
- Parishes engaged: 12

## Sacraments
- Baptisms: 58
- Confirmations: 142
- Marriages: 31
- Funerals: 42

## Challenges
- Marriage numbers declining (need focus)
- Rural parish support inadequate
- Clergy shortage in two counties

## Victories
- Formation participation up across board
- Justice engagement exceeding targets
- New interfaith partnerships formed

## Next Quarter Priorities
1. Develop rural parish support plan
2. Launch marriage prep enhancement
3. Expand justice training programs

---
Submitted: {datetime.now().isoformat()}
        """
        return report
    
    @staticmethod
    def global_impact_report(campaigns: List[Dict[str, Any]]) -> str:
        """Generate global justice impact report"""
        report = f"""
# Global Justice Network - Impact Report 2026

**Report Date**: {datetime.now().strftime('%B %Y')}
**Coverage**: 47 dioceses, 2,300 parishes

## Aggregate Impact
- Total workers helped: 26,000
- Total income increase: $45,000,000
- Policy wins: 5
- Countries: 84

## Campaign Breakdown
- Living Wage (East Africa): 250 parishes, 26,000 workers, +26%
- Living Wage (Latin America): 45 parishes, 8,000 workers, +18%
- Living Wage (Asia): 23 parishes, 3,000 workers, +14%
- Refugee Support: 8 parishes, 45 families
- Housing Justice: 5 parishes, 120 families

## Top Performing Dioceses
1. Diocese of Nairobi: 450 workers, +28%
2. Diocese of Manila: 380 workers, +24%
3. Diocese of Springfield: 260 workers, +26%

## New Pilot Programs (Vote to Scale)
- Tech ethics (AI, labor): 3 dioceses
- Climate justice (green jobs): 8 dioceses
- Debt relief (student loans): 2 dioceses

---
Generated: {datetime.now().isoformat()}
        """
        return report
    
    @staticmethod
    def crisis_response_report(crisis_data: Dict[str, Any]) -> str:
        """Generate crisis response report"""
        report = f"""
# Crisis Response Report - East Africa Drought

**Crisis**: {crisis_data.get('name', 'Crisis')}
**Location**: {crisis_data.get('location', 'Location')}
**Activated**: {crisis_data.get('activated_at', 'Date')}
**Status**: ACTIVE

## Response Summary
- Dioceses activated: {len(crisis_data.get('affected_dioceses', []))}
- Volunteers mobilized: {crisis_data.get('volunteers_mobilized', 0)}
- People receiving aid: {crisis_data.get('people_receiving_aid', 0):,}
- Funds raised: ${crisis_data.get('funds_raised', 0):,}

## Needs Met
- Food distributed: 2,300 packages
- Water filters: 450
- Medical care: 3,400 people
- Temporary shelter: 890 families

## Gaps Identified
- Water: Need 200 more filters
- Transportation: Need 15 more vehicles
- Medical: Need 2 more mobile clinics

## Partners Coordinating
- Catholic Relief Services: 25 staff
- Red Cross: 12 volunteers
- Islamic Relief: 8 teams
- Local NGOs: 35 organizations

## Sustainability Plan
- Phase out emergency aid: Month 4
- Transition to recovery programs: Months 5-6
- Local capacity building: Ongoing

---
Generated: {datetime.now().isoformat()}
        """
        return report


class Exports:
    """Export data in various formats"""
    
    @staticmethod
    def export_personal_to_pdf(user_data: Dict[str, Any]) -> bytes:
        """Export personal data to PDF (for sharing with spiritual director)"""
        # In real implementation, would use reportlab or similar
        pass
    
    @staticmethod
    def export_parish_to_csv(parish_data: Dict[str, Any]) -> str:
        """Export parish data to CSV"""
        # In real implementation, would generate proper CSV
        pass
    
    @staticmethod
    def export_diocese_to_json(diocese_data: Dict[str, Any]) -> str:
        """Export diocese data to JSON"""
        return json.dumps(diocese_data, indent=2)
    
    @staticmethod
    def share_campaign_stats(campaign_data: Dict[str, Any]) -> str:
        """Generate shareable campaign statistics"""
        text = f"""
🌍 Global Justice Campaign: {campaign_data.get('name', 'Campaign')}

📊 Impact:
• {campaign_data.get('workers_affected', 0):,} workers helped
• +{campaign_data.get('wage_increase_percent', 0):.0f}% wage increase
• ${campaign_data.get('income_increase', 0):,} income gained
• {campaign_data.get('policy_wins', 0)} policy victories

✊ Coordinated by {len(campaign_data.get('dioceses', []))} dioceses
    across {campaign_data.get('countries', 0)} countries

Join us: [Link to campaign]
        """
        return text
