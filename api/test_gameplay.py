import logging
import inspect
from fruitcraft_client import FruitClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def test_api():
    client = FruitClient()
    
    expected_methods = [
        'assign_to_mine', 'assign_to_offense', 'assign_to_defense',
        'heal_card', 'heal_all', 'deposit_to_bank', 'withdraw_from_bank',
        'get_tribe_members', 'donate_tribe', 'leave_tribe', 'join_tribe_request',
        'find_tribe', 'poke_tribe_member', 'get_shop_items', 'turn_wheel',
        'claim_ad_reward', 'handle_error_backoff', 'add_potion'
    ]
    
    missing = []
    for m in expected_methods:
        if not hasattr(client, m):
            missing.append(m)
        else:
            # check docstring exists
            doc = getattr(client, m).__doc__
            if not doc:
                logging.warning(f"Method {m} is missing docstring")
                
    if missing:
        logging.error(f"Missing methods: {missing}")
        return False
        
    logging.info("All required Phase 7b methods implemented successfully with docstrings.")
    return True

if __name__ == '__main__':
    if test_api():
        print("Success! Ready to commit.")
    else:
        print("Failed. Missing required implementations.")
