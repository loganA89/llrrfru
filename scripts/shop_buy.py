import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.account_manager import AccountManager
from api.fruitcraft_client import FruitClient

def main():
    print("\n=== Card Shop Buy Script ===")
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
    
    if not success:
        print(f"Error: Login failed for {selected_acc['name']}.")
        return
        
    print("Login successful!\n")
    
    # Gold-buyable packs are hardcoded in the client (Data.BaseShopItems.lua)
    pack_list = [
        (1, "Brown Pack", 600),
        (2, "Green Pack", 2000),
        (3, "Yellow Pack", 6500),
        (4, "Red Pack", 10000),
        (5, "Silver Pack", 15000),
        (6, "Gold Pack", 35000),
        (7, "Platinium Pack", 110000),
        (8, "Black Pack", 350000),
        (16, "Monsters Pack", 2500000),
        (25, "Crystal Pack", 3000000)
    ]
        
    print("Available Gold Card Packs:")
    for i, (p_id, name, price) in enumerate(pack_list, 1):
        print(f"{i}. {name} (ID: {p_id}) - {price:,} Gold")
        
    try:
        pack_choice = int(input("\nEnter choice to buy: ")) - 1
        if pack_choice < 0 or pack_choice >= len(pack_list):
            print("Error: Invalid selection.")
            return
            
        selected_pack_id, selected_pack_name, selected_pack_price = pack_list[pack_choice]
        qty = int(input(f"How many '{selected_pack_name}' do you want to buy? "))
        
        if qty <= 0:
            print("Error: Quantity must be > 0.")
            return
    except ValueError:
        print("Error: Invalid input.")
        return

    print(f"\nBuying {qty}x '{selected_pack_name}'...")
    successful_buys = 0
    total_spent = 0
    
    for i in range(qty):
        print(f"Attempt {i+1}/{qty}...", end=" ")
        buy_resp = client.buy_card_pack(selected_pack_id)
        
        if buy_resp and buy_resp.get("status"):
            print("Success!")
            successful_buys += 1
            total_spent += selected_pack_price
        else:
            err = buy_resp.get("error", "Unknown error") if buy_resp else "No response"
            print(f"Failed: {err}")
            
        if i < qty - 1:
            time.sleep(1.5) # Minimum 1.5s delay required by server
            
    print("\n" + "="*30)
    print("      PURCHASE SUMMARY")
    print("="*30)
    print(f"Packs bought successfully : {successful_buys}/{qty}")
    if total_spent > 0:
        print(f"Estimated gold spent      : {total_spent:,}")
    print("="*30)

if __name__ == '__main__':
    main()
