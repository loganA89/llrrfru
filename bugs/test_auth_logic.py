import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Invite Logic Bypass...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    # Can we accept invite for another player?
    print("\n[+] Accepting invite for another player")
    res = c1.post("/tribe/decideinvite", {"invite_id": 999999, "accept": True})
    print("Invite Acceptance:", res)
    
if __name__ == "__main__":
    main()
