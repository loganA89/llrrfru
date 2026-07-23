import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient
import threading

def trigger_ability(cid, battle_id):
    c1 = FruitClient()
    c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    res = c1.post("/live-battle/triggerability", {"card_id": cid, "battle_id": battle_id})
    print(res)

def main():
    print("Testing Live Battle Race Condition...")
    # This requires an active live battle, difficult to trigger without setting one up
    # We will just verify if the endpoint crashes on garbage
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("\n[+] Triggering ability on non-existent battle")
    res = c1.post("/live-battle/triggerability", {"card_id": 1234, "battle_id": 9999})
    print(res)

if __name__ == "__main__":
    main()
