import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("Logged in")
    res = c1.post("/player/withdrawfrombank", {"withdraw": 99999})
    time.sleep(2)
    
    # After doing post /player/getplayerinfo doesnt return gold in my code setup correctly for get_profile.
    # But /player/load gets full state. Lets do that.
    s2, d2 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if d2 and "data" in d2:
        print("Gold: " + str(d2["data"].get("gold")))
    else:
        print("Fail")
    
if __name__ == "__main__":
    main()
