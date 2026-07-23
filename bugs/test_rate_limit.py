import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    c1 = FruitClient()
    s1, d1 = c1.login('fact11439memory24', 'android_vuln_t1')
    
    # Send requests fast
    for i in range(10):
        res = c1.post('/player/getplayerinfo', {})
        if res.get('raw_html'):
            print(f'Attempt {i}: Got HTML Crash! (Rate limit or WAF triggered)')
            break
        else:
            print(f'Attempt {i}: OK')

if __name__ == '__main__':
    main()
