import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("Testing In-App Purchase Receipt Validation...")
    
    # Try buying gold pack 1 (usually lowest tier)
    # The Lua client sends: type, amount, receipt, signature
    payload = {
        "type": 1,
        "amount": 1,
        "receipt": "dummy_receipt_12345",
        "signature": "dummy_signature_12345"
    }
    res = c1.post("/store/buygoldpack", payload)
    print("Buy Gold Pack response:", res)
    time.sleep(2)
    
    # Try with missing signature
    payload2 = {
        "type": 1,
        "amount": 1,
        "receipt": "dummy_receipt_12345"
    }
    res2 = c1.post("/store/buygoldpack", payload2)
    print("Buy Gold Pack (no sig):", res2)
    time.sleep(2)
    
    # What about buying a progress bundle?
    res3 = c1.post("/store/buyprogressbundle", {"type": 1, "receipt": "test", "signature": "test"})
    print("Buy Progress Bundle:", res3)

if __name__ == "__main__":
    main()
