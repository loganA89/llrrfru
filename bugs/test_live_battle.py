import sys, os, time, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Live Battle Status Hypothesis...")
    
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    opp_id = int(os.environ.get("TEST_ACC_2_ID", "9999999")) # T2 ID
    
    payload = {"opponent_id": opp_id}
    res = c1.post("/live-battle/livebattle", payload)
    print("\nLive Battle Request against Offline Opponent:", res)

if __name__ == "__main__":
    main()
