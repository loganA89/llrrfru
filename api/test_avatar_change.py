import json
import os
import logging
import urllib3
from session_manager import SessionManager

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def main():
    sm = SessionManager()
    
    # 1. Load Session
    if not sm.load_session():
        logging.error("No active session found in session.json. You must login first.")
        # For testing purposes, we could prompt for login here, but strict flow demands we load it.
        return

    # 2. GET available avatars (In Fruit Craft, basic avatars IDs 1 & 2 are free/default unlocked)
    # Often stored client-side in Data.Avatars.lua. We will pick Avatar ID: 2
    target_avatar_id = 2 
    logging.info(f"Selected target avatar ID: {target_avatar_id}")

    # 3. POST to change avatar
    # Based on naming conventions found in Constants.lua, the endpoint is likely player/setavatar or profile update.
    url = sm.api_base.rstrip('/') + '/player/setavatar'
    payload = {'avatar_id': target_avatar_id}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    result = {
        'success': False,
        'endpoint': url,
        'status_code': None,
        'response': None,
        'error': None
    }

    logging.info(f"Sending POST request to {url} to change avatar...")
    try:
        response = sm.session.post(url, data=payload, headers=headers, timeout=15)
        result['status_code'] = response.status_code
        
        # 4. Verify change
        if response.status_code == 200:
            try:
                resp_json = response.json()
                result['response'] = resp_json
                if resp_json.get('status') is True:
                    result['success'] = True
                    logging.info("Avatar successfully changed!")
                else:
                    logging.warning(f"Avatar change rejected by server: {resp_json}")
            except json.JSONDecodeError:
                result['response'] = response.text
                result['error'] = "Invalid JSON response"
                logging.error("Failed to parse JSON response.")
        elif response.status_code == 404:
            logging.error("Endpoint '/player/setavatar' not found. The API might use a different profile update route.")
            result['error'] = "404 Not Found"
        else:
            result['response'] = response.text
            result['error'] = f"HTTP Error {response.status_code}"
            logging.error(f"HTTP Error {response.status_code}")

    except Exception as e:
        result['error'] = str(e)
        logging.error(f"Request failed: {str(e)}")

    # 5. Save results
    result_path = os.path.join(os.path.dirname(__file__), 'avatar_result.json')
    with open(result_path, 'w') as f:
        json.dump(result, f, indent=4)
    logging.info(f"Saved results to {result_path}")

if __name__ == '__main__':
    main()
