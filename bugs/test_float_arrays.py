import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing structural Array Length Bypasses...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return

    c1_cards = d1.get("data", {}).get("cards", [])
    if len(c1_cards) < 2:
        c1.buy_card_pack(1)
        d1 = c1.get_profile()
        c1_cards = d1.get("data", {}).get("cards", [])

    if len(c1_cards) < 2: return

    c1_target = c1_cards[0]["id"]
    c1_sac = c1_cards[1]["id"]

    print("\n[+] 1. Testing Float Card IDs in arrays")
    res = c1.post("/cards/enhance", {"card_id": c1_target, "sacrifices": json.dumps([c1_sac + 0.5])})
    print(res)
    time.sleep(2)

    print("\n[+] 2. Testing extremely large arrays (DoS / Buffer limits)")
    large_arr = [c1_sac] * 10000
    res = c1.post("/cards/enhance", {"card_id": c1_target, "sacrifices": json.dumps(large_arr)})
    if res and res.get("raw_html"):
        print("Crashed HTML")
    else:
        print(res)

if __name__ == "__main__":
    main()
