import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Misc Logic...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("\n[+] Check new name")
    d1 = c1.get_profile()
    print("New name:", d1.get("data", {}).get("name"))

if __name__ == "__main__":
    main()
