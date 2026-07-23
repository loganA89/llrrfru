import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("Testing Multiple Assignments...")
    
    cards = d1.get("data", {}).get("cards", [])
    if len(cards) == 0: return
    card1 = cards[0]["id"]
    
    # Try assigning card1 twice to the mine
    print(f"\n[+] Assigning {card1} twice to Gold Mine (1001)")
    res = c1.post("/cards/assign", {"type": 1001, "cards": json.dumps([card1, card1])})
    print("Assign duplicate:", res)
    time.sleep(2)
    
    # Try assigning card1 to multiple ministries at once? The API takes one type per request.
    print(f"\n[+] Assigning {card1} to Gold Mine (1001) and then Offense (1002)")
    c1.post("/cards/assign", {"type": 1001, "cards": json.dumps([card1])})
    time.sleep(2)
    res2 = c1.post("/cards/assign", {"type": 1002, "cards": json.dumps([card1])})
    print("Assign cross-ministry:", res2)
    time.sleep(2)
    
    # Check if the card is assigned to both
    d1 = c1.get_profile()
    c = next((x for x in d1["data"]["cards"] if x["id"] == card1), None)
    print("Card state:", c)

if __name__ == "__main__":
    main()
