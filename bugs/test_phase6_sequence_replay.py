import sys, os, time, hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Regression Test: Sequence Replay (Combat Hash)")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    q_start = c1.q
    
    cards = d1.get("data", {}).get("cards", [])
    if not cards: return
    c_target = cards[0]["id"]
    
    # 1. Do quest
    payload1 = {
        "cards": str(c_target), 
        "check": hashlib.md5(str(q_start).encode("utf-8")).hexdigest()
    }
    c1.post("/battle/quest", payload1)
    
    # 2. Try same check again immediately
    res = c1.post("/battle/quest", payload1)
    print("Replay Result:", res.get("status") if isinstance(res, dict) else res)
    if isinstance(res, dict) and "data" in res:
        print("Error code:", res["data"].get("code"))

if __name__ == "__main__":
    main()
