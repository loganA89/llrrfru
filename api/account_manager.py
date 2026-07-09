import json
import os
import time
import uuid
from typing import Dict, Optional

class AccountManager:
    """
    Manages FruitCraft accounts with local JSON storage.
    Extensible for future botting and multi-account capabilities.
    """
    def __init__(self, filename: str = "accounts.json"):
        # Store in the api directory
        self.filepath = os.path.join(os.path.dirname(__file__), filename)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create the JSON file if it doesn't exist."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump({}, f)

    def _load(self) -> Dict[str, dict]:
        """Load account data from JSON."""
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save(self, data: Dict[str, dict]) -> None:
        """Save account data back to JSON."""
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def add_account(self, name: str, recovery_code: str) -> bool:
        """Creates a new account with a random UDID."""
        data = self._load()
        if name in data:
            return False # Account already exists
            
        data[name] = {
            "name": name,
            "recovery_code": recovery_code,
            "udid": "android_" + uuid.uuid4().hex[:16],
            "disabled": False,
            "created_at": int(time.time())
        }
        self._save(data)
        return True

    def edit_account(self, old_name: str, new_name: Optional[str] = None, new_code: Optional[str] = None) -> bool:
        """Update an existing account's name or recovery code."""
        data = self._load()
        if old_name not in data:
            return False
        
        acc = data[old_name]
        
        if new_code:
            acc['recovery_code'] = new_code
            
        if new_name and new_name != old_name:
            if new_name in data:
                return False # Target name already taken
            acc['name'] = new_name
            data[new_name] = acc
            del data[old_name]
            
        self._save(data)
        return True

    def delete_account(self, name: str) -> bool:
        """Delete an account from storage."""
        data = self._load()
        if name in data:
            del data[name]
            self._save(data)
            return True
        return False

    def disable_account(self, name: str) -> bool:
        """Mark an account as disabled."""
        data = self._load()
        if name in data:
            data[name]['disabled'] = True
            self._save(data)
            return True
        return False

    def enable_account(self, name: str) -> bool:
        """Mark an account as active."""
        data = self._load()
        if name in data:
            data[name]['disabled'] = False
            self._save(data)
            return True
        return False

    def list_accounts(self) -> Dict[str, dict]:
        """Return all accounts."""
        return self._load()

    def get_account(self, name: str) -> Optional[dict]:
        """Return a single account by name."""
        return self._load().get(name)
