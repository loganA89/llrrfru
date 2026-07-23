import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Bank Logic Flaws...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    # Empty bank
    c1.post("/player/withdrawfrombank", {"withdraw": 999999})
    time.sleep(1)
    
    c1.post("/player/deposittobank", {"deposit": 100})
    time.sleep(2)

    d = c1.get_profile()
    if not d or "data" not in d: return
    
    b_bal = str(d["data"].get("bank_account_balance"))
    print("Bank: " + b_bal)
    
    print("\n[+] Testing withdraw JSON array")
    # If we pass an array to withdraw, does it withdraw EVERYTHING instead of just the requested amount?
    res = c1.post("/player/withdrawfrombank", {"withdraw": [1]})
    print("Withdraw Array [1]: " + str(res))

if __name__ == "__main__":
    main()
