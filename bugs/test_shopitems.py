import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    
    print('Testing getshopitems...')
    # Try with version string
    res = c1.post('/store/getshopitems', {'version': '1.10.10755'})
    print('Result:', res)

if __name__ == '__main__':
    main()
