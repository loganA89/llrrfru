import sys, os
import json
import time
import hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Daily Reward/Wheel...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    q_start = c1.q

    print("\n[+] Spinning wheel with old check")
    payload = {"check": hashlib.md5(str(q_start).encode("utf-8")).hexdigest()}
    res = c1.post("/player/turnthewheel", payload)
    print("Wheel Spin 1:", res)
    time.sleep(2)
    
    print("\n[+] Spinning wheel again with same check (Replay)")
    res = c1.post("/player/turnthewheel", payload)
    print("Wheel Spin 2:", res)

if __name__ == "__main__":
    main()
