"""
Input Forms - Streamlit components for data collection
Handles Rule of Life, journal entries, events, etc.
"""

import streamlit as st
from datetime import datetime, time
from typing import Dict, Any


class PersonalForms:
    """Forms for individual user data"""
    
    @staticmethod
    def rule_of_life_entry() -> Dict[str, Any]:
        """Form to add a Rule of Life entry"""
        st.subheader("➕ Add Practice to Rule of Life")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Practice name", placeholder="Morning prayer")
            category = st.selectbox("Category", [
                "prayer",
                "scripture",
                "examen",
                "virtue",
                "fasting",
                "mercy",
                "other"
            ])
        
        with col2:
            duration_minutes = st.number_input("Duration (minutes)", 1, 180, 15)
            frequency = st.selectbox("Frequency", [
                "daily",
                "weekly",
                "monthly",
                "occasional"
            ])
        
        time_of_day = st.selectbox("Time of day (optional)", [
            "morning",
            "midday",
            "evening",
            "any time"
        ])
        
        notes = st.text_area("Notes (optional)", placeholder="Why this practice matters to you")
        
        if st.button("✅ Add to Rule of Life"):
            if name:
                return {
                    "name": name,
                    "category": category,
                    "duration_minutes": duration_minutes,
                    "frequency": frequency,
                    "time_of_day": time_of_day,
                    "notes": notes,
                    "added_at": datetime.now().isoformat(),
                }
            else:
                st.error("Please enter a practice name")
        
        return None
    
    @staticmethod
    def journal_entry(template_type: str = "examen") -> Dict[str, Any]:
        """Form for journal entry"""
        st.subheader(f"📔 {template_type.upper()} Reflection")
        
        templates = {
            "examen": [
                "Where did I feel God's grace today?",
                "Where did I fall short? What would I do differently?",
                "Who did I help? Who helped me?",
                "What am I grateful for?",
                "What do I ask forgiveness for?",
            ],
            "lectio_divina": [
                "LECTIO - What word or phrase strikes you?",
                "MEDITATIO - What does it mean for your life?",
                "ORATIO - What do you say to God?",
                "CONTEMPLATIO - How will this change you?",
            ],
            "hardening_vs_healing": [
                "Where do I feel my heart closing? Why?",
                "Where do I feel my heart opening?",
                "What would it look like to let God heal this?",
                "Who can I talk to about this?",
            ],
            "fatigue_warning": [
                "Where do I feel spiritually dry?",
                "What needs are going unmet?",
                "What small practice could help?",
                "Who can support me?",
            ],
        }
        
        prompts = templates.get(template_type, [])
        responses = {}
        
        for i, prompt in enumerate(prompts):
            responses[f"response_{i}"] = st.text_area(
                prompt,
                placeholder="Your reflection...",
                height=100,
                key=f"journal_{i}"
            )
        
        title = st.text_input("Title (optional)", placeholder="Today's reflection")
        
        if st.button("💾 Save Entry"):
            return {
                "title": title or f"{template_type} - {datetime.now().strftime('%Y-%m-%d')}",
                "template_type": template_type,
                "responses": responses,
                "created_at": datetime.now().isoformat(),
            }
        
        return None
    
    @staticmethod
    def sacrament_milestone() -> Dict[str, Any]:
        """Form for sacramental milestone"""
        st.subheader("🛐 Record Sacramental Milestone")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.selectbox("Sacrament", [
                "Baptism",
                "Confirmation",
                "Eucharist (First Communion)",
                "Reconciliation (Penance)",
                "Marriage",
                "Holy Orders (Priesthood)",
                "Anointing of the Sick",
            ])
            
            category = st.selectbox("Stage", [
                "received",
                "preparation_started",
                "preparation_ongoing",
            ])
        
        with col2:
            date_received = st.date_input("Date")
            location = st.text_input("Location", placeholder="Church name")
        
        minister = st.text_input("Minister (optional)", placeholder="Priest/Bishop name")
        notes = st.text_area("Notes", placeholder="Your reflection on this sacrament")
        
        if st.button("✅ Save Sacramental Milestone"):
            if name:
                return {
                    "name": name,
                    "category": category,
                    "date_received": date_received.isoformat() if category == "received" else None,
                    "location": location,
                    "minister": minister,
                    "notes": notes,
                    "recorded_at": datetime.now().isoformat(),
                }
            else:
                st.error("Please select a sacrament")
        
        return None


class ParishForms:
    """Forms for parish coordinators"""
    
    @staticmethod
    def bulletin_update() -> Dict[str, Any]:
        """Form to update parish bulletin"""
        st.subheader("📰 Update Bulletin")
        
        text = st.text_area(
            "Bulletin content (Markdown supported)",
            placeholder="# This Sunday\n\nReadings: ...",
            height=300
        )
        
        if st.button("✅ Update Bulletin"):
            if text:
                return {
                    "content": text,
                    "updated_at": datetime.now().isoformat(),
                }
            else:
                st.error("Please enter bulletin content")
        
        return None
    
    @staticmethod
    def event_creation() -> Dict[str, Any]:
        """Form to create parish event"""
        st.subheader("📅 Create Event")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Event name", placeholder="RCIA Class")
            event_date = st.date_input("Date")
            event_time = st.time_input("Time")
        
        with col2:
            location = st.text_input("Location", placeholder="Church hall")
            description = st.text_area("Description", height=100)
        
        ministry = st.selectbox("Ministry", [
            "Formation",
            "Sacraments",
            "Service",
            "Social",
            "Other"
        ])
        
        if st.button("✅ Create Event"):
            if name:
                return {
                    "name": name,
                    "date": event_date.isoformat(),
                    "time": str(event_time),
                    "location": location,
                    "description": description,
                    "ministry": ministry,
                    "created_at": datetime.now().isoformat(),
                }
            else:
                st.error("Please enter event name")
        
        return None
    
    @staticmethod
    def volunteer_management() -> Dict[str, Any]:
        """Form for volunteer signup/management"""
        st.subheader("👥 Volunteer Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Volunteer name")
            skills = st.multiselect("Skills", [
                "Food preparation",
                "Construction",
                "Medical",
                "Childcare",
                "Translation",
                "Music",
                "Other"
            ])
        
        with col2:
            availability = st.multiselect("Available", [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ])
            
            has_transportation = st.checkbox("Has vehicle for transportation")
        
        notes = st.text_area("Notes")
        
        if st.button("✅ Register Volunteer"):
            if name:
                return {
                    "name": name,
                    "skills": skills,
                    "availability": availability,
                    "has_transportation": has_transportation,
                    "notes": notes,
                    "registered_at": datetime.now().isoformat(),
                }
            else:
                st.error("Please enter volunteer name")
        
        return None


class DioceseForums:
    """Forms for diocesan leaders"""
    
    @staticmethod
    def transparency_update() -> Dict[str, Any]:
        """Form for bishop's transparency report"""
        st.subheader("📊 Update Transparency Report")
        
        priorities = st.text_area(
            "What are you prioritizing this year?",
            placeholder="Formation, Justice, Vocations, etc.",
            height=150
        )
        
        accomplishments = st.text_area(
            "What progress have we made?",
            placeholder="Formation +12%, Workers helped 26,000, etc.",
            height=150
        )
        
        challenges = st.text_area(
            "What challenges are we facing?",
            placeholder="Marriages declining, Rural support needed, etc.",
            height=150
        )
        
        if st.button("✅ Update Transparency Report"):
            if priorities or accomplishments or challenges:
                return {
                    "priorities": priorities,
                    "accomplishments": accomplishments,
                    "challenges": challenges,
                    "updated_at": datetime.now().isoformat(),
                }
            else:
                st.error("Please fill in at least one field")
        
        return None
    
    @staticmethod
    def strategic_plan() -> Dict[str, Any]:
        """Form for 5-year strategic plan"""
        st.subheader("📋 5-Year Strategic Plan")
        
        st.write("**Priority Areas:**")
        
        goals = {}
        for i in range(1, 6):
            goal = st.text_input(f"Priority {i}", placeholder="e.g., Double formation engagement")
            if goal:
                goals[f"priority_{i}"] = goal
        
        if st.button("✅ Save Strategic Plan"):
            if goals:
                return {
                    "goals": goals,
                    "updated_at": datetime.now().isoformat(),
                }
            else:
                st.error("Please add at least one priority")
        
        return None


class CrisisForms:
    """Forms for crisis coordination"""
    
    @staticmethod
    def volunteer_registration() -> Dict[str, Any]:
        """Form to register volunteers for crisis"""
        st.subheader("👥 Register for Crisis Response")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name")
            phone = st.text_input("Phone")
        
        with col2:
            skills = st.multiselect("Skills", [
                "Medical",
                "Logistics",
                "Food preparation",
                "Childcare",
                "Construction",
                "Translation"
            ])
            
            availability = st.selectbox("When can you help?", [
                "Immediately",
                "Next 24 hours",
                "Next 3 days",
                "Next week"
            ])
        
        if st.button("✅ Register"):
            if name:
                return {
                    "name": name,
                    "phone": phone,
                    "skills": skills,
                    "availability": availability,
                    "registered_at": datetime.now().isoformat(),
                }
            else:
                st.error("Please enter your name")
        
        return None
    
    @staticmethod
    def resource_donation() -> Dict[str, Any]:
        """Form to log resource donations"""
        st.subheader("📦 Log Resource Donation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            resource_type = st.selectbox("Resource type", [
                "Food",
                "Water",
                "Medical supplies",
                "Blankets/Shelter",
                "Cash",
                "Transportation",
                "Other"
            ])
            
            quantity = st.number_input("Quantity", 1, 10000)
        
        with col2:
            unit = st.selectbox("Unit", [
                "pieces",
                "kilos",
                "liters",
                "kits",
                "dollars",
                "vehicles"
            ])
            
            donor_name = st.text_input("Donor name (optional)")
        
        notes = st.text_area("Notes")
        
        if st.button("✅ Log Donation"):
            return {
                "resource_type": resource_type,
                "quantity": quantity,
                "unit": unit,
                "donor_name": donor_name,
                "notes": notes,
                "logged_at": datetime.now().isoformat(),
            }
        
        return None
    
    @staticmethod
    def needs_assessment() -> Dict[str, Any]:
        """Form to report crisis needs"""
        st.subheader("🆘 Report Crisis Needs")
        
        need_type = st.selectbox("Type of need", [
            "Food",
            "Water",
            "Medical",
            "Shelter",
            "Psychosocial",
            "Livestock support",
            "Other"
        ])
        
        affected_people = st.number_input("Number of people affected", 1, 1000000)
        
        priority = st.selectbox("Priority", [
            "CRITICAL",
            "HIGH",
            "MEDIUM",
            "LOW"
        ])
        
        location = st.text_input("Location")
        
        description = st.text_area("Description of need")
        
        if st.button("✅ Report Need"):
            return {
                "need_type": need_type,
                "affected_people": affected_people,
                "priority": priority,
                "location": location,
                "description": description,
                "reported_at": datetime.now().isoformat(),
            }
        
        return None
