import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login('fact11439memory24', 'android_vuln_t1')
    print('Login Status:', s1)
    if not s1: 
        print(d1)
        return
    res = c1.get_profile()
    print('Profile Status:', res.get('status') if res else None)

if __name__ == '__main__':
    main()
