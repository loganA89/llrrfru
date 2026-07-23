import sys, os, time, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Live Battle Status Hypothesis...")
    
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    opp_id = 9561877 # T2 ID
    
    payload = {"opponent_id": opp_id}
    res = c1.post("/live-battle/livebattle", payload)
    print("\nLive Battle Request against Offline Opponent:", res)

if __name__ == "__main__":
    main()
