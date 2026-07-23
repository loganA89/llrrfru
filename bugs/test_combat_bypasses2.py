import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient
import hashlib

def main():
    print("Testing combat state anomalies...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    q_start = c1.q
    
    print("\n[+] Quest parameter pollution: Multiple check hashes")
    # Sending check as an array instead of string
    payload = {"cards": "700127207", "check": [hashlib.md5(str(q_start).encode("utf-8")).hexdigest(), "123"]}
    res = c1.post("/battle/quest", payload)
    print("Array check hash:", res)

if __name__ == "__main__":
    main()
