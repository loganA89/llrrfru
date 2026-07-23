import sys, os, time, requests, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login('fact11439memory24', 'android_vuln_t1')
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; FruitClient API Build/QQ3A.200805.001)',
        'Cookie': 'FRUITPASSPORT=' + c1.passport
    }
    raw_body = 'edata=' + c1.encrypt_v2({}) + '&version=2'
    
    res = requests.post('https://iran.fruitcraft.ir/player/getplayerinfo', data=raw_body, headers=headers, verify=False)
    print(res.text[:200])

if __name__ == '__main__':
    main()
