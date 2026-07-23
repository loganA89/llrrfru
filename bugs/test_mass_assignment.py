import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("Testing Mass Assignment on /player/setplayerinfo...")
    
    payload = {
        "gold": 999999,
        "level": 100,
        "xp": 999999
    }
    res = c1.post("/player/setplayerinfo", payload)
    print("Set info:", res)
    
    time.sleep(2)
    prof = c1.get_profile()
    if prof and "data" in prof:
        print("Gold after:", prof["data"].get("gold"))
        print("Level after:", prof["data"].get("level"))

if __name__ == "__main__":
    main()
