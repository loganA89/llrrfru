import json
import uuid
import requests
import logging
import traceback
import os

from session_manager import SessionManager

logging.basicConfig(
    filename='test_login_flow.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def generate_device_id(prefix):
    return prefix + uuid.uuid4().hex[:16]

def main():
    sm = SessionManager()

    recovery_code = input("Enter recovery code: ").strip()
    if not recovery_code:
        logging.error("No recovery code provided.")
        return

    udid = generate_device_id('android_')
    
    # Notice the change here. In older scripts / decompiled code, sometimes /player/load 
    # required extra sequential API hits to truly "complete" the session state.
    # We will replicate the exact flow seen in `exampleFr/OldScripts/.../session.py`.
    
    payload = {
        'udid': udid,
        'restore_key': recovery_code,
        'game_version': sm.config.get('game_version', '1.10.10755') if hasattr(sm, 'config') else '1.10.10755',
        'os_type': '2',
        'device_name': 'API_Test_Flow',
        'os_version': '10',
        'model': 'TestModel_API',
        'store_type': 'myket'
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    load_url = sm.api_base.rstrip('/') + '/player/load'

    logging.info(f"Step 1: Sending POST to {load_url}...")
    try:
        resp = sm.session.post(load_url, data=payload, headers=headers, timeout=15)
        
        if resp.status_code == 200:
            try:
                resp_json = resp.json()
            except:
                logging.error(f"Failed to parse JSON. Response text: {resp.text}")
                return

            if resp_json.get('status') is True:
                logging.info(f"Login Step 1 successful! Found {len(sm.session.cookies)} cookies.")
                
                # Step 2: In the old API logic and in `main.lua` / `Scenes.Loading.lua`
                # The client fires several sync endpoints right after /player/load.
                # If these aren't fired, the session might drop or remain fully uninitialized.
                # Let's fire /player/comeback to finalize session sync.
                
                comeback_url = sm.api_base.rstrip('/') + '/player/comeback'
                logging.info(f"Step 2: Sending POST to {comeback_url} to finalize session state...")
                
                # Empty body for comeback, uses stored cookies natively
                comeback_resp = sm.session.post(comeback_url, data={}, headers=headers, timeout=15)
                
                if comeback_resp.status_code == 200:
                    logging.info("Login flow fully finalized. /player/comeback returned 200 OK.")
                    
                    # Test final profile read
                    logging.info("Step 3: Testing profile read access...")
                    profile_url = sm.api_base.rstrip('/') + '/player/getplayerinfo'
                    prof_resp = sm.session.post(profile_url, data={}, headers=headers, timeout=15)
                    
                    if prof_resp.status_code == 200 and prof_resp.json().get('status') is True:
                        logging.info("SUCCESS: Profile read successful! The multi-step login flow is completely functional.")
                        
                        # Save result
                        result_path = os.path.join(os.path.dirname(__file__), 'flow_result.json')
                        safe_json = prof_resp.json()
                        with open(result_path, 'w') as f:
                            json.dump(safe_json, f, indent=4)
                    else:
                        logging.error(f"Profile read failed: {prof_resp.text}")
                else:
                    logging.error(f"Comeback failed: {comeback_resp.status_code} - {comeback_resp.text}")
            else:
                logging.error(f"Load Step 1 failed: {resp_json}")
        else:
            logging.error(f"HTTP Error: {resp.status_code} - {resp.text}")

    except Exception as e:
        error_str = traceback.format_exc()
        logging.error(f"Request failed: {error_str}")

if __name__ == '__main__':
    main()
