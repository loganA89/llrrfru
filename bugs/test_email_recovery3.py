import sys, os, time, requests, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    print('Testing Restore Key / Password Logic...')
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    # Can we fetch our own restore key? Yes it's returned on login.
    # What if we ask the server to change it?
    print('\n[+] Attempting to inject new restore key')
    res = c1.post('/player/setplayerinfo', {'restore_key': 'hacked1234567'})
    print('SetPlayerInfo (restore_key):', res)
    
    time.sleep(2)
    # Does the old one still work?
    c2 = FruitClient()
    s2, d2 = c2.login('hacked1234567', os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if s2 and d2.get('data', {}).get('name') == 'test/bin/bash001':
        print('[!] SUCCESS! Restore Key changed via setplayerinfo')
    else:
        print('[-] FAILED. Server ignored restore_key update.')

if __name__ == '__main__':
    main()
