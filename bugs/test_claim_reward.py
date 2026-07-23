import sys, os
import json
import time
import hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Ad/Wheel logic bypasses...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    q_start = c1.q
    print(f"Starting Q: {q_start}")

    print("\n[+] Testing wheel without check param")
    res = c1.post("/player/turnthewheel", {})
    if res and res.get("status"):
        print("Success! (Should require check)")
    else:
        print("Failed (Expected if patched):", res)
        
    time.sleep(2)

    print("\n[+] Testing ad reward with replay check")
    payload = {"check": hashlib.md5(str(q_start).encode("utf-8")).hexdigest()}
    res = c1.post("/player/claimadvertismentreward", payload)
    print("Claim 1:", res)
    time.sleep(2)
    
    res = c1.post("/player/claimadvertismentreward", payload)
    print("Claim 2 (Replay):", res)

if __name__ == "__main__":
    main()
