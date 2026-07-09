import json
import os
import logging
import hashlib
from session_manager import SessionManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def main():
    sm = SessionManager()
    
    # 1. Load Session
    if not sm.load_session():
        logging.error("No active session found in session.json. You must login first via test_connection.py.")
        return

    # 2. GET available avatars
    # In Fruit Craft, basic avatars IDs 1 & 2 are free/default unlocked. We will pick Avatar ID 2.
    target_avatar_id = 2 
    logging.info(f"Selected target avatar ID: {target_avatar_id}")

    # 3. POST to change avatar
    # From decompiled code, changing the avatar uses the generic /player/setplayerinfo route.
    url = sm.api_base.rstrip('/') + '/player/setplayerinfo'
    
    # The Lua code sets body = { avatar_id = A0_16 }
    payload = {'avatar_id': target_avatar_id}
    
    # MD5 check for operation validation, using the extracted 'q' parameter
    payload['check'] = hashlib.md5(str(sm.q).encode('utf-8')).hexdigest()
    
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
            logging.error(f"Endpoint '{url}' not found.")
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
