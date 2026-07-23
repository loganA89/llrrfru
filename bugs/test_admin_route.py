import sys, os, time, requests, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    
    # Is the API returning 200 OK with the admin login page?
    res = requests.get('https://iran.fruitcraft.ir/player/getplayerinfo', verify=False)
    print(res.status_code)
    print(res.text[:300])

if __name__ == '__main__':
    main()
