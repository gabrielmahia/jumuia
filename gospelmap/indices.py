"""
GospelMap Indices - Real-time crisis signal detection
Like OpenResilience: Multi-dimensional indices for decision support
"""

from typing import Dict
import math


class EcosystemIndices:
    """Calculate parish + diocesan health indices in real-time"""
    
    @staticmethod
    def calculate_pastoral_crisis_index(
        priest_vacancies: int,
        total_priests: int,
        abuse_allegations_recent: int,  # Last 5 years
        youth_engagement_pct: float,
        immigrant_integration_score: float,  # 0-10
        leadership_opacity_score: float  # 0-10, higher = more opaque
    ) -> float:
        """
        PASTORAL CRISIS INDEX (0-10)
        Measures spiritual health and safety of parish
        
        Components:
        - Priest shortage (vacancy rate)
        - Abuse allegations and response
        - Youth engagement (turnover indicator)
        - Immigrant integration
        - Leadership transparency
        """
        
        # Priest shortage component
        if total_priests > 0:
            vacancy_rate = priest_vacancies / max(total_priests + priest_vacancies, 1)
        else:
            vacancy_rate = 1.0
        priest_crisis = min(vacancy_rate * 10, 10)  # 0-10
        
        # Abuse component (0-10)
        # More than 3 allegations in 5 years = crisis
        abuse_crisis = min(abuse_allegations_recent / 3 * 10, 10)
        
        # Youth engagement (low engagement = crisis)
        youth_crisis = max(0, (100 - youth_engagement_pct) / 10)  # Inverted
        
        # Immigrant integration (low = crisis)
        integration_crisis = (10 - immigrant_integration_score)  # Inverted
        
        # Leadership opacity
        opacity_crisis = leadership_opacity_score  # Higher = worse
        
        # Composite (weighted average)
        pci = (
            priest_crisis * 0.25 +
            abuse_crisis * 0.25 +
            youth_crisis * 0.15 +
            integration_crisis * 0.15 +
            opacity_crisis * 0.20
        )
        
        return round(min(max(pci, 0), 10), 1)
    
    @staticmethod
    def calculate_material_crisis_index(
        food_insecurity_pct: float,  # % in parish area
        homelessness_gap_pct: float,  # % needing shelter but unavailable
        healthcare_gap_pct: float,  # % without access
        education_gap_pct: float,  # % without access
        emergency_response_time_hours: float  # How quickly parish responds
    ) -> float:
        """
        MATERIAL CRISIS INDEX (0-10)
        Measures material well-being of those parish serves
        
        Components:
        - Food insecurity
        - Homelessness (gap between need and supply)
        - Healthcare gaps
        - Education gaps
        - Emergency response capacity
        """
        
        # Each gap is 0-10 scale
        food_crisis = food_insecurity_pct / 10  # If 50% insecure = 5.0
        homelessness_crisis = homelessness_gap_pct / 10
        healthcare_crisis = healthcare_gap_pct / 10
        education_crisis = education_gap_pct / 10
        
        # Response time (slow = crisis)
        # Fast response < 1 hour = 0, slow > 24 hours = 10
        response_crisis = min(emergency_response_time_hours / 2.4, 10)
        
        # Composite
        mci = (
            food_crisis * 0.25 +
            homelessness_crisis * 0.25 +
            healthcare_crisis * 0.20 +
            education_crisis * 0.20 +
            response_crisis * 0.10
        )
        
        return round(min(max(mci, 0), 10), 1)
    
    @staticmethod
    def calculate_justice_crisis_index(
        living_wage_gap_pct: float,  # % of workers below just wage
        housing_insecurity_pct: float,
        refugee_vulnerability_score: float,  # 0-10
        climate_impact_score: float,  # 0-10
        racial_justice_gap_score: float,  # 0-10
        active_campaigns_count: int,
        parish_justice_engagement_pct: float  # % involved
    ) -> float:
        """
        JUSTICE CRISIS INDEX (0-10)
        Measures structural injustices affecting parish area
        AND parish response to them
        
        Components:
        - Wage gaps
        - Housing crisis
        - Refugee vulnerability
        - Climate impact
        - Racial equity gaps
        - Parish response (% in campaigns)
        """
        
        # Structural injustices (reality)
        wage_crisis = living_wage_gap_pct / 10
        housing_crisis = housing_insecurity_pct / 10
        refugee_crisis = refugee_vulnerability_score
        climate_crisis = climate_impact_score
        racial_crisis = racial_justice_gap_score
        
        # Parish response (if high crisis but no response = worse)
        structural_crisis = (
            wage_crisis * 0.20 +
            housing_crisis * 0.20 +
            refugee_crisis * 0.20 +
            climate_crisis * 0.20 +
            racial_crisis * 0.20
        )
        
        # Response score (0-10, lower = better response)
        # If crisis is high but engagement low = bad response
        if structural_crisis > 5 and parish_justice_engagement_pct < 3:
            response_gap = 8  # Bad response to high crisis
        elif structural_crisis > 5 and parish_justice_engagement_pct > 15:
            response_gap = 2  # Good response to high crisis
        else:
            response_gap = max(0, 10 - parish_justice_engagement_pct)
        
        # Composite (crisis + poor response = worse)
        jci = (structural_crisis * 0.7) + (response_gap * 0.3)
        
        return round(min(max(jci, 0), 10), 1)
    
    @staticmethod
    def calculate_financial_transparency_index(
        budget_public: bool,
        overhead_pct: float,  # Ideal: 10-15%
        charitable_pct: float,  # Ideal: 80%+
        accountability_structures: int,  # Count: finance council, external audit, etc.
        years_of_disclosure: int,
        responsive_to_questions: bool
    ) -> float:
        """
        FINANCIAL TRANSPARENCY INDEX (0-10)
        Higher = more transparent
        
        Components:
        - Budget publicly available
        - Reasonable overhead
        - High charitable allocation
        - Accountability mechanisms
        - Historical disclosure
        - Responsiveness to community
        """
        
        # Budget public
        budget_score = 2.0 if budget_public else 0.0
        
        # Overhead reasonableness
        # Ideal 10-15%, bad if > 25% or < 5% (too little internal function)
        if 10 <= overhead_pct <= 15:
            overhead_score = 2.0
        elif 5 <= overhead_pct <= 25:
            overhead_score = 1.0
        else:
            overhead_score = 0.0
        
        # Charitable allocation
        # Ideal 80%+, poor if < 60%
        if charitable_pct >= 80:
            charitable_score = 3.0
        elif charitable_pct >= 60:
            charitable_score = 1.5
        else:
            charitable_score = 0.0
        
        # Accountability structures
        # Each structure (council, audit, community oversight) = +0.5
        structure_score = min(accountability_structures * 0.5, 2.0)
        
        # Historical disclosure
        # +0.5 per year up to 5 years
        disclosure_score = min(years_of_disclosure * 0.5, 2.5)
        
        # Responsiveness
        responsiveness_score = 1.0 if responsive_to_questions else 0.0
        
        # Composite (out of 10 max)
        fti = (
            budget_score +
            overhead_score +
            charitable_score +
            structure_score +
            disclosure_score +
            responsiveness_score
        )
        
        return round(min(max(fti, 0), 10), 1)
    
    @staticmethod
    def calculate_welcome_index(
        lgbtq_welcome: float,
        divorced_remarried_welcome: float,
        interfaith_welcome: float,
        immigrant_refugee_welcome: float,
        poor_welcome: float,  # Financial accessibility
        women_leadership_pct: float
    ) -> float:
        """
        WELCOME INDEX (0-10)
        Composite measure of inclusivity
        """
        
        # Normalize women leadership to 0-10
        women_score = (women_leadership_pct / 100) * 10
        
        welcome = (
            lgbtq_welcome * 0.20 +
            divorced_remarried_welcome * 0.20 +
            interfaith_welcome * 0.15 +
            immigrant_refugee_welcome * 0.20 +
            poor_welcome * 0.15 +
            women_score * 0.10
        )
        
        return round(min(max(welcome, 0), 10), 1)
    
    @staticmethod
    def calculate_ecosystem_health_score(
        pci: float,  # Pastoral Crisis Index
        mci: float,  # Material Crisis Index
        jci: float,  # Justice Crisis Index
        fti: float,  # Financial Transparency Index
        welcome_index: float,
        positive_factors: float = 1.0  # Bonus for extra good things
    ) -> float:
        """
        ECOSYSTEM HEALTH SCORE (0-10, where 10 = perfectly healthy)
        Composite of all indices
        
        Higher = healthier
        All indices are 0-10 where 10 = crisis/bad
        So we invert them: 10 - crisis_score = health
        """
        
        # Invert crisis indices (higher crisis = lower health)
        pastoral_health = 10 - pci
        material_health = 10 - mci
        justice_health = 10 - jci
        
        # Transparency and welcome are already positive
        transparency_health = fti
        
        # Composite (weighted)
        ehs = (
            pastoral_health * 0.25 +
            material_health * 0.20 +
            justice_health * 0.20 +
            transparency_health * 0.15 +
            welcome_index * 0.20
        ) * positive_factors
        
        return round(min(max(ehs, 0), 10), 1)
    
    @staticmethod
    def interpret_index(score: float, index_type: str) -> tuple:
        """
        Interpret numerical index as human-readable label + color
        
        Returns: (label, color, recommendation)
        """
        
        color_map = {
            "green": "#2ecc71",      # Healthy
            "yellow": "#f39c12",     # Monitor
            "orange": "#e74c3c",     # Serious
            "red": "#c0392b"         # Crisis
        }
        
        if index_type in ["PCI", "MCI", "JCI"]:
            # Crisis indices: low score is good
            if score < 2:
                return ("Excellent", color_map["green"], "Continue good practices")
            elif score < 4:
                return ("Good", color_map["green"], "Monitor quarterly")
            elif score < 6:
                return ("Fair", color_map["yellow"], "Address issues within 6 months")
            elif score < 8:
                return ("Serious", color_map["orange"], "Urgent improvement needed")
            else:
                return ("Crisis", color_map["red"], "Immediate intervention required")
        
        elif index_type in ["FTI", "EHS", "Welcome"]:
            # Positive indices: high score is good
            if score > 8:
                return ("Excellent", color_map["green"], "Model for others")
            elif score > 6:
                return ("Good", color_map["green"], "Continue practices")
            elif score > 4:
                return ("Fair", color_map["yellow"], "Improvements recommended")
            elif score > 2:
                return ("Poor", color_map["orange"], "Significant work needed")
            else:
                return ("Crisis", color_map["red"], "Complete overhaul required")
        
        return ("Unknown", color_map["yellow"], "Review data")


# Usage example
if __name__ == "__main__":
    # Example: Calculate indices for a fictional parish
    pci = EcosystemIndices.calculate_pastoral_crisis_index(
        priest_vacancies=2,
        total_priests=5,
        abuse_allegations_recent=0,
        youth_engagement_pct=8,
        immigrant_integration_score=7,
        leadership_opacity_score=4
    )
    print(f"Pastoral Crisis Index: {pci}/10")
    label, color, recommendation = EcosystemIndices.interpret_index(pci, "PCI")
    print(f"Status: {label} ({color})")
    print(f"Recommendation: {recommendation}")
    
    # Calculate material crisis
    mci = EcosystemIndices.calculate_material_crisis_index(
        food_insecurity_pct=15,
        homelessness_gap_pct=20,
        healthcare_gap_pct=10,
        education_gap_pct=5,
        emergency_response_time_hours=2
    )
    print(f"\nMaterial Crisis Index: {mci}/10")
    
    # Calculate justice crisis
    jci = EcosystemIndices.calculate_justice_crisis_index(
        living_wage_gap_pct=35,
        housing_insecurity_pct=12,
        refugee_vulnerability_score=6,
        climate_impact_score=4,
        racial_justice_gap_score=5,
        active_campaigns_count=3,
        parish_justice_engagement_pct=12
    )
    print(f"Justice Crisis Index: {jci}/10")
    
    # Calculate ecosystem health
    welcome_index = EcosystemIndices.calculate_welcome_index(
        lgbtq_welcome=7,
        divorced_remarried_welcome=8,
        interfaith_welcome=6,
        immigrant_refugee_welcome=9,
        poor_welcome=8,
        women_leadership_pct=35
    )
    
    fti = EcosystemIndices.calculate_financial_transparency_index(
        budget_public=True,
        overhead_pct=12,
        charitable_pct=85,
        accountability_structures=3,
        years_of_disclosure=4,
        responsive_to_questions=True
    )
    
    ehs = EcosystemIndices.calculate_ecosystem_health_score(
        pci=pci,
        mci=mci,
        jci=jci,
        fti=fti,
        welcome_index=welcome_index,
        positive_factors=1.0
    )
    
    print(f"\nEcosystem Health Score: {ehs}/10")
    label, color, recommendation = EcosystemIndices.interpret_index(ehs, "EHS")
    print(f"Status: {label} ({color})")
    print(f"Recommendation: {recommendation}")

