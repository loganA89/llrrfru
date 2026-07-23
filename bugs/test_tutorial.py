import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("Testing Tutorial logic...")
    
    prof = c1.get_profile()
    if prof and "data" in prof:
        print("Gold before:", prof["data"].get("gold"))
        print("Level before:", prof["data"].get("level"))
    
    # Send some tutorial IDs
    for idx in range(1, 15):
        res = c1.post("/player/tutorial", {"id": 100 * idx, "index": idx})
        if res and res.get("status"):
            print(f"Tutorial step {idx} accepted")
        else:
            print(f"Tutorial step {idx} failed:", res)
        time.sleep(1)
        
    prof2 = c1.get_profile()
    if prof2 and "data" in prof2:
        print("Gold after:", prof2["data"].get("gold"))
        print("Level after:", prof2["data"].get("level"))

if __name__ == "__main__":
    main()
