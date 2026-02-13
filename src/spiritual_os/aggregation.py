"""
Aggregation Logic - Compute aggregates from individual data
Runs on a schedule to update parish/diocese/global aggregates
"""

from typing import List, Dict, Optional
from src.spiritual_os.models import User, Parish, Diocese, JusticeCampaign


class AggregationEngine:
    """Compute aggregates from detailed user data"""
    
    @staticmethod
    def aggregate_parish_from_users(users: List[User], parish: Parish) -> Parish:
        """
        Compute parish aggregates from all users who opted in
        """
        # Filter users in this parish who opted in
        parish_users = [
            u for u in users 
            if u.parish_id == parish.id and u.opt_in_to_parish_aggregates
        ]
        
        if not parish_users:
            parish.aggregated_members_count = 0
            parish.aggregated_formation_participants = 0
            parish.aggregated_avg_practice_minutes = 0.0
            return parish
        
        # Count members
        parish.aggregated_members_count = len(parish_users)
        
        # Count formation participants (people with Rule of Life)
        formation_participants = sum(
            1 for u in parish_users 
            if u.rule_of_life and len(u.rule_of_life) > 0
        )
        parish.aggregated_formation_participants = formation_participants
        
        # Average practice time
        total_minutes = 0
        practice_count = 0
        for user in parish_users:
            if user.rule_of_life:
                # Assume rule has "entries" list with "duration_minutes"
                for entry in user.rule_of_life.get("entries", []):
                    total_minutes += entry.get("duration_minutes", 0)
                    practice_count += 1
        
        if practice_count > 0:
            parish.aggregated_avg_practice_minutes = total_minutes / practice_count
        
        # Sacrament stats (aggregate counts)
        sacrament_counts = {}
        for user in parish_users:
            for milestone in user.sacrament_milestones:
                sacrament_type = milestone.get("name", "Unknown")
                sacrament_counts[sacrament_type] = sacrament_counts.get(sacrament_type, 0) + 1
        
        parish.aggregated_sacrament_stats = sacrament_counts
        
        return parish
    
    @staticmethod
    def aggregate_diocese_from_parishes(parishes: List[Parish], diocese: Diocese) -> Diocese:
        """
        Compute diocese aggregates from all parishes
        """
        diocese_parishes = [p for p in parishes if p.diocese_id == diocese.id]
        
        if not diocese_parishes:
            return diocese
        
        # Simple aggregates
        diocese.aggregated_parishes_count = len(diocese_parishes)
        
        # Aggregate formation
        total_formation = sum(p.aggregated_formation_participants for p in diocese_parishes)
        diocese.aggregated_formation_participants = total_formation
        
        # Estimate total Catholics (rough: avg parish size × parishes)
        avg_parish_size = 2000  # Reasonable estimate
        diocese.aggregated_total_catholics = len(diocese_parishes) * avg_parish_size
        
        # Estimate weekly attendance (rough: 35% of Catholics)
        diocese.aggregated_weekly_attendance = int(diocese.aggregated_total_catholics * 0.35)
        
        return diocese
    
    @staticmethod
    def aggregate_campaign_impact(
        campaign: JusticeCampaign,
        diocese_data: Dict[str, Dict]
    ) -> JusticeCampaign:
        """
        Compute campaign aggregates from participating dioceses
        
        diocese_data: {diocese_id: {
            "workers": 8000,
            "wage_increase_percent": 26,
            "policy_wins": 1
        }}
        """
        if not campaign.dioceses_joined:
            return campaign
        
        total_workers = 0
        total_wage_increase = 0.0
        total_income_increase = 0
        total_policy_wins = 0
        
        for diocese_id in campaign.dioceses_joined:
            if diocese_id in diocese_data:
                data = diocese_data[diocese_id]
                workers = data.get("workers", 0)
                wage_pct = data.get("wage_increase_percent", 0)
                
                total_workers += workers
                total_wage_increase += wage_pct
                total_income_increase += int(workers * wage_pct * 500)  # Rough estimate: $500 per % increase
                total_policy_wins += data.get("policy_wins", 0)
        
        campaign.aggregated_workers_affected = total_workers
        
        if campaign.dioceses_joined:
            campaign.aggregated_wage_increase_percent = total_wage_increase / len(campaign.dioceses_joined)
        
        campaign.aggregated_income_increase_dollars = total_income_increase
        campaign.aggregated_policy_wins = total_policy_wins
        
        return campaign


class QueryBuilder:
    """Build permission-aware queries based on user role"""
    
    @staticmethod
    def get_visible_users(
        all_users: List[User],
        requesting_user: User,
        permission_context
    ) -> List[User]:
        """Return users visible to requesting_user based on permissions"""
        visible = []
        
        if permission_context.role.value == "individual":
            # Individuals can only see themselves
            visible = [u for u in all_users if u.id == requesting_user.id]
        
        elif permission_context.role.value == "parish_coordinator":
            # Coordinators see all users in their parish (but only aggregates, not details)
            visible = [u for u in all_users if u.parish_id == requesting_user.parish_id]
        
        elif permission_context.role.value == "diocesan_leader":
            # Leaders see all users in diocese (aggregated)
            visible = [u for u in all_users if u.diocese_id == requesting_user.diocese_id]
        
        else:
            # Global/crisis: no direct user view
            visible = []
        
        return visible
    
    @staticmethod
    def get_visible_parishes(
        all_parishes: List[Parish],
        requesting_user: User,
        permission_context
    ) -> List[Parish]:
        """Return parishes visible to requesting_user"""
        visible = []
        
        if permission_context.role.value == "individual":
            # See your parish only
            visible = [p for p in all_parishes if p.id == requesting_user.parish_id]
        
        elif permission_context.role.value == "parish_coordinator":
            # See your parish only
            visible = [p for p in all_parishes if p.id == requesting_user.parish_id]
        
        elif permission_context.role.value == "diocesan_leader":
            # See all parishes in your diocese
            visible = [p for p in all_parishes if p.diocese_id == requesting_user.diocese_id]
        
        elif permission_context.role.value == "global_coordinator":
            # See all parishes (aggregated only)
            visible = all_parishes
        
        return visible
    
    @staticmethod
    def get_visible_dioceses(
        all_dioceses: List[Diocese],
        requesting_user: User,
        permission_context
    ) -> List[Diocese]:
        """Return dioceses visible to requesting_user"""
        visible = []
        
        if permission_context.role.value in ["individual", "parish_coordinator"]:
            # Don't see diocese-level data directly
            visible = []
        
        elif permission_context.role.value == "diocesan_leader":
            # See your diocese
            visible = [d for d in all_dioceses if d.id == requesting_user.diocese_id]
        
        elif permission_context.role.value == "global_coordinator":
            # See all dioceses (aggregated)
            visible = all_dioceses
        
        return visible
    
    @staticmethod
    def get_visible_campaigns(
        all_campaigns: List[JusticeCampaign],
        requesting_user: User,
        permission_context
    ) -> List[JusticeCampaign]:
        """Return campaigns visible to requesting_user"""
        visible = []
        
        if permission_context.role.value in ["individual", "parish_coordinator"]:
            # Limited access to campaigns (maybe through parish)
            visible = all_campaigns  # Show all but aggregated view
        
        elif permission_context.role.value == "diocesan_leader":
            # See all campaigns
            visible = all_campaigns
        
        elif permission_context.role.value == "global_coordinator":
            # See all campaigns in detail
            visible = all_campaigns
        
        return visible
