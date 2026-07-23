import sys, os, time
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    print('Testing Check Profile...')
    c1 = FruitClient()
    s1, d1 = c1.login('fact11439memory24', 'android_vuln_t1')
    
    d2 = c1.get_profile()
    c2_cards = d2.get('data', {}).get('cards', [])
    print(f'Total cards: {len(c2_cards)}')

if __name__ == '__main__':
    main()
