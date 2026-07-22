import sys, os
import json
import time
import hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Quest Bypass...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    q_start = c1.q

    c1_cards = d1.get("data", {}).get("cards", [])
    if c1_cards:
        c1_target = c1_cards[0]["id"]
        # Quest expects a string of card ids comma separated
        # what if we send boolean True?
        payload = {"cards": True, "check": hashlib.md5(str(q_start).encode("utf-8")).hexdigest()}
        res = c1.post("/battle/quest", payload)
        print("Quest True:", res)
        time.sleep(2)

if __name__ == "__main__":
    main()
