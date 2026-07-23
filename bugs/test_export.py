import sys, os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    
    # Try fetching export json
    res = c1.post("/cards/cardsjsonexport", {"version": "0"})
    print("Cards Export:", type(res), str(res)[:500])

if __name__ == "__main__":
    main()
