import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Assign IDOR...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    
    # Can we poke ourselves to get unlimited 500 gold?
    my_id = d1.get("data", {}).get("id")
    print("\n[+] Testing Self Poke")
    res = c1.post("/tribe/poke", {"member_id": my_id})
    print(res)
    time.sleep(2)

    # Can we poke arbitrary people without being in a tribe?
    print("\n[+] Testing Arbitrary Poke")
    res = c1.post("/tribe/poke", {"member_id": 9561877})
    print(res)

if __name__ == "__main__":
    main()
