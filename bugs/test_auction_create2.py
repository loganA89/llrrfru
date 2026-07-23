import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    
    # Buy a new card so it is not assigned
    res = c1.post("/store/buycardpack", {"type": 1})
    print("Bought card")
    time.sleep(1)
    
    s2, d2 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    cards = d2.get("data", {}).get("cards", [])
    
    # Find a card that is not in a deck
    for c in cards:
        print("Trying to auction", c["id"])
        res = c1.post("/auction/setcardforauction", {
            "card_id": c["id"],
            "start_price": 100,
            "duration": 12
        })
        print(res)
        time.sleep(1)
        if res and res.get("status"):
            break

if __name__ == "__main__":
    main()
