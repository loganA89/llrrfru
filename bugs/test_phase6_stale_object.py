import sys, os, time, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Regression Test: Stale Object Reuse (Auction vs Assigned)")
    c1 = FruitClient()
    # REDACTED ACCOUNT
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    # 1. Buy a card
    c1.post("/store/buycardpack", {"type": 1})
    time.sleep(1)
    
    d1 = c1.get_profile()
    cards = d1.get("data", {}).get("cards", [])
    if not cards: return
    target_card = cards[-1]["id"]
    
    # 2. Assign to Gold Mine
    c1.post("/cards/assign", {"type": 1001, "cards": json.dumps([target_card])})
    time.sleep(1)
    
    # 3. Try to auction it
    res_auc = c1.post("/auction/setcardforauction", {"card_id": target_card, "start_price": 100, "duration": 12})
    print("Auctioning Assigned Card Result:", res_auc.get("status") if isinstance(res_auc, dict) else res_auc)

if __name__ == "__main__":
    main()
