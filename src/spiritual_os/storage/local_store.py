"""
Storage Module - Privacy-first local file storage
"""

import json
from pathlib import Path
from typing import Any, Optional
from datetime import datetime


class LocalStore:
    """File-based storage for privacy-first data (LOCAL ONLY)"""
    
    def __init__(self, data_dir: str = ".data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.user_dir = self.data_dir / "user"
        self.user_dir.mkdir(exist_ok=True)
    
    def save_user_data(self, user_id: str, key: str, data: dict) -> bool:
        """Save user-specific data locally"""
        try:
            filepath = self.user_dir / f"{user_id}_{key}.json"
            # Add timestamp
            data_with_ts = {
                **data,
                "_saved_at": datetime.now().isoformat()
            }
            with open(filepath, "w") as f:
                json.dump(data_with_ts, f, indent=2)
            return True
        except Exception as e:
            print(f"Storage error: {e}")
            return False
    
    def load_user_data(self, user_id: str, key: str) -> Optional[dict]:
        """Load user-specific data from local storage"""
        try:
            filepath = self.user_dir / f"{user_id}_{key}.json"
            if not filepath.exists():
                return None
            with open(filepath, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Load error: {e}")
            return None
    
    def delete_user_data(self, user_id: str, key: str) -> bool:
        """Delete user data locally"""
        try:
            filepath = self.user_dir / f"{user_id}_{key}.json"
            if filepath.exists():
                filepath.unlink()
            return True
        except Exception as e:
            print(f"Delete error: {e}")
            return False
    
    def list_user_files(self, user_id: str) -> list:
        """List all files for a user"""
        return [f.name for f in self.user_dir.glob(f"{user_id}_*")]


# Demo/test storage using Streamlit session state
class SessionStore:
    """In-memory storage for demo (resets on page refresh)"""
    
    def __init__(self):
        self.data = {}
    
    def save(self, key: str, value: Any):
        """Save to session"""
        self.data[key] = value
    
    def load(self, key: str) -> Optional[Any]:
        """Load from session"""
        return self.data.get(key)


# Privacy notice
PRIVACY_NOTICE = """
🔒 **Privacy First**

All data is:
- Stored locally on your device
- Never sent to external servers
- Yours to control
- Encrypted by design

Spiritual formation is personal. This tool respects that privacy.
"""
