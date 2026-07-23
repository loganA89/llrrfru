import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing fill potion vulnerabilities...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("\n[+] Testing fill potion with bypass values")
    res = c1.post("/player/fillpotion", {"amount": -1})
    print("Fill Potion -1:", res)
    time.sleep(2)
    
    res = c1.post("/player/fillpotion", {"amount": 1e5})
    print("Fill Potion 1e5:", res)
    time.sleep(2)

    res = c1.post("/player/fillpotion", {"amount": "0xff"})
    print("Fill Potion Hex:", res)

if __name__ == "__main__":
    main()
