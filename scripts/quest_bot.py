import os
import sys
import time
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.account_manager import AccountManager
from api.fruitcraft_client import FruitClient

def main():
    print("\n=== Fast Quest Automation Bot ===")
    am = AccountManager()
    accounts = am.list_accounts()
    active_accounts = [acc for name, acc in accounts.items() if not acc.get("disabled")]
    
    if not active_accounts:
        print("No active accounts found. Enable or create an account first.")
        return
        
    print("Select an account to login:")
    for i, acc in enumerate(active_accounts, 1):
        print(f"{i}. {acc['name']}")
        
    try:
        choice = int(input("\nEnter choice: ")) - 1
        if choice < 0 or choice >= len(active_accounts):
            print("Error: Invalid selection.")
            return
        selected_acc = active_accounts[choice]
    except ValueError:
        print("Error: Invalid input format.")
        return

    print(f"\nLogging in as {selected_acc['name']}...")
    client = FruitClient()
    success, resp = client.login(selected_acc['recovery_code'], selected_acc['udid'])
    
    if not success or not resp or 'data' not in resp:
        print(f"Error: Login failed for {selected_acc['name']}.")
        return
        
    player_data = resp['data']
    level = player_data.get('level', 1)
    
    # Filter weak cards (power < 70) for questing
    # Keep strong cards available for offense ministry mapping
    cards = [c['id'] for c in player_data.get('cards', []) if c.get('power', 0) < 70]
    
    if not cards:
        print("Error: No weak cards (power < 70) found!")
        print("Ensure you have weak cards in your deck to utilize the infinite quest loop.")
        return
        
    print(f"Found {len(cards)} weak cards for questing.")
    print("Starting automated quest loop. Press Ctrl+C to stop.\n")
    
    quest_count = 0
    total_xp = 0
    req_burst = 0
    
    try:
        while True:
            # 1. Pop the first card and append it to the back (Rotate selection)
            card_id = cards[0]
            cards.append(cards.pop(0))
            
            req_burst += 1
            
            # 2. Execute Quest
            q_resp = client.do_quest([card_id])
            
            if q_resp and q_resp.get('status'):
                q_data = q_resp.get('data', {})
                xp_added = q_data.get('xp_added', q_data.get('xpGain', 0))
                
                if xp_added > 0:
                    total_xp += xp_added
                    level = q_data.get('level', level)
                    quest_count += 1
                    
                    sys.stdout.write(f"\r『Quest Bot』 ╾ Quests: {quest_count} | XP: +{total_xp} | Level: {level} | Burst: {req_burst}/60   ")
                    sys.stdout.flush()
                else:
                    print("\n[!] Quest succeeded but no XP gained. Make sure your Offense Ministry has high power cards assigned!")
                    # Keep trying instead of breaking, sometimes it fluctuates
                    time.sleep(2)
            else:
                err = q_resp.get('error', 'Unknown Error') if q_resp else "Connection Timeout / 429"
                print(f"\n[!] Quest Request Failed: {err}")
                time.sleep(3)
            
            # 3. Rate Limiting Logic
            if req_burst >= 60:
                sys.stdout.write(f"\r『Quest Bot』 ╾ Reached {req_burst} rapid requests. Sleeping 10s to prevent ban...                 ")
                sys.stdout.flush()
                time.sleep(10)
                req_burst = 0
            else:
                # 1.5s pause to avoid rapid IP block / HTTP 429
                time.sleep(1.5)
                
    except KeyboardInterrupt:
        print(f"\n\nStopping bot gracefully. Final session stats:")
        print(f"- Quests Completed: {quest_count}")
        print(f"- XP Gained: {total_xp}")
        print(f"- Final Level: {level}")

if __name__ == '__main__':
    main()
