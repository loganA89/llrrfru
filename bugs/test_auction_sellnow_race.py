import sys, os, time, threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def sellnow(c, auc_id):
    res = c.post("/auction/sellnow", {"auction_id": auc_id})
    if res and res.get("status"):
        print("True", end=" ")
    else:
        err = res.get("data", {}).get("code") if res and isinstance(res.get("data"), dict) else "Error"
        print(f"False({err})", end=" ")

def main():
    print("Testing Concurrent Auction SellNow...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    t1_gold = d1["data"].get("gold", 0)
    print("T1 Gold Start:", t1_gold)
    
    # Get active auction ID
    res_auc = c1.post("/auction/loadmyauctions", {})
    auctions = res_auc.get("data", []) if isinstance(res_auc.get("data"), list) else []
    auc_id = None
    for a in auctions:
        if a.get("activity_status") == 1:
            auc_id = a["id"]
            break
            
    if not auc_id:
        print("No active auction.")
        return
        
    print(f"Selling auction {auc_id}...")
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=sellnow, args=(c1, auc_id))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print()
    time.sleep(2)
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    t1_gold_end = d1["data"].get("gold", 0)
    print("T1 Gold End:", t1_gold_end)

if __name__ == "__main__":
    main()
