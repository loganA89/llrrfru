import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Bank Int Bypass / Underflow / Overflow...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("\n[+] Testing String bypass (forcing Zend to evaluate it weirdly)")
    res = c1.post("/player/withdrawfrombank", {"withdraw": "-100"})
    print("Withdraw -100 string:", res)
    time.sleep(2)
    
    res = c1.post("/player/withdrawfrombank", {"withdraw": "100.5"})
    print("Withdraw 100.5 string:", res)
    time.sleep(2)

    res = c1.post("/player/withdrawfrombank", {"withdraw": "1e9"})
    print("Withdraw 1e9:", res)
    time.sleep(2)
    
    print("\n[+] Testing MaxInt")
    res = c1.post("/player/deposittobank", {"deposit": 2147483647})
    print("Deposit MaxInt:", res)

if __name__ == "__main__":
    main()
