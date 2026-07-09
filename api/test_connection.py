import json
import uuid
import logging
import traceback
import os

from session_manager import SessionManager

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

def main():
    sm = SessionManager()

    recovery_code = input("Enter recovery code: ").strip()
    if not recovery_code:
        logging.error("No recovery code provided.")
        return

    udid = generate_device_id('android_')
    
    result = {
        'success': False,
        'login_response': None,
        'profile_response': None,
        'error': None
    }

    logging.info("Step 1: Logging in...")
    try:
        success, resp_json = sm.login(recovery_code, udid)
        if success:
            # Remove sensitive info from response
            if 'data' in resp_json:
                if 'restore_key' in resp_json['data']:
                    resp_json['data']['restore_key'] = '***REDACTED***'
                if 'email' in resp_json['data']:
                    resp_json['data']['email'] = '***REDACTED***'
                if 'udid' in resp_json['data']:
                    resp_json['data']['udid'] = '***REDACTED***'
            result['login_response'] = resp_json

            logging.info("Step 2: Testing profile read access...")
            profile_url = sm.api_base.rstrip('/') + '/player/getplayerinfo'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            # Empty body will fetch logged-in player
            prof_resp = sm.session.post(profile_url, data={}, headers=headers, timeout=15)
            
            if prof_resp.status_code == 200:
                prof_json = prof_resp.json()
                result['profile_response'] = prof_json
                if prof_json.get('status') is True:
                    result['success'] = True
                    logging.info("Successfully read profile!")
                else:
                    logging.error(f"Profile read returned status=false: {prof_json}")
            else:
                logging.error(f"HTTP Error reading profile: {prof_resp.status_code}")
                result['error'] = f"Profile HTTP Error {prof_resp.status_code}"

        else:
            result['error'] = "Login failed"

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
