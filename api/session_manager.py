import json
import os
import requests
import logging

SESSION_FILE = os.path.join(os.path.dirname(__file__), 'session.json')

class SessionManager:
    def __init__(self, config_path='config.json'):
        self.config_path = os.path.join(os.path.dirname(__file__), config_path)
        self.session = requests.Session()
        self.api_base = "https://iran.fruitcraft.ir/"
        self.q = 0
        self.load_config()
        
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.api_base = config.get('api_base', self.api_base)
                
    def load_session(self):
        """Load session cookies and variables from disk."""
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    self.session.cookies.update(data.get('cookies', {}))
                    self.q = data.get('q', 0)
                    logging.info("Session loaded from disk.")
                    return True
                except json.JSONDecodeError:
                    logging.error("Corrupted session.json file.")
        return False

    def save_session(self, q_value=None):
        """Save active session cookies and variables to disk."""
        if q_value is not None:
            self.q = q_value
            
        data = {
            'cookies': self.session.cookies.get_dict(),
            'q': self.q
        }
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
        
        logging.info(f"Attempting to login to {url}...")
        try:
            resp = self.session.post(url, data=payload, headers=headers, timeout=15)
            if resp.status_code == 200:
                resp_json = resp.json()
                if resp_json.get('status') is True:
                    # Extract 'q' (quest count) for future MD5 checks
                    player_id = str(resp_json.get('data', {}).get('id', ''))
                    q_val = 0
                    if 'players_info' in resp_json and player_id in resp_json['players_info']:
                        q_val = resp_json['players_info'][player_id].get('q', 0)
                    elif 'data' in resp_json and 'q' in resp_json['data']:
                        q_val = resp_json['data'].get('q', 0)
                        
                    self.save_session(q_value=q_val)
                    logging.info(f"Login successful. Session established. Player q = {q_val}")
                    return True, resp_json
                else:
                    logging.error(f"Login failed by API: {resp_json}")
            else:
                logging.error(f"HTTP Error during login: {resp.status_code}")
        except Exception as e:
            logging.error(f"Login request failed: {e}")
        return False, None
