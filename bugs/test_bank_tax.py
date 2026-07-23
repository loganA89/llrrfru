import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Bank Tax Bypass...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    # Empty bank
    c1.post("/player/withdrawfrombank", {"withdraw": 999999})
    time.sleep(1)
    
    d = c1.get_profile()["data"]
    start_gold = d.get("gold", 0)
    bank_bal = d.get("bank_account_balance", 0)
    print(f"Starting Gold: {start_gold}, Bank: {bank_bal}")
    
    if start_gold < 200:
        print("Need more gold to test tax.")
        return
        
    print("\n[+] 1. Normal Deposit (100 gold)")
    res = c1.post("/player/deposittobank", {"deposit": 100})
    print("Normal Deposit:", res)
    time.sleep(1)
    
    # Withdraw to reset
    c1.post("/player/withdrawfrombank", {"withdraw": 999999})
    time.sleep(1)

    print("\n[+] 2. Float Deposit (100.5 gold)")
    res = c1.post("/player/deposittobank", {"deposit": 100.5})
    print("Float Deposit:", res)
    time.sleep(1)

    # Withdraw to reset
    c1.post("/player/withdrawfrombank", {"withdraw": 999999})
    time.sleep(1)
    
    print("\n[+] 3. Array Deposit ([100])")
    res = c1.post("/player/deposittobank", {"deposit": [100]})
    print("Array Deposit:", res)

if __name__ == "__main__":
    main()
