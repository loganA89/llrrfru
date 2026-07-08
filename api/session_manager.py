import json
import os
import requests
import logging

SESSION_FILE = os.path.join(os.path.dirname(__file__), 'session.json')

class SessionManager:
    def __init__(self, config_path='config.json'):
        self.config_path = os.path.join(os.path.dirname(__file__), config_path)
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for legacy endpoints
        self.api_base = "https://iran.fruitcraft.ir/"
        self.load_config()
        
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.api_base = config.get('api_base', self.api_base)
                
    def load_session(self):
        """Load session cookies from disk."""
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    self.session.cookies.update(data.get('cookies', {}))
                    logging.info("Session loaded from disk.")
                    return True
                except json.JSONDecodeError:
                    logging.error("Corrupted session.json file.")
        return False

    def save_session(self):
        """Save active session cookies to disk."""
        data = {'cookies': self.session.cookies.get_dict()}
        with open(SESSION_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info("Session saved to disk.")

    def login(self, recovery_code, udid, game_version='1.10.10755'):
        """Perform a fresh login and store the session tokens."""
        url = self.api_base.rstrip('/') + '/player/load'
        payload = {
            'udid': udid,
            'restore_key': recovery_code,
            'game_version': game_version,
            'os_type': '2',
            'device_name': 'API_Session_Manager'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        logging.info("Attempting to login and acquire session...")
        try:
            resp = self.session.post(url, data=payload, headers=headers, timeout=15)
            if resp.status_code == 200:
                resp_json = resp.json()
                if resp_json.get('status') is True:
                    self.save_session()
                    logging.info("Login successful. Session established.")
                    return True
                else:
                    logging.error(f"Login failed by API: {resp_json.get('error')}")
            else:
                logging.error(f"HTTP Error during login: {resp.status_code}")
        except Exception as e:
            logging.error(f"Login request failed: {e}")
        return False
