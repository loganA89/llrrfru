import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c2 = FruitClient()
    s2, d2 = c2.login("skirt11437fire14", "android_vuln_t2") # T2
    
    t_res = c2.post("/tribe/find", {"query": "test"})
    print("Find:", t_res)

if __name__ == "__main__":
    main()
