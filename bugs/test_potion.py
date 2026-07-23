import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Magic/Potion structural bugs...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("Gold:", d1.get("data", {}).get("gold", 0))

    print("\n[+] Testing adding negative potions")
    res = c1.post("/magic/addpotion", {"amount": -1})
    print(res)
    time.sleep(2)
    
    print("\n[+] Testing adding float potions")
    res = c1.post("/magic/addpotion", {"amount": 1.5})
    print(res)

if __name__ == "__main__":
    main()
