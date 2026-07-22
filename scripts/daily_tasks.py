import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def run_daily_tasks(recovery_code, udid):
    print("\n[+] Running daily tasks for account (Recovery: " + recovery_code + ")")
    client = FruitClient()
    success, resp = client.login(recovery_code, udid)
    if not success:
        print("[-] Login failed.")
        return

    player_name = str(resp.get("data", {}).get("name", "Unknown"))
    print("[+] Logged in as: " + player_name)

    print("[*] Collecting gold from mine...")
    res = client.collect_gold()
    if res and res.get("status"):
        val = str(res.get("data", {}).get("player_gold"))
        print("  -> Collected gold! New balance: " + val)
    else:
        print("  -> No gold to collect or failed.")
    time.sleep(1)

    print("[*] Turning the wheel...")
    res = client.turn_wheel()
    if res and res.get("status"):
        val = str(res.get("data", {}).get("reward_type"))
        print("  -> Wheel turned! Reward: " + val)
    else:
        print("  -> Wheel turn failed or already turned.")
    time.sleep(1)

    print("[*] Claiming ad reward...")
    res = client.claim_ad_reward()
    if res and res.get("status"):
        val = str(res.get("data", {}).get("amount"))
        print("  -> Ad reward claimed! Amount: " + val)
    else:
        print("  -> Ad reward failed or already claimed.")
    
    print("[+] Daily tasks completed for " + player_name)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        run_daily_tasks(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python daily_tasks.py <recovery_code> <udid>")
