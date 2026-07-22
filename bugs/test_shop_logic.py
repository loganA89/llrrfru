import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Shop/Economy Logic vulnerabilities...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1:
        print("Login T1 failed")
        return

    gold_start = d1.get("data", {}).get("gold", 0)
    print(f"Starting Gold: {gold_start}")

    print(f"\n--- 1. Testing Negative Pack ID ---")
    res = c1.post("/store/buycardpack", {"type": -1})
    if res and res.get("status"):
        print("[!] VULNERABLE! Accepted negative pack ID.")
    elif res and res.get("raw_html"):
        print("[-] Crashed (HTML)")
    else:
        print("[-] Rejected:", res)

    time.sleep(2)

    print(f"\n--- 2. Testing Float Pack ID (Type Confusion) ---")
    res = c1.post("/store/buycardpack", {"type": 1.5})
    if res and res.get("status"):
        print("[!] VULNERABLE! Accepted float pack ID.")
    elif res and res.get("raw_html"):
        print("[-] Crashed (HTML)")
    else:
        print("[-] Rejected:", res)

    time.sleep(2)
    
    print(f"\n--- 3. Testing Missing Pack ID Parameter ---")
    res = c1.post("/store/buycardpack", {})
    if res and res.get("status"):
        print("[!] VULNERABLE! Accepted empty buy request.")
    elif res and res.get("raw_html"):
        print("[-] Crashed (HTML)")
    else:
        print("[-] Rejected:", res)

if __name__ == "__main__":
    main()
