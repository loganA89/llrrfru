import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Bank Logic vulnerabilities...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1:
        print("Login T1 failed")
        return

    print(f"\n--- 1. Testing Float Deposit (Type Confusion) ---")
    res = c1.post("/player/deposittobank", {"deposit": 10.5})
    if res and res.get("status"):
        print("[!] Accepted float deposit:", res)
    elif res and res.get("raw_html"):
        print("[-] Crashed (HTML)")
    else:
        print("[-] Rejected:", res)

    time.sleep(2)

    print(f"\n--- 2. Testing Negative Withdraw ---")
    res = c1.post("/player/withdrawfrombank", {"withdraw": -100})
    if res and res.get("status"):
        print("[!] Accepted negative withdraw:", res)
    elif res and res.get("raw_html"):
        print("[-] Crashed (HTML)")
    else:
        print("[-] Rejected:", res)

    time.sleep(2)

    print(f"\n--- 3. Testing Missing Deposit Parameter ---")
    res = c1.post("/player/deposittobank", {})
    if res and res.get("status"):
        print("[!] Accepted empty deposit:", res)
    elif res and res.get("raw_html"):
        print("[-] Crashed (HTML) - likely unhandled missing parameter.")
    else:
        print("[-] Rejected:", res)

if __name__ == "__main__":
    main()
