import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    cards = d1.get("data", {}).get("cards", [])
    if not cards: return
    
    c_target = cards[0]["id"]
    
    print("\n[+] Assigning card to type 1000 (invalid)")
    res = c1.post("/cards/assign", {"type": 1000, "cards": json.dumps([c_target])})
    print(res)

if __name__ == "__main__":
    main()
