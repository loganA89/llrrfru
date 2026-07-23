import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Bank Int Bypass...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("\n[+] Testing withdraw JSON string injection")
    # In earlier tests "100.5" caused a crash, "1e2" caused a crash.
    # What about an array withdrawal again, did it withdraw everything?
    c1.post("/player/deposittobank", {"deposit": 100})
    res = c1.post("/player/withdrawfrombank", {"withdraw": [100]})
    print("Withdraw Array:", res)

    print("\n[+] Testing float injection on quest endpoint")
    c1_cards = d1.get("data", {}).get("cards", [])
    if c1_cards:
        c1_target = c1_cards[0]["id"]
        res = c1.post("/battle/quest", {"cards": json.dumps([c1_target + 0.1]), "check": "abc"})
        print("Float Quest ID:", res)

if __name__ == "__main__":
    main()
