import sys, os, time, requests, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

import logging
import http.client as http_client

http_client.HTTPConnection.debuglevel = 1

def main():
    print('Testing Network Dumping...')
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    
    print('\n[+] Clean client request:')
    c1.get_profile()

if __name__ == '__main__':
    main()
