import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    res = c1.post("/user/iforgot", {"email": "test@test.com", "udid": os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1")})
    print("Forgot:", res)

if __name__ == "__main__":
    main()
