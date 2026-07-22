import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing buying item logic (Negative checks)...")
    c1 = FruitClient()
    s1, d1 = c1.login("fact11439memory24", "android_vuln_t1")
    if not s1: return
    
    print("\n[+] 1. Buy avatar pack 1")
    res = c1.post("/store/buyavatarpack", {"type": 1})
    print(res)

if __name__ == "__main__":
    main()
