import sys, os, time, hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Regression Test: Temporal Manipulation (Wheel/Ad)")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    q_start = c1.q
    
    # 1. Inject future timestamps
    payload = {
        "check": hashlib.md5(str(q_start).encode("utf-8")).hexdigest(),
        "timestamp": 2000000000,
        "time": 2000000000,
        "date": "2030-01-01"
    }
    
    res = c1.post("/player/claimadvertismentreward", payload)
    print("Temporal Bypass Result:", res.get("status") if isinstance(res, dict) else res)

if __name__ == "__main__":
    main()
