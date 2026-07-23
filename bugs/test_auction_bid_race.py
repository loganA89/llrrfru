import sys, os, time, threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def bid(c, auc_id, amount):
    res = c.post("/auction/bid", {"auction_id": auc_id, "bid_amount": amount})
    if res and res.get("status"):
        print("True", end=" ")
    else:
        err = res.get("data", {}).get("code") if res and isinstance(res.get("data"), dict) else "Error"
        print(f"False({err})", end=" ")

def main():
    print("Testing Concurrent Bids (Race Condition)...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    # Get active auction ID
    res_auc = c1.post("/auction/loadmyauctions", {})
    auctions = res_auc.get("data", []) if isinstance(res_auc.get("data"), list) else []
    auc_id = None
    for a in auctions:
        if a.get("activity_status") == 1:
            auc_id = a["id"]
            max_bid = a["max_bid"]
            break
            
    if not auc_id:
        print("No active auction.")
        return
        
    print(f"Bidding on auction {auc_id} (Current Max: {max_bid}) from T2...")
    
    c2 = FruitClient()
    s2, d2 = c2.login(os.environ.get("TEST_ACC_2_KEY", "REDACTED_KEY_2"), os.environ.get("TEST_ACC_2_UDID", "REDACTED_UDID_2"))
    if not s2: return
    
    t2_gold = d2["data"].get("gold", 0)
    print("T2 Gold Start:", t2_gold)
    
    # We will bid max_bid + 10
    bid_amt = max_bid + 10
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=bid, args=(c2, auc_id, bid_amt))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print()
    time.sleep(2)
    s2, d2 = c2.login(os.environ.get("TEST_ACC_2_KEY", "REDACTED_KEY_2"), os.environ.get("TEST_ACC_2_UDID", "REDACTED_UDID_2"))
    t2_gold_end = d2["data"].get("gold", 0)
    print("T2 Gold End:", t2_gold_end)

if __name__ == "__main__":
    main()
