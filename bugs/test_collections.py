import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("Testing Collection Spoofing...")
    
    prof = c1.get_profile()
    start_gold = prof["data"].get("gold", 0) if prof and "data" in prof else 0
    print("Starting Gold:", start_gold)
    
    for i in range(1, 10):
        res = c1.post("/cards/collection", {"collection_id": i})
        print(f"Collection {i}:", res.get("status") if res else "Fail")
        time.sleep(1)

    prof2 = c1.get_profile()
    end_gold = prof2["data"].get("gold", 0) if prof2 and "data" in prof2 else 0
    print("Final Gold:", end_gold)

if __name__ == "__main__":
    main()
