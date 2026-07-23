import sys, os, time, uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login("", "android_" + uuid.uuid4().hex[:16])
    if s1:
        print("New code:", d1["data"].get("restore_key"))

if __name__ == "__main__":
    main()
