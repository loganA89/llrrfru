import json
import os
import sys
import base64
import urllib.parse as url
import requests
import logging

SESSION_FILE = os.path.join(os.path.dirname(__file__), 'session.json')

class SessionManager:
    def __init__(self, config_path='config.json'):
        self.config_path = os.path.join(os.path.dirname(__file__), config_path)
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for legacy endpoints
        self.api_base = "https://iran.fruitcraft.ir/"
        self.q = 0
        self.load_config()
        
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.api_base = config.get('api_base', self.api_base)
                
    def load_session(self):
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    self.session.cookies.update(data.get('cookies', {}))
                    self.q = data.get('q', 0)
                    logging.info("Session loaded from disk.")
                    return True
                except json.JSONDecodeError:
                    pass
        return False

    def save_session(self, q_value=None):
        if q_value is not None:
            self.q = q_value
            
        data = {
            'cookies': self.session.cookies.get_dict(),
            'q': self.q
        }
        with open(SESSION_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info("Session saved to disk.")

    def _xor_str(self, edata: bytes, key: bytes) -> bytes:
        key += key * ((len(edata) // len(key)) + 1)
        byteorder = sys.byteorder
        key, var = key[:len(edata)], edata
        int_var = int.from_bytes(var, byteorder)
        int_key = int.from_bytes(key, byteorder)
        int_enc = int_var ^ int_key
        return int_enc.to_bytes(len(var), byteorder)

    def encrypt_v2(self, payload_dict: dict) -> str:
        """Encrypt payload using Fruit Craft V2 logic"""
        key_str = "mwBSDp1nMhcdCravltVGADXTFx7bN9mr0XMgyDezIJghf65lvXhRdLWrScCk"
        payload_str = json.dumps(payload_dict, separators=(',', ':'))
        edata_b = payload_str.encode('utf-8')
        key_b = key_str.encode('utf-8')
        encrypted = base64.b64encode(self._xor_str(edata_b, key_b))
        return url.quote(encrypted, safe="")

    def post_encrypted(self, endpoint, payload_dict):
        """Sends an encrypted POST request to the API."""
        target_url = self.api_base.rstrip('/') + endpoint
        edata_val = self.encrypt_v2(payload_dict)
        raw_body = f"edata={edata_val}&version=2"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; API_Test Build/QQ3A.200805.001)'
        }
        return self.session.post(target_url, data=raw_body, headers=headers, timeout=15)

    def login(self, recovery_code, udid, game_version='1.10.10755'):
        payload = {
            'udid': udid,
            'restore_key': recovery_code,
            'game_version': game_version,
            'os_type': 2,
            'device_name': 'API_Session_Manager',
            'os_version': '10',
            'model': 'TestModel_API',
            'store_type': 'myket'
        }
        
        logging.info(f"Attempting to login to /player/load...")
        try:
            import urllib3
            urllib3.disable_warnings()
            resp = self.post_encrypted('/player/load', payload)
            
            if resp.status_code == 200:
                resp_json = resp.json()
                if resp_json.get('status') is True:
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
                logging.error(f"HTTP Error during login: {resp.status_code} - {resp.text}")
        except Exception as e:
            logging.error(f"Login request failed: {e}")
        return False, None
