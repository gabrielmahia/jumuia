"""
Authentication & Permissions
Simple, privacy-first auth system for nested architecture
"""

import streamlit as st
from typing import Optional, Tuple
import hashlib
import json
from pathlib import Path


class Authentication:
    """Handle user authentication"""
    
    AUTH_FILE = Path(".data/auth.json")
    
    @staticmethod
    def init_auth_system():
        """Initialize authentication system with demo accounts"""
        Authentication.AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        demo_users = {
            "user_001": {
                "name": "John Smith",
                "email": "john@example.com",
                "role": "individual",
                "parish_id": "parish_001",
                "diocese_id": "diocese_001",
                "password_hash": Authentication._hash_password("demo"),
            },
            "coord_001": {
                "name": "Sarah Johnson",
                "email": "sarah@example.com",
                "role": "parish_coordinator",
                "parish_id": "parish_001",
                "diocese_id": "diocese_001",
                "password_hash": Authentication._hash_password("demo"),
            },
            "bishop_001": {
                "name": "Bishop Michael",
                "email": "bishop@example.com",
                "role": "diocesan_leader",
                "parish_id": None,
                "diocese_id": "diocese_001",
                "password_hash": Authentication._hash_password("demo"),
            },
            "global_001": {
                "name": "Justice Network Lead",
                "email": "global@example.com",
                "role": "global_coordinator",
                "parish_id": None,
                "diocese_id": None,
                "password_hash": Authentication._hash_password("demo"),
            },
            "crisis_001": {
                "name": "Crisis Responder",
                "email": "crisis@example.com",
                "role": "crisis_responder",
                "parish_id": "parish_001",
                "diocese_id": "diocese_001",
                "password_hash": Authentication._hash_password("demo"),
            },
        }
        
        if not Authentication.AUTH_FILE.exists():
            with open(Authentication.AUTH_FILE, 'w') as f:
                json.dump(demo_users, f, indent=2)
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password with salt"""
        salt = "catholic_spiritual_os_salt"
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    
    @staticmethod
    def login(email: str, password: str) -> Optional[Tuple[str, dict]]:
        """
        Authenticate user
        Returns: (user_id, user_data) or None
        """
        if not Authentication.AUTH_FILE.exists():
            return None
        
        try:
            with open(Authentication.AUTH_FILE, 'r') as f:
                users = json.load(f)
            
            password_hash = Authentication._hash_password(password)
            
            for user_id, user_data in users.items():
                if user_data.get("email") == email and user_data.get("password_hash") == password_hash:
                    return (user_id, user_data)
            
            return None
        except Exception as e:
            print(f"Auth error: {e}")
            return None
    
    @staticmethod
    def create_user(name: str, email: str, password: str, role: str, 
                   parish_id: Optional[str] = None, 
                   diocese_id: Optional[str] = None) -> Tuple[bool, str]:
        """
        Create new user
        Returns: (success, message)
        """
        if not Authentication.AUTH_FILE.exists():
            Authentication.init_auth_system()
        
        try:
            with open(Authentication.AUTH_FILE, 'r') as f:
                users = json.load(f)
            
            # Check email exists
            for user_data in users.values():
                if user_data.get("email") == email:
                    return (False, "Email already registered")
            
            # Generate user ID
            user_id = f"user_{len(users) + 1:03d}"
            
            # Add new user
            users[user_id] = {
                "name": name,
                "email": email,
                "role": role,
                "parish_id": parish_id,
                "diocese_id": diocese_id,
                "password_hash": Authentication._hash_password(password),
            }
            
            with open(Authentication.AUTH_FILE, 'w') as f:
                json.dump(users, f, indent=2)
            
            return (True, f"User created: {user_id}")
        except Exception as e:
            return (False, f"Error creating user: {e}")
    
    @staticmethod
    def list_demo_accounts() -> dict:
        """List available demo accounts for testing"""
        return {
            "Individual": {"email": "john@example.com", "password": "demo"},
            "Parish Coordinator": {"email": "sarah@example.com", "password": "demo"},
            "Diocesan Leader": {"email": "bishop@example.com", "password": "demo"},
            "Global Coordinator": {"email": "global@example.com", "password": "demo"},
            "Crisis Responder": {"email": "crisis@example.com", "password": "demo"},
        }


class PermissionManager:
    """Manage user permissions and access control"""
    
    @staticmethod
    def can_access_lens(user_role: str, lens: str) -> bool:
        """Check if user can access lens"""
        access_matrix = {
            "individual": ["personal", "parish"],
            "parish_coordinator": ["personal", "parish", "diocese"],
            "diocesan_leader": ["personal", "parish", "diocese", "global"],
            "global_coordinator": ["personal", "parish", "diocese", "global"],
            "crisis_responder": ["crisis", "personal", "parish"],
        }
        
        return lens in access_matrix.get(user_role, [])
    
    @staticmethod
    def can_see_personal_data(viewing_user_role: str, target_user_id: str, 
                             viewing_user_id: str) -> bool:
        """Check if user can see target user's personal data"""
        if viewing_user_role == "individual":
            # Individuals can only see their own data
            return viewing_user_id == target_user_id
        elif viewing_user_role == "parish_coordinator":
            # Coordinators can see aggregates only, not individual data
            return False
        else:
            # Diocesan/Global/Crisis can see aggregates only
            return False
    
    @staticmethod
    def can_edit_parish_data(user_role: str, parish_id: str, user_parish_id: str) -> bool:
        """Check if user can edit parish data"""
        if user_role == "parish_coordinator":
            # Only own parish
            return parish_id == user_parish_id
        elif user_role == "diocesan_leader":
            # Can edit any parish in diocese
            return True
        else:
            return False
    
    @staticmethod
    def can_activate_crisis(user_role: str) -> bool:
        """Check if user can activate crisis mode"""
        return user_role in ["diocesan_leader", "crisis_responder"]
    
    @staticmethod
    def can_view_campaign_details(user_role: str) -> bool:
        """Check if user can see detailed campaign statistics"""
        return user_role in ["diocesan_leader", "global_coordinator"]
    
    @staticmethod
    def get_accessible_parishes(user_role: str, user_parish_id: str, 
                               user_diocese_id: str, all_parishes: list) -> list:
        """Get list of parishes user can see"""
        if user_role == "individual":
            # See their parish only
            return [p for p in all_parishes if p.get("id") == user_parish_id]
        
        elif user_role == "parish_coordinator":
            # See their parish only
            return [p for p in all_parishes if p.get("id") == user_parish_id]
        
        elif user_role == "diocesan_leader":
            # See all parishes in diocese (aggregated)
            return [p for p in all_parishes if p.get("diocese_id") == user_diocese_id]
        
        elif user_role == "global_coordinator":
            # See all parishes
            return all_parishes
        
        else:
            return []
    
    @staticmethod
    def get_accessible_dioceses(user_role: str, user_diocese_id: str, 
                               all_dioceses: list) -> list:
        """Get list of dioceses user can see"""
        if user_role in ["individual", "parish_coordinator"]:
            return []  # Don't see diocese level directly
        
        elif user_role == "diocesan_leader":
            # See only their diocese
            return [d for d in all_dioceses if d.get("id") == user_diocese_id]
        
        elif user_role in ["global_coordinator", "crisis_responder"]:
            # See all dioceses
            return all_dioceses
        
        else:
            return []


def show_login_screen() -> Optional[Tuple[str, dict]]:
    """Display login screen"""
    st.markdown("# ✝️ Catholic Spiritual OS - Login")
    st.write("Choose your role or use demo account credentials below")
    
    st.divider()
    
    # Demo accounts section
    st.subheader("🔑 Demo Accounts (for testing)")
    
    demo_accounts = Authentication.list_demo_accounts()
    
    for role, credentials in demo_accounts.items():
        with st.expander(f"📧 {role}", expanded=False):
            st.write(f"**Email**: `{credentials['email']}`")
            st.write(f"**Password**: `{credentials['password']}`")
    
    st.divider()
    
    # Login form
    st.subheader("🔐 Login")
    
    email = st.text_input("Email", placeholder="john@example.com")
    password = st.text_input("Password", type="password", placeholder="••••••")
    
    if st.button("Login"):
        if email and password:
            result = Authentication.login(email, password)
            if result:
                user_id, user_data = result
                st.success(f"Logged in as {user_data.get('name')}!")
                return (user_id, user_data)
            else:
                st.error("Invalid email or password")
        else:
            st.error("Please enter email and password")
    
    st.divider()
    
    # Create account
    st.subheader("➕ Create Account")
    
    with st.expander("Sign up for an account", expanded=False):
        new_name = st.text_input("Full name")
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        new_role = st.selectbox("Your role", [
            "individual",
            "parish_coordinator",
            "diocesan_leader",
            "global_coordinator",
        ])
        
        if st.button("Create Account"):
            if new_name and new_email and new_password:
                success, message = Authentication.create_user(
                    new_name, new_email, new_password, new_role
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.error("Please fill all fields")
    
    return None
