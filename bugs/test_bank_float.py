import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Bank Float vulnerability in depth...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("Starting Gold:", d1["data"]["gold"])
    
    res = c1.post("/player/withdrawfrombank", {"withdraw": 999999999})
    time.sleep(2)
    
    d1 = c1.get_profile()
    if not d1.get("status"):
        print("Failed to get profile")
        return
    g = d1["data"].get("gold", 0)
    print(f"\nCurrent Gold: {g}")
    
    # Normally deposit has a 9% wage. 100 gold -> 91 deposited.
    print("\n[+] Testing 100.99 deposit")
    res = c1.post("/player/deposittobank", {"deposit": 100.99})
    print("Deposit Res:", res)
    time.sleep(2)

    d1 = c1.get_profile()
    g2 = d1["data"].get("gold", 0)
    b2 = d1["data"].get("bank_account_balance", 0)
    print(f"Current Gold: {g2}, Bank: {b2}")
    print(f"Spent: {g - g2}, Deposited: {b2}")
    
    print("\n[+] Testing 0.99 deposit (Does it bypass wage or underflow?)")
    res = c1.post("/player/deposittobank", {"deposit": 0.99})
    print("Deposit Res:", res)
    
    time.sleep(2)
    d1 = c1.get_profile()
    g3 = d1["data"].get("gold", 0)
    b3 = d1["data"].get("bank_account_balance", 0)
    print(f"Final Gold: {g3}, Bank: {b3}")

if __name__ == "__main__":
    main()
