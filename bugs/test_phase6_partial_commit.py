import sys, os, time, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Regression Test: Partial Failure Commit (Enhance)")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    # Needs 2 cards
    cards = d1.get("data", {}).get("cards", [])
    if len(cards) < 2: return
    
    c_target = cards[0]["id"]
    c_sac1 = cards[1]["id"]
    
    # Submitting valid sacrifice alongside an invalid out-of-bounds integer
    res = c1.post("/cards/enhance", {"card_id": c_target, "sacrifices": json.dumps([c_sac1, 999999999])})
    
    # Will crash (HTML) or reject
    print("Partial Commit Result:", res.get("status") if isinstance(res, dict) else res)
    
    time.sleep(1)
    d2 = c1.get_profile()
    c2_cards = d2.get("data", {}).get("cards", [])
    still_has_sac1 = any(c["id"] == c_sac1 for c in c2_cards)
    print("Valid sacrifice retained?", still_has_sac1)

if __name__ == "__main__":
    main()
