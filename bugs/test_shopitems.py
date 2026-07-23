import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login('fact11439memory24', 'android_vuln_t1')
    
    print('Testing getshopitems...')
    # Try with version string
    res = c1.post('/store/getshopitems', {'version': '1.10.10755'})
    print('Result:', res)

if __name__ == '__main__':
    main()
