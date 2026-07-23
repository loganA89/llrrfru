import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Negative amounts on various endpoints...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("\n[+] Testing Negative Card Cooldown (-1)")
    c1_cards = d1.get("data", {}).get("cards", [])
    if c1_cards:
        c1_target = c1_cards[0]["id"]
        res = c1.post("/cards/cooloff", {"card_id": c1_target, "amount": -1, "cost": -1})
        print("Cooloff:", res)
    else:
        print("No cards.")

    time.sleep(2)
    print("\n[+] Testing Negative Tribe Donate (-100)")
    res = c1.post("/tribe/donate", {"player_gold": -100})
    print("Donate:", res)

    time.sleep(2)
    print("\n[+] Testing Tribe Create with negative name length / ID injection")
    res = c1.post("/tribe/create", {"name": "Test", "description": "Test", "min_level": -10})
    print("Create:", res)

if __name__ == "__main__":
    main()
