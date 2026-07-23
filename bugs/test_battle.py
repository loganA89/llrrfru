import sys, os
import json
import time
import hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Battle Replays and Sync...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    c1_cards = d1.get("data", {}).get("cards", [])
    if not c1_cards: return
    
    q_start = c1.q
    card_id = c1_cards[0]["id"]
    print(f"Starting Q: {q_start}")
    
    print("\n[+] Testing quest with correct check")
    payload = {"cards": str(card_id), "check": hashlib.md5(str(q_start).encode("utf-8")).hexdigest()}
    res = c1.post("/battle/quest", payload)
    print("Quest 1:", res.get("status"))
    time.sleep(2)
    
    print("\n[+] Testing replay attack (using old check on incremented state)")
    payload = {"cards": str(card_id), "check": hashlib.md5(str(q_start).encode("utf-8")).hexdigest()}
    res2 = c1.post("/battle/quest", payload)
    print("Quest 2 (replay):", res2)
    time.sleep(2)

    print("\n[+] Testing quest without check parameter")
    payload = {"cards": str(card_id)}
    res3 = c1.post("/battle/quest", payload)
    print("Quest 3 (no check):", res3)

if __name__ == "__main__":
    main()
