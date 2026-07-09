import json
import base64
import hashlib
import urllib.parse as url
import urllib.parse
import requests
import urllib3
import time
import logging
from typing import List, Dict, Optional, Any
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from captcha_solver import CaptchaSolver

# Disable warnings globally since we're interacting with legacy endpoints that may have SSL issues
urllib3.disable_warnings()

class FruitClient:
    def __init__(self, api_base: str = "https://iran.fruitcraft.ir/"):
        self.api_base = api_base.rstrip('/')
        self.session = requests.Session()
        self.session.verify = False  # Ignore SSL errors for legacy game servers
        self.q = 0
        self.udid = None
        self.logger = logging.getLogger("FruitClient")
        self.captcha_solver = CaptchaSolver()

    def _xor_str(self, data: bytes, key: bytes) -> bytes:
        result = bytearray()
        for i in range(len(data)):
            result.append(data[i] ^ key[i % len(key)])
        return bytes(result)

    def encrypt_v2(self, payload_dict: dict) -> str:
        key_str = "mwBSDp1nMhcdCravltVGADXTFx7bN9mr0XMgyDezIJghf65lvXhRdLWrScCk"
        payload_str = json.dumps(payload_dict, separators=(',', ':'))
        edata_b = payload_str.encode('utf-8')
        key_b = key_str.encode('utf-8')
        encrypted = base64.b64encode(self._xor_str(edata_b, key_b))
        return url.quote(encrypted, safe="")

    def decrypt_response(self, encrypted_text: str) -> dict:
        """Decrypt V2 encrypted server response"""
        key = "mwBSDp1nMhcdCravltVGADXTFx7bN9mr0XMgyDezIJghf65lvXhRdLWrScCk"
        try:
            data = base64.b64decode(urllib.parse.unquote(encrypted_text))
            key_bytes = key.encode('utf-8')
            result = bytearray()
            for i in range(len(data)):
                result.append(data[i] ^ key_bytes[i % len(key_bytes)])
            return json.loads(result.decode('utf-8'))
        except Exception as e:
            return {"error": str(e), "raw": encrypted_text}

    def handle_error_backoff(self, error_code: int) -> None:
        """Handle rate-limit and other error backoffs based on known error codes."""
        if error_code == 156:
            self.logger.warning("Error 156 detected. Backing off for 4s...")
            time.sleep(4)
        elif error_code in (124, 184):
            self.logger.warning(f"Error {error_code} detected. Backing off for 2s...")
            time.sleep(2)

    def _handle_captcha(self) -> bool:
        """Fetch, solve, and submit CAPTCHA if required."""
        self.logger.warning("CAPTCHA required. Initiating solver flow.")
        for attempt in range(3):
            try:
                resp = self.session.get(self.api_base + '/bot/getcaptcha', verify=False, timeout=10)
                if resp.status_code == 200:
                    b64_img = resp.text.strip()
                    solution = self.captcha_solver.solve(b64_img)
                    if solution:
                        # submit
                        chal_payload = {'captcha': solution}
                        chal_url = self.api_base + '/bot/challengeresponse'
                        edata_val = self.encrypt_v2(chal_payload)
                        raw_body = f"edata={edata_val}&version=2"
                        headers = {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; FruitClient API Build/QQ3A.200805.001)'
                        }
                        c_resp = self.session.post(chal_url, data=raw_body, headers=headers, timeout=10)
                        if c_resp.status_code == 200:
                            c_dec = self.decrypt_response(c_resp.text)
                            if c_dec and c_dec.get('status'):
                                self.logger.info("CAPTCHA successfully solved.")
                                return True
                            else:
                                self.logger.error(f"CAPTCHA response rejected: {c_dec}")
            except Exception as e:
                self.logger.error(f"Error handling captcha: {e}")
        return False

    def post(self, endpoint: str, payload_dict: dict, retry: int = 0) -> Optional[Dict]:
        """Send an encrypted POST request, handling errors and CAPTCHA automatically."""
        target_url = self.api_base + endpoint
        edata_val = self.encrypt_v2(payload_dict)
        raw_body = f"edata={edata_val}&version=2"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; FruitClient API Build/QQ3A.200805.001)'
        }
        try:
            resp = self.session.post(target_url, data=raw_body, headers=headers, timeout=15)
            if resp.status_code == 200:
                decrypted = self.decrypt_response(resp.text)
                if not decrypted:
                    return None
                    
                # Check CAPTCHA
                data_block = decrypted.get('data')
                if isinstance(data_block, dict) and data_block.get('needs_captcha'):
                    if retry < 3:
                        if self._handle_captcha():
                            return self.post(endpoint, payload_dict, retry + 1)
                    return decrypted
                    
                # Check error backoff
                if not decrypted.get('status') and 'error_code' in decrypted:
                    self.handle_error_backoff(decrypted['error_code'])
                    
                return decrypted
            else:
                self.logger.error(f"HTTP {resp.status_code} on POST {endpoint}")
        except Exception as e:
            self.logger.error(f"Exception on POST {endpoint}: {e}")
        return None

    def login(self, recovery_code: str, udid: str) -> tuple[bool, Optional[Dict]]:
        """Log into the Fruit Craft server using a recovery code and device ID."""
        self.udid = udid
        payload = {
            'udid': udid,
            'restore_key': recovery_code,
            'game_version': '1.10.10755',
            'os_type': 2,
            'device_name': 'FruitClient_Bot',
            'os_version': '10',
            'model': 'FruitClient',
            'store_type': 'myket'
        }
        
        resp_json = self.post('/player/load', payload)
        if resp_json and resp_json.get('status'):
            self.post('/player/comeback', {})
            player_id = str(resp_json.get('data', {}).get('id', ''))
            if 'players_info' in resp_json and player_id in resp_json['players_info']:
                self.q = resp_json['players_info'][player_id].get('q', 0)
            elif 'data' in resp_json and 'q' in resp_json['data']:
                self.q = resp_json['data'].get('q', 0)
            return True, resp_json
        return False, resp_json

    def get_profile(self) -> Optional[Dict]:
        """Fetch the logged-in player's profile data."""
        return self.post('/player/getplayerinfo', {})

    def do_quest(self, card_ids: List[int]) -> Optional[Dict]:
        """Execute a quest sequence with the specified cards."""
        payload = {
            'cards': json.dumps(card_ids),
            'check': hashlib.md5(str(self.q).encode('utf-8')).hexdigest()
        }
        resp = self.post('/battle/quest', payload)
        if resp and resp.get('status') and 'result' in resp:
            self.q += 1
        return resp

    def collect_gold(self) -> Optional[Dict]:
        """Collect gold from the passive mine generator."""
        return self.post('/cards/collectgold', {})

    def scout(self, opponent_id: int) -> Optional[Dict]:
        """Scout a player to preview their defensive power."""
        return self.post('/battle/scout', {'opponent_id': opponent_id})
        
    def battle(self, opponent_id: int, card_ids: List[int], attacks_in_today: int = 1) -> Optional[Dict]:
        """Execute a PvP battle against a specific opponent."""
        payload = {
            'opponent_id': opponent_id,
            'attacks_in_today': attacks_in_today,
            'cards': json.dumps(card_ids),
            'check': hashlib.md5(str(self.q).encode('utf-8')).hexdigest()
        }
        resp = self.post('/battle/battle', payload)
        if resp and resp.get('status') and 'result' in resp:
            self.q += 1
        return resp

    def change_avatar(self, avatar_id: int) -> Optional[Dict]:
        """Change player's avatar icon."""
        payload = {'avatar_id': avatar_id}
        return self.post('/player/setplayerinfo', payload)

    def assign_to_mine(self, cards: List[int]) -> Optional[Dict]:
        """Assign specific cards to Gold Mine (Type 1001)."""
        return self.post('/cards/assign', {'type': 1001, 'cards': json.dumps(cards)})

    def assign_to_offense(self, cards: List[int]) -> Optional[Dict]:
        """Assign specific cards to Offense Ministry (Type 1002)."""
        return self.post('/cards/assign', {'type': 1002, 'cards': json.dumps(cards)})

    def assign_to_defense(self, cards: List[int]) -> Optional[Dict]:
        """Assign specific cards to Defense Ministry (Type 1003)."""
        return self.post('/cards/assign', {'type': 1003, 'cards': json.dumps(cards)})

    def heal_card(self, card_id: int) -> Optional[Dict]:
        """Heal/cooloff a specific card manually."""
        return self.post('/cards/cooloff', {'card_id': card_id})

    def heal_all(self, cards: List[int]) -> List[Optional[Dict]]:
        """Heal multiple cards sequentially, pausing between requests to avoid limits."""
        results = []
        for cid in cards:
            results.append(self.heal_card(cid))
            time.sleep(1)
        return results

    def deposit_to_bank(self, amount: int) -> Optional[Dict]:
        """Deposit gold to the player bank (Note: Incurs a 9% server-side wage tax)."""
        return self.post('/player/deposittobank', {'deposit': amount})

    def withdraw_from_bank(self, amount: int) -> Optional[Dict]:
        """Withdraw gold from the player bank."""
        return self.post('/player/withdrawfrombank', {'withdraw': amount})

    def get_tribe_members(self, tribe_id: int) -> Optional[Dict]:
        """Get members list of a specific tribe."""
        return self.post('/tribe/members', {'tribe_id': tribe_id})

    def donate_tribe(self, amount: int) -> Optional[Dict]:
        """Donate gold from personal wallet to current tribe treasury."""
        return self.post('/tribe/donate', {'player_gold': amount})

    def leave_tribe(self) -> Optional[Dict]:
        """Leave current tribe."""
        return self.post('/tribe/leave', {})

    def join_tribe_request(self, tribe_id: int) -> Optional[Dict]:
        """Send a join request to a targeted tribe."""
        return self.post('/tribe/joinrequest', {'tribe_id': tribe_id})

    def find_tribe(self, query: str) -> Optional[Dict]:
        """Search for a tribe by text query."""
        return self.post('/tribe/find', {'query': query})

    def poke_tribe_member(self, member_id: int) -> Optional[Dict]:
        """Poke a tribe member (Gives them 500 gold passively, zero cost)."""
        return self.post('/tribe/poke', {'member_id': member_id})

    def get_shop_items(self) -> Optional[Dict]:
        """Fetch available shop items and pricing from server."""
        return self.post('/store/getshopitems', {})

    def turn_wheel(self) -> Optional[Dict]:
        """Turn the daily wheel of fortune."""
        payload = {'check': hashlib.md5(str(self.q).encode('utf-8')).hexdigest()}
        return self.post('/player/turnthewheel', payload)

    def claim_ad_reward(self) -> Optional[Dict]:
        """Claim a daily advertisement reward."""
        payload = {'check': hashlib.md5(str(self.q).encode('utf-8')).hexdigest()}
        return self.post('/player/claimadvertismentreward', payload)

    def add_potion(self, amount: int) -> Optional[Dict]:
        """Craft or instantly purchase potions for hero evolution."""
        return self.post('/magic/addpotion', {'amount': amount})

