import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    c1.login("fact11439memory24", "android_vuln_t1")
    res = c1.post("/battle/getopponents", {})
    print(res)

if __name__ == "__main__":
    main()
