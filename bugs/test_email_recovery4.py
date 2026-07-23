import sys, os, time, requests, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    print('Testing Set Email Bypass...')
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    # Try array injection on new_email
    res = c1.post('/player/setemail', {'new_email': ['test@test.com']})
    print('SetEmail Array:', res)

    # What if we pass boolean true?
    res2 = c1.post('/player/setemail', {'new_email': True})
    print('SetEmail Bool:', res2)

if __name__ == '__main__':
    main()
