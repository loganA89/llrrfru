import sys, os
import json
import hashlib
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("Testing attacks_in_today parameter trust...")
    
    c1_cards = d1.get("data", {}).get("cards", [])
    if not c1_cards: return
    card_id = c1_cards[0]["id"]
    
    opp_res = c1.post("/battle/getopponents", {})
    if not opp_res or not opp_res.get("status"):
        print("Could not fetch opponents:", opp_res)
        # Maybe use a hardcoded opponent from previous tests if it fails
        opp_id = 9563332 # ♠️FIGHTER♠️
    else:
        opponents = opp_res["data"]["players"]
        if not opponents:
            print("No opponents found")
            return
        opp_id = opponents[0]["id"]
        
    print(f"Found opponent: {opp_id}")
    
    # Attack with attacks_in_today = -1
    for att in [-1, "0", 1, 1000]:
        q = c1.q
        payload = {
            "opponent_id": opp_id,
            "attacks_in_today": att,
            "cards": json.dumps([card_id]),
            "check": hashlib.md5(str(q).encode("utf-8")).hexdigest()
        }
        res = c1.post("/battle/battle", payload)
        if res and res.get("status"):
            print(f"Attack with attacks_in_today={att}: Success (Result: {res[data].get(result)})")
            c1.q += 1
        else:
            print(f"Attack with attacks_in_today={att}: Failed/Rejected ->", res)
        time.sleep(2)

if __name__ == "__main__":
    main()
