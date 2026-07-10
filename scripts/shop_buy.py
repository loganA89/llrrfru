import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.account_manager import AccountManager
from api.fruitcraft_client import FruitClient

def extract_packs(data):
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        if "card_packs" in data:
            return data["card_packs"]
        elif "items" in data:
            return data["items"]
        return [v for k, v in data.items() if isinstance(v, dict) and "id" in v]
    return []

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
        
    print("Login successful! Fetching shop items...")
    shop_resp = client.get_shop_items()
    
    if not shop_resp or not shop_resp.get("status"):
        print("Error: Failed to fetch shop items from the server.")
        return
        
    packs = extract_packs(shop_resp.get("data", {}))
    if not packs:
        print("Error: No packs found in the shop response.")
        return
        
    print("\nAvailable Gold Card Packs:")
    pack_list = []
    
    for p in packs:
        p_id = p.get('id')
        name = p.get('name', f"Pack {p_id}")
        
        raw_price = p.get('priceNumber', p.get('price'))
        is_gold = False
        display_price = "Unknown"
        
        if isinstance(raw_price, dict):
            is_gold = True
            display_price = str(raw_price.get('13', raw_price.get('1', 'Unknown')))
        elif isinstance(raw_price, str):
            if '.' not in raw_price and '$' not in raw_price:
                is_gold = True
                display_price = raw_price
        elif isinstance(raw_price, int):
            is_gold = True
            display_price = str(raw_price)
            
        if str(p_id) in ['90', '91']:
            is_gold = True
            
        if is_gold and p_id is not None:
            pack_list.append((p_id, name, display_price))
            
    if not pack_list:
        print("No gold-buyable packs found.")
        return
        
    for i, item in enumerate(pack_list, 1):
        p_id, name, price = item
        print(f"{i}. {name} (ID: {p_id}) - {price} Gold")
        
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
            try:
                clean_price = ''.join(c for c in str(selected_pack_price) if c.isdigit())
                total_spent += int(clean_price)
            except:
                pass
        else:
            err = buy_resp.get("error", "Unknown error") if buy_resp else "No response"
            print(f"Failed: {err}")
            
        if i < qty - 1:
            time.sleep(1)
            
    print("\n==============================")
    print("      PURCHASE SUMMARY")
    print("==============================")
    print(f"Packs bought successfully : {successful_buys}/{qty}")
    if total_spent > 0:
        print(f"Estimated gold spent      : {total_spent}")
    print("==============================")

if __name__ == '__main__':
    main()
