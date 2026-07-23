import sys, os, time, requests, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    print('Testing WAF/IP headers...')
    c1 = FruitClient()
    s1, d1 = c1.login('fact11439memory24', 'android_vuln_t1')
    if not s1: return
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; FruitClient API Build/QQ3A.200805.001)',
        'Cookie': 'FRUITPASSPORT=' + c1.passport,
        'X-Forwarded-For': '8.8.8.8',
    }
    
    raw_body = 'edata=' + c1.encrypt_v2({}) + '&version=2'
    
    res = requests.post('https://iran.fruitcraft.ir/player/getplayerinfo', data=raw_body, headers=headers, verify=False)
    dec = c1.decrypt_response(res.text)
    
    print('With X-Forwarded-For:', dec.get('status') if isinstance(dec, dict) else dec)
    
    headers.pop('X-Forwarded-For')
    res2 = requests.post('https://iran.fruitcraft.ir/player/getplayerinfo', data=raw_body, headers=headers, verify=False)
    dec2 = c1.decrypt_response(res2.text)
    print('Without X-Forwarded-For:', dec2.get('status') if isinstance(dec2, dict) else dec2)

if __name__ == '__main__':
    main()
