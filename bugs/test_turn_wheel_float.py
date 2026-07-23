import sys, os
import json
import time
import hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Turn Wheel Bypass...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    q_start = c1.q

    # The normal wheel expects nothing but a check. 
    # What if we pass an array to check to see if we can trigger another response?
    payload = {"check": [hashlib.md5(str(q_start).encode("utf-8")).hexdigest()]}
    res = c1.post("/player/turnthewheel", payload)
    print("Wheel Array Check:", res)
    time.sleep(2)

if __name__ == "__main__":
    main()
