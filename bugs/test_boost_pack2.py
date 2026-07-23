import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("Testing Boost Pack Purchases...")
    
    # Try buying boost pack 1 with nectar = True
    print("\n[+] Buying Boost Pack 1 (with_nectar = true)")
    res = c1.post("/store/buyboostpack", {"type": 1, "with_nectar": True})
    print("Boost Pack:", res)

if __name__ == "__main__":
    main()
