import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Live Battle Offline Target...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    res = c1.post("/live-battle/livebattle", {"opponent_id": 9561877})
    print("Live Battle Request against offline target:", res)

if __name__ == "__main__":
    main()
