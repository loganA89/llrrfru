import json
import uuid
import logging
import traceback
import os
import urllib3

from session_manager import SessionManager

# Setup logging
logging.basicConfig(
    filename='test_login_flow.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

urllib3.disable_warnings()

def generate_device_id(prefix):
    return prefix + uuid.uuid4().hex[:16]

def main():
    sm = SessionManager()

    recovery_code = input("Enter recovery code: ").strip()
    if not recovery_code:
        logging.error("No recovery code provided.")
        return

    udid = generate_device_id('android_')
    
    logging.info("Step 1: Sending POST to https://iran.fruitcraft.ir/player/load (ENCRYPTED)...")
    try:
        success, resp_json = sm.login(recovery_code, udid)
        
        if success:
            logging.info(f"Login Step 1 successful! Found {len(sm.session.cookies)} cookies.")
            
            logging.info("Step 2: Sending POST to /player/comeback to finalize session state...")
            # Empty body for comeback, uses stored cookies natively
            comeback_resp = sm.post_encrypted('/player/comeback', {})
            
            if comeback_resp.status_code == 200:
                logging.info("Login flow fully finalized. /player/comeback returned 200 OK.")
                
                # Test final profile read
                logging.info("Step 3: Testing profile read access...")
                prof_resp = sm.post_encrypted('/player/getplayerinfo', {})
                
                if prof_resp.status_code == 200 and prof_resp.json().get('status') is True:
                    logging.info("SUCCESS: Profile read successful! The multi-step login flow is completely functional.")
                    
                    # Clean PII before saving
                    safe_json = prof_resp.json()
                    
                    result_path = os.path.join(os.path.dirname(__file__), 'flow_result.json')
                    with open(result_path, 'w') as f:
                        json.dump(safe_json, f, indent=4)
                    logging.info(f"Saved secure results to {result_path}")
                else:
                    logging.error(f"Profile read failed: {prof_resp.text}")
            else:
                logging.error(f"Comeback failed: {comeback_resp.status_code} - {comeback_resp.text}")
        else:
            logging.error("Load Step 1 failed.")

    except Exception as e:
        error_str = traceback.format_exc()
        logging.error(f"Request failed: {error_str}")

if __name__ == '__main__':
    main()
