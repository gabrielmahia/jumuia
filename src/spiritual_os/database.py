"""
Database Layer - SQLite with persistent storage
Handles all data persistence for nested architecture
"""

import sqlite3
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime

DB_PATH = Path(".data/spiritual_os.db")


class Database:
    """SQLite database for Catholic Spiritual OS"""
    
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()
    
    def init_schema(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                role TEXT NOT NULL,
                parish_id TEXT,
                diocese_id TEXT,
                opt_in_to_parish_aggregates BOOLEAN DEFAULT 0,
                opt_in_to_diocese_aggregates BOOLEAN DEFAULT 0,
                opt_in_to_global_aggregates BOOLEAN DEFAULT 0,
                privacy_level INTEGER DEFAULT 0,
                rule_of_life TEXT,
                journal_entries TEXT,
                sacrament_milestones TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # Parishes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parishes (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                diocese_id TEXT NOT NULL,
                coordinator_id TEXT,
                address TEXT,
                phone TEXT,
                email TEXT,
                bulletin_text TEXT,
                events TEXT,
                volunteer_signups TEXT,
                aggregated_members_count INTEGER DEFAULT 0,
                aggregated_formation_participants INTEGER DEFAULT 0,
                aggregated_avg_practice_minutes REAL DEFAULT 0.0,
                aggregated_sacrament_stats TEXT,
                aggregated_justice_campaigns TEXT,
                aggregated_volunteer_count INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # Dioceses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dioceses (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                bishop_name TEXT,
                region TEXT,
                transparency_priorities TEXT,
                strategic_plan TEXT,
                aggregated_parishes_count INTEGER DEFAULT 0,
                aggregated_total_catholics INTEGER DEFAULT 0,
                aggregated_weekly_attendance INTEGER DEFAULT 0,
                aggregated_formation_participants INTEGER DEFAULT 0,
                aggregated_justice_campaigns TEXT,
                aggregated_workers_helped INTEGER DEFAULT 0,
                aggregated_policy_wins INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # Justice campaigns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS justice_campaigns (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                campaign_type TEXT,
                description TEXT,
                dioceses_joined TEXT,
                parishes_joined_count INTEGER DEFAULT 0,
                aggregated_workers_affected INTEGER DEFAULT 0,
                aggregated_wage_increase_percent REAL DEFAULT 0.0,
                aggregated_income_increase_dollars INTEGER DEFAULT 0,
                aggregated_policy_wins INTEGER DEFAULT 0,
                success_stories TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # Crisis events table (temporary)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crisis_events (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                event_type TEXT,
                location TEXT,
                activated_at TEXT,
                expected_duration_days INTEGER DEFAULT 180,
                affected_dioceses TEXT,
                activated_parishes TEXT,
                volunteers TEXT,
                resources TEXT,
                needs TEXT,
                people_affected INTEGER DEFAULT 0,
                people_receiving_aid INTEGER DEFAULT 0,
                total_funds_raised INTEGER DEFAULT 0,
                auto_delete_date TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # Aggregation logs (for tracking when aggregates were last updated)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aggregation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT,
                entity_id TEXT,
                aggregated_at TEXT,
                computation_time_ms REAL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_user(self, user: 'User') -> bool:
        """Save or update user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user.id,
                user.name,
                user.email,
                user.role.value,
                user.parish_id,
                user.diocese_id,
                user.opt_in_to_parish_aggregates,
                user.opt_in_to_diocese_aggregates,
                user.opt_in_to_global_aggregates,
                user.privacy_level,
                json.dumps(user.rule_of_life),
                json.dumps(user.journal_entries),
                json.dumps(user.sacrament_milestones),
                user.created_at or now,
                now,
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving user: {e}")
            return False
    
    def get_user(self, user_id: str) -> Optional['User']:
        """Get user by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            from src.spiritual_os.models import User, UserRole
            
            return User(
                id=row[0],
                name=row[1],
                email=row[2],
                role=UserRole(row[3]),
                parish_id=row[4],
                diocese_id=row[5],
                opt_in_to_parish_aggregates=bool(row[6]),
                opt_in_to_diocese_aggregates=bool(row[7]),
                opt_in_to_global_aggregates=bool(row[8]),
                privacy_level=row[9],
                rule_of_life=json.loads(row[10]) if row[10] else {},
                journal_entries=json.loads(row[11]) if row[11] else [],
                sacrament_milestones=json.loads(row[12]) if row[12] else [],
                created_at=row[13],
                updated_at=row[14],
            )
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_users_in_parish(self, parish_id: str) -> List['User']:
        """Get all users in a parish"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE parish_id = ?", (parish_id,))
            rows = cursor.fetchall()
            conn.close()
            
            from src.spiritual_os.models import User, UserRole
            
            users = []
            for row in rows:
                users.append(User(
                    id=row[0],
                    name=row[1],
                    email=row[2],
                    role=UserRole(row[3]),
                    parish_id=row[4],
                    diocese_id=row[5],
                    opt_in_to_parish_aggregates=bool(row[6]),
                    opt_in_to_diocese_aggregates=bool(row[7]),
                    opt_in_to_global_aggregates=bool(row[8]),
                    privacy_level=row[9],
                    rule_of_life=json.loads(row[10]) if row[10] else {},
                    journal_entries=json.loads(row[11]) if row[11] else [],
                    sacrament_milestones=json.loads(row[12]) if row[12] else [],
                    created_at=row[13],
                    updated_at=row[14],
                ))
            
            return users
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def save_parish(self, parish: 'Parish') -> bool:
        """Save or update parish"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT OR REPLACE INTO parishes VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
            """, (
                parish.id,
                parish.name,
                parish.diocese_id,
                parish.coordinator_id,
                parish.address,
                parish.phone,
                parish.email,
                parish.bulletin_text,
                json.dumps(parish.events),
                json.dumps(parish.volunteer_signups),
                parish.aggregated_members_count,
                parish.aggregated_formation_participants,
                parish.aggregated_avg_practice_minutes,
                json.dumps(parish.aggregated_sacrament_stats),
                json.dumps(parish.aggregated_justice_campaigns),
                parish.aggregated_volunteer_count,
                parish.created_at or now,
                now,
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving parish: {e}")
            return False
    
    def get_parish(self, parish_id: str) -> Optional['Parish']:
        """Get parish by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM parishes WHERE id = ?", (parish_id,))
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            from src.spiritual_os.models import Parish
            
            return Parish(
                id=row[0],
                name=row[1],
                diocese_id=row[2],
                coordinator_id=row[3],
                address=row[4],
                phone=row[5],
                email=row[6],
                bulletin_text=row[7],
                events=json.loads(row[8]) if row[8] else [],
                volunteer_signups=json.loads(row[9]) if row[9] else [],
                aggregated_members_count=row[10],
                aggregated_formation_participants=row[11],
                aggregated_avg_practice_minutes=row[12],
                aggregated_sacrament_stats=json.loads(row[13]) if row[13] else {},
                aggregated_justice_campaigns=json.loads(row[14]) if row[14] else [],
                aggregated_volunteer_count=row[15],
                created_at=row[16],
                updated_at=row[17],
            )
        except Exception as e:
            print(f"Error getting parish: {e}")
            return None
    
    def cleanup_expired_crises(self) -> int:
        """Delete crisis events past their auto_delete_date"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            cursor.execute(
                "DELETE FROM crisis_events WHERE auto_delete_date < ?",
                (now,)
            )
            
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            return deleted
        except Exception as e:
            print(f"Error cleaning up crises: {e}")
            return 0
