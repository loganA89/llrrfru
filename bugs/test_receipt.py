import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    print("\n[+] Testing IAP logic")
    payload = {
        "type": 130,
        "amount": 1,
        "receipt": "dummy_receipt_12345",
        "signature": "dummy_signature_12345"
    }
    res = c1.post("/store/buygoldpack", payload)
    print("Buy Gold Pack (dummy sig):", res)
    
    payload2 = {
        "type": 130,
        "amount": 1,
    }
    res2 = c1.post("/store/buygoldpack", payload2)
    print("Buy Gold Pack (no sig):", res2)

if __name__ == "__main__":
    main()
