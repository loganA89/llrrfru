import sys, os
import json
import time
import hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Ad Reward Replay...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    q_start = c1.q
    print(f"Starting Q: {q_start}")

    print("\n[+] Looping ad reward with SAME check")
    payload = {"check": hashlib.md5(str(q_start).encode("utf-8")).hexdigest()}
    
    for i in range(10):
        res = c1.post("/player/claimadvertismentreward", payload)
        if res and res.get("status"):
            added = res.get("data", {}).get("added_gold")
            total = res.get("data", {}).get("gold")
            print(f"[{i+1}] Success: +{added} gold | Total: {total}")
        else:
            print(f"[{i+1}] Failed / Limited:", res)
        time.sleep(1.5)

if __name__ == "__main__":
    main()
