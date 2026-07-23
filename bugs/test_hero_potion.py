import sys, os, time, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    print('Testing /cards/potionize logic bypass...')
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    payload = {'hero_id': 1, 'potion': 0.1}
    res = c1.post('/cards/potionize', payload)
    print('Potionize Float:', res)

if __name__ == '__main__':
    main()
