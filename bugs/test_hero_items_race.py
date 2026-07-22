import sys, os
import json
import time
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def buy(c, itm):
    res = c.post("/store/buyheroitem", {"type": itm})
    print(res.get("status") if res else "Fail", end=" ")

def main():
    print("Testing Concurrent Hero Item Buys (Race Condition)...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=buy, args=(c1, 1)) # item 1
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
