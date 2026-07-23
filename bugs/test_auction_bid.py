import sys, os, time, threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient() # T1
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    c1_cards = d1["data"].get("cards", [])
    if len(c1_cards) > 0:
        c_target = c1_cards[0]["id"]
        print(f"T1 Auctioning card {c_target}...")
        res = c1.post("/auction/setcardforauction", {"card_id": c_target, "start_price": 100, "duration": 12})
        print("Auction create:", res)

if __name__ == "__main__":
    main()
