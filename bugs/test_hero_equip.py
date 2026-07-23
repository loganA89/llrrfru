import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Assign IDOR...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    
    # Can we poke ourselves to get unlimited 500 gold?
    my_id = d1.get("data", {}).get("id")
    print("\n[+] Testing Self Poke")
    res = c1.post("/tribe/poke", {"member_id": my_id})
    print(res)
    time.sleep(2)

    # Can we poke arbitrary people without being in a tribe?
    print("\n[+] Testing Arbitrary Poke")
    res = c1.post("/tribe/poke", {"member_id": int(os.environ.get("TEST_ACC_2_ID", "9999999"))})
    print(res)

if __name__ == "__main__":
    main()
