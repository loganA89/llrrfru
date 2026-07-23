import sys, os, time, requests, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    print('Testing Session Token Binding...')
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    
    passport = c1.session.cookies.get('FRUITPASSPORT')
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; FruitClient API Build/QQ3A.200805.001)',
        'Cookie': 'FRUITPASSPORT=' + passport
    }
    
    raw_body = 'edata=' + c1.encrypt_v2({}) + '&version=2'
    
    time.sleep(2)
    res = requests.post('https://iran.fruitcraft.ir/player/getplayerinfo', data=raw_body, headers=headers, verify=False)
    dec = c1.decrypt_response(res.text)
    
    if dec and 'data' in dec and 'name' in dec['data']:
        print('[!] SUCCESS: Token is valid and Replay possible.')
        print('Name:', dec['data']['name'])
        
        print('\n[+] Testing with different UA')
        headers['User-Agent'] = 'Mozilla/5.0'
        time.sleep(2)
        res2 = requests.post('https://iran.fruitcraft.ir/player/getplayerinfo', data=raw_body, headers=headers, verify=False)
        print('Change UA:', c1.decrypt_response(res2.text).get('status', False))
        
        print('\n[+] Testing with X-Forwarded-For')
        headers['User-Agent'] = 'Dalvik/2.1.0 (Linux; U; Android 10; FruitClient API Build/QQ3A.200805.001)'
        headers['X-Forwarded-For'] = '1.2.3.4'
        time.sleep(2)
        res3 = requests.post('https://iran.fruitcraft.ir/player/getplayerinfo', data=raw_body, headers=headers, verify=False)
        print('X-Forwarded-For:', c1.decrypt_response(res3.text).get('status', False))
    else:
        print('[-] FAILED: Default replay rejected')
        print(dec)

if __name__ == '__main__':
    main()
