import sys, os
import json
import time
import hashlib
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def spin(c, q):
    payload = {"check": hashlib.md5(str(q).encode("utf-8")).hexdigest()}
    res = c.post("/player/turnthewheel", payload)
    print(res.get("status") if res else "Fail", end=" ")

def main():
    print("Testing Concurrent Wheel Spins (Race Condition)...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    q_start = c1.q
    
    threads = []
    # Send 5 concurrent spin requests
    for i in range(5):
        t = threading.Thread(target=spin, args=(c1, q_start)) 
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
