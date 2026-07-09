import json
import base64
import hashlib
import urllib.parse
import urllib.parse as url
import requests
import urllib3

# Disable warnings globally since we're interacting with legacy endpoints that may have SSL issues
urllib3.disable_warnings()

class FruitClient:
    def __init__(self, api_base="https://iran.fruitcraft.ir/"):
        self.api_base = api_base.rstrip('/')
        self.session = requests.Session()
        self.session.verify = False  # Ignore SSL errors for legacy game servers
        self.q = 0
        self.udid = None

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
            # URL decode, Base64 decode, XOR
            data = base64.b64decode(urllib.parse.unquote(encrypted_text))
            key_bytes = key.encode('utf-8')
            result = bytearray()
            for i in range(len(data)):
                result.append(data[i] ^ key_bytes[i % len(key_bytes)])
            return json.loads(result.decode('utf-8'))
        except Exception as e:
            return {"error": str(e), "raw": encrypted_text}

    def post(self, endpoint, payload_dict):
        target_url = self.api_base + endpoint
        edata_val = self.encrypt_v2(payload_dict)
        raw_body = f"edata={edata_val}&version=2"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; FruitClient API Build/QQ3A.200805.001)'
        }
        resp = self.session.post(target_url, data=raw_body, headers=headers, timeout=15)
        if resp.status_code == 200:
            # Decrypt the response
            return self.decrypt_response(resp.text)
        return None

    def login(self, recovery_code, udid):
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
            # Comeback
            self.post('/player/comeback', {})
            # Update q
            player_id = str(resp_json.get('data', {}).get('id', ''))
            if 'players_info' in resp_json and player_id in resp_json['players_info']:
                self.q = resp_json['players_info'][player_id].get('q', 0)
            elif 'data' in resp_json and 'q' in resp_json['data']:
                self.q = resp_json['data'].get('q', 0)
            return True, resp_json
        return False, resp_json

    def get_profile(self):
        return self.post('/player/getplayerinfo', {})

    def do_quest(self, card_ids):
        payload = {
            'cards': json.dumps(card_ids),
            'check': hashlib.md5(str(self.q).encode('utf-8')).hexdigest()
        }
        resp = self.post('/battle/quest', payload)
        if resp and resp.get('status') and 'result' in resp:
            self.q += 1 # Optimistic update
        return resp

    def collect_gold(self):
        return self.post('/cards/collectgold', {})

    def scout(self, opponent_id):
        return self.post('/battle/scout', {'opponent_id': opponent_id})
        
    def battle(self, opponent_id, card_ids, attacks_in_today=1):
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
