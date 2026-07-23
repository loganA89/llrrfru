import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Tribe logic bugs...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("\n[+] Testing tribe donate with string")
    res = c1.post("/tribe/donate", {"player_gold": "1e9"})
    print(res)
    time.sleep(2)

    print("\n[+] Testing tribe donate with bool")
    res = c1.post("/tribe/donate", {"player_gold": True})
    print(res)

if __name__ == "__main__":
    main()
