import sys, os
import json
import time
import hashlib
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def withdraw(c):
    res = c.post("/player/withdrawfrombank", {"withdraw": 100})
    print(res.get("status") if res else "Fail", end=" ")

def main():
    print("Testing Concurrent Withdraws Result (Race Condition)...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    # ensure clean bank
    c1.post("/player/withdrawfrombank", {"withdraw": 999999})
    time.sleep(1)

    # Deposit exactly 100 gold (91 deposited due to tax)
    c1.post("/player/deposittobank", {"deposit": 100})
    time.sleep(2)
    
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not d1 or "data" not in d1: return
    print("Starting Bank: " + str(d1["data"].get("bank_account_balance")))
    print("Starting Gold: " + str(d1["data"].get("gold")))

    threads = []
    # Send 5 concurrent withdraw requests for 91 gold when we only have 91
    for i in range(5):
        t = threading.Thread(target=withdraw, args=(c1,)) 
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()

    print()
    time.sleep(2)
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if d1 and "data" in d1:
        print("Final Bank: " + str(d1["data"].get("bank_account_balance")))
        print("Final Gold: " + str(d1["data"].get("gold")))

if __name__ == "__main__":
    main()
