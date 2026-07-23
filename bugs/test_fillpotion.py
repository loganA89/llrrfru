import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("Testing /player/fillpotion ...")
    
    res = c1.post("/player/fillpotion", {"amount": 0})
    print("Fill 0:", res)

    res = c1.post("/player/fillpotion", {"amount": 0.5})
    print("Fill 0.5:", res)

if __name__ == "__main__":
    main()
