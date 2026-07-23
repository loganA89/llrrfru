import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Quest logic...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("\n[+] Quest Array / Object Injection")
    # try sending array of cards
    c1_cards = d1.get("data", {}).get("cards", [])
    if len(c1_cards) > 0:
        c1_target = c1_cards[0]["id"]
        res = c1.post("/battle/quest", {"cards": json.dumps([c1_target, c1_target]), "check": "abc"})
        print("Multiple cards in Quest:", res)
        time.sleep(2)

        res = c1.post("/battle/quest", {"cards": {"$gte": 0}, "check": "abc"})
        print("Object injected Quest:", res)

if __name__ == "__main__":
    main()
