import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("\n[+] Testing IAP logic with SKU")
    payload = {
        "type": "com.tod.fruitcraft.gold1_t_g1",
        "amount": 1,
        "receipt": "dummy_receipt",
        "signature": "dummy_signature"
    }
    res = c1.post("/store/buygoldpack", payload)
    print("Buy Gold Pack (SKU):", res)

if __name__ == "__main__":
    main()
