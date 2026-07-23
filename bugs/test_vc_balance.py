import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    res = c1.post("/user/getvcbalance/client/iOS/", {})
    print("Balance:", res)

if __name__ == "__main__":
    main()
