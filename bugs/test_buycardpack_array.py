import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    print('Testing Card Pack Logic Bypass (Details)...')
    c1 = FruitClient()
    s1, d1 = c1.login('fact11439memory24', 'android_vuln_t1')
    if not s1: return
    
    # Let's get some gold
    c1.post('/player/withdrawfrombank', {'withdraw': 500})
    time.sleep(1)
    
    _, d1 = c1.login('fact11439memory24', 'android_vuln_t1')
    print('Gold Before:', d1['data'].get('gold', 0))
    
    # Try buying a high-end pack (e.g., 25 = Crystal Pack, costs 3M gold) with an array
    res = c1.post('/store/buycardpack', {'type': [25]})
    print('Array [25] Purchase Result:', res)
    time.sleep(2)
    
    res2 = c1.post('/store/buycardpack', {'type': True})
    print('Bool True Purchase Result:', res2)
    time.sleep(2)

    _, d2 = c1.login('fact11439memory24', 'android_vuln_t1')
    print('Gold After:', d2['data'].get('gold', 0))

if __name__ == '__main__':
    main()
