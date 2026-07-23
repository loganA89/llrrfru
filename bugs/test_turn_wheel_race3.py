import sys, os
import json
import time
import hashlib
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

# Can we race the deposit?

def deposit(c):
    res = c.post("/player/deposittobank", {"deposit": 100})
    print(res.get("status") if res else "Fail", end=" ")

def main():
    print("Testing Concurrent Deposits (Race Condition)...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    # ensure clean bank
    c1.post("/player/withdrawfrombank", {"withdraw": 999999})
    time.sleep(2)

    d1 = c1.get_profile()
    if not d1 or "data" not in d1: return
    print("Starting Bank: " + str(d1["data"].get("bank_account_balance")))
    print("Starting Gold: " + str(d1["data"].get("gold")))

    threads = []
    # Send 5 concurrent deposit requests for 100 gold
    for i in range(5):
        t = threading.Thread(target=deposit, args=(c1,)) 
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()

    print()
    d1 = c1.get_profile()
    if d1 and "data" in d1:
        print("Final Bank: " + str(d1["data"].get("bank_account_balance")))
        print("Final Gold: " + str(d1["data"].get("gold")))

if __name__ == "__main__":
    main()
