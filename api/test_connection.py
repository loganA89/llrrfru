import json
import uuid
import hashlib
import base64
import requests
import logging
import traceback
import sys
import os
import urllib3

# Setup logging
logging.basicConfig(
    filename='test_log.txt',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def generate_device_id(prefix):
    return prefix + uuid.uuid4().hex[:16]

def xor_encrypt(data, key_hex):
    """
    Encrypts data using XOR with a SHA-512 hex digest, then Base64 encodes it.
    This matches the game's Encryption v2 implementation.
    """
    if not data:
        return ""
    key_bytes = key_hex.encode('utf-8')
    data_bytes = data.encode('utf-8')
    out = bytearray()
    for i in range(len(data_bytes)):
        out.append(data_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return base64.b64encode(out).decode('utf-8')

def get_encryption_key():
    base_string = "wave712sound123pluck394synth449"
    return hashlib.sha512(base_string.encode('utf-8')).hexdigest()

def main():
    try:
        # Load config from the same directory as the script
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config.json: {e}")
        return

    recovery_code = input("Enter recovery code: ").strip()
    if not recovery_code:
        logging.error("No recovery code provided.")
        return

    udid = generate_device_id(config.get('device_id_prefix', 'android_'))
    api_base = config.get('api_base', 'https://iran.fruitcraft.ir/')
    
    # We implement encryption v2 as requested, to demonstrate the logic.
    # The email is typically encrypted, but we'll include the encryption function here
    # to show the V2 cryptography logic implementation.
    enc_key = get_encryption_key()
    
    payload = {
        'udid': udid,
        'device_name': 'API_Test_Device',
        'game_version': config.get('game_version', '1.10.10755'),
        'os_type': '2',
        'os_version': '10',
        'model': 'TestModel_API',
        'restore_key': recovery_code
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; TestModel Build/QQ3A.200805.001)'
    }

    load_url = api_base.rstrip('/') + '/player/load'

    session = requests.Session()
    # SSL handling: Disable warnings and set verify=False to handle generic SSL/TLS certs that game APIs sometimes use
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session.verify = False 

    result = {
        'success': False,
        'url': load_url,
        'status_code': None,
        'response': None,
        'error': None
    }

    logging.info(f"Sending load request to {load_url}...")
    try:
        response = session.post(load_url, data=payload, headers=headers, timeout=15)
        result['status_code'] = response.status_code
        
        if response.status_code == 200:
            try:
                resp_json = response.json()
                # Remove sensitive info from response
                if 'data' in resp_json:
                    if 'restore_key' in resp_json['data']:
                        resp_json['data']['restore_key'] = '***REDACTED***'
                    if 'email' in resp_json['data']:
                        resp_json['data']['email'] = '***REDACTED***'
                    if 'udid' in resp_json['data']:
                        resp_json['data']['udid'] = '***REDACTED***'

                result['response'] = resp_json
                if resp_json.get('status') is True:
                    result['success'] = True
                    logging.info("Successfully loaded profile (read-only)!")
                else:
                    logging.error("API returned status=false")
            except json.JSONDecodeError:
                result['response'] = response.text
                result['error'] = "Invalid JSON response"
                logging.error("Failed to parse JSON response.")
        else:
            result['response'] = response.text
            result['error'] = f"HTTP Error {response.status_code}"
            logging.error(f"HTTP Error {response.status_code}")

    except Exception as e:
        error_str = traceback.format_exc()
        result['error'] = str(e)
        logging.error(f"Request failed: {error_str}")

    result_path = os.path.join(os.path.dirname(__file__), 'test_result.json')
    with open(result_path, 'w') as f:
        json.dump(result, f, indent=4)
        
    logging.info("Saved results to test_result.json (without credentials)")

if __name__ == '__main__':
    main()
