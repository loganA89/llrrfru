import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Negative Bank Limits...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("\n[+] Checking gold Before")
    d1 = c1.get_profile()
    if d1 and "data" in d1:
        print("Bank: " + str(d1["data"].get("bank_account_balance")))
        print("Gold: " + str(d1["data"].get("gold")))

    # Empty bank to sync it
    c1.post("/player/withdrawfrombank", {"withdraw": 999999})
    time.sleep(1)

    print("\n[+] Testing JSON Boolean injection")
    res = c1.post("/player/deposittobank", {"deposit": True})
    print("Deposit True:", res)
    time.sleep(1)
    
    res = c1.post("/player/withdrawfrombank", {"withdraw": True})
    print("Withdraw True:", res)
    time.sleep(1)

    print("\n[+] Checking gold After")
    d1 = c1.get_profile()
    if d1 and "data" in d1:
        print("Bank: " + str(d1["data"].get("bank_account_balance")))
        print("Gold: " + str(d1["data"].get("gold")))

if __name__ == "__main__":
    main()
