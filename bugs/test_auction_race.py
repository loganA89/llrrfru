import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    
    # Buy a new card
    c1.post("/store/buycardpack", {"type": 1})
    time.sleep(2)
    s2, d2 = c1.login("fact11439memory24", "android_vuln_t1")
    cards = d2.get("data", {}).get("cards", [])
    
    c_target2 = cards[-1]["id"]
    
    print(f"Auctioning {c_target2}...")
    res = c1.post("/auction/setcardforauction", {"card_id": c_target2, "start_price": 100, "duration": 12})
    print("Auction:", res)
    
    time.sleep(2)
    res_auc = c1.post("/auction/loadmyauctions", {})
    print("Auctions:", res_auc)

if __name__ == "__main__":
    main()
