import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Session Reuse & Binding...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print(f"Logged in as T1. Passport: {c1.passport[:10]}...")
    
    c2 = FruitClient()
    c2.passport = c1.passport
    
    res = c2.post("/player/getplayerinfo", {})
    if res and res.get("status"):
        print("[!] SUCCESS: Used stolen cookie to fetch profile from a new client instance.")
        print("Name:", res["data"].get("name"))
    else:
        print("[-] FAILED: Cookie reuse blocked.")
        print(res)

if __name__ == "__main__":
    main()
