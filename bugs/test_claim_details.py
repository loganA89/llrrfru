import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    res_fb = c1.post("/player/claimfbreward", {})
    print("FB Reward:", res_fb)
    
    res_ig = c1.post("/player/claiminstagramreward", {})
    print("IG Reward:", res_ig)

if __name__ == "__main__":
    main()
