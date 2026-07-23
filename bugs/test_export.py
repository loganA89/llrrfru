import sys, os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    c1.login("fact11439memory24", "android_vuln_t1")
    
    # Try fetching export json
    res = c1.post("/cards/cardsjsonexport", {"version": "0"})
    print("Cards Export:", type(res), str(res)[:500])

if __name__ == "__main__":
    main()
