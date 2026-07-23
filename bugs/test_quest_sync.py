import sys, os
import json
import time
import hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Quest Sync...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    c1_cards = d1.get("data", {}).get("cards", [])
    if len(c1_cards) < 2: return
    card1 = c1_cards[0]["id"]
    card2 = c1_cards[1]["id"]
    
    print("\n[+] Testing 1 card Quest vs Multi-Card Quest XP")
    q_start = c1.q
    
    # Normally a quest with 1 card gives X XP and Y Gold
    payload1 = {
        "cards": json.dumps([card1]), 
        "check": hashlib.md5(str(q_start).encode("utf-8")).hexdigest()
    }
    res1 = c1.post("/battle/quest", payload1)
    print("Single Card Quest:", res1.get("data", {}).get("gold_added"), "gold,", res1.get("data", {}).get("xp_added"), "XP")
    
    time.sleep(2)
    c1.q += 1
    
    payload2 = {
        "cards": json.dumps([card2, card2, card2, card2, card2]), 
        "check": hashlib.md5(str(c1.q).encode("utf-8")).hexdigest()
    }
    res2 = c1.post("/battle/quest", payload2)
    print("Multi Duplicate Card Quest:", res2.get("data", {}).get("gold_added"), "gold,", res2.get("data", {}).get("xp_added"), "XP")

if __name__ == "__main__":
    main()
