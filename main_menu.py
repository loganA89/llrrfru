import os
import sys
import time

# Ensure we can import from the api folder
sys.path.insert(0, os.path.dirname(__file__))
from api.account_manager import AccountManager
from api.fruitcraft_client import FruitClient

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str):
    """Print a styled header."""
    print("\n" + "=" * 40)
    print(f"  {title}")
    print("=" * 40)

def menu_new_account(am: AccountManager):
    """Handle creation of a new account."""
    print_header("New Account")
    name = input("Enter account name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return
        
    code = input("Enter recovery code: ").strip()
    if not code:
        print("Error: Recovery code cannot be empty.")
        return
        
    if am.add_account(name, code):
        print(f"\nSuccess! Account '{name}' has been created.")
    else:
        print(f"\nError: Account '{name}' already exists.")

def menu_edit_account(am: AccountManager):
    """Submenu to edit, disable, or delete an existing account."""
    print_header("Edit Account")
    accounts = am.list_accounts()
    if not accounts:
        print("No accounts found. Please create one first.")
        return
        
    names = list(accounts.keys())
    for i, name in enumerate(names, 1):
        status = "DISABLED" if accounts[name].get("disabled") else "ACTIVE"
        print(f"{i}. {name} [{status}]")
        
    try:
        choice = int(input("\nSelect account number: ")) - 1
        if choice < 0 or choice >= len(names):
            print("Error: Invalid selection.")
            return
        selected_name = names[choice]
    except ValueError:
        print("Error: Invalid input format.")
        return

    while True:
        acc = am.get_account(selected_name)
        if not acc:
            break
            
        print_header(f"Editing: {selected_name}")
        print("1. Edit Name")
        print("2. Edit Recovery Code")
        print("3. Disable Account")
        print("4. Enable Account")
        print("5. Delete Account")
        print("6. Back")
        
        opt = input("\nSelect option: ").strip()
        
        if opt == '1':
            new_name = input("Enter new name: ").strip()
            if new_name:
                if am.edit_account(selected_name, new_name=new_name):
                    print("Name updated successfully.")
                    selected_name = new_name
                else:
                    print("Error: Failed to update name (name might already exist).")
        elif opt == '2':
            new_code = input("Enter new recovery code: ").strip()
            if new_code:
                am.edit_account(selected_name, new_code=new_code)
                print("Recovery code updated successfully.")
        elif opt == '3':
            am.disable_account(selected_name)
            print(f"Account '{selected_name}' disabled.")
        elif opt == '4':
            am.enable_account(selected_name)
            print(f"Account '{selected_name}' enabled.")
        elif opt == '5':
            confirm = input("Type 'yes' to confirm deletion: ").strip().lower()
            if confirm == 'yes':
                am.delete_account(selected_name)
                print("Account deleted successfully.")
                break
        elif opt == '6':
            break
        else:
            print("Invalid option. Please try again.")

def extract_packs(data: dict) -> list:
    """Helper to dynamically find packs in the shop JSON response."""
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        if "card_packs" in data:
            return data["card_packs"]
        elif "items" in data:
            return data["items"]
        # Fallback: find dicts with an 'id'
        return [v for k, v in data.items() if isinstance(v, dict) and "id" in v]
    return []

def menu_card_shop(am: AccountManager):
    """Test script to buy card packs using an active account."""
    print_header("Card Shop Test")
    
    accounts = am.list_accounts()
    active_accounts = [acc for name, acc in accounts.items() if not acc.get("disabled")]
    
    if not active_accounts:
        print("No active accounts found. Enable or create an account first.")
        return
        
    print("Select an account to login:")
    for i, acc in enumerate(active_accounts, 1):
        print(f"{i}. {acc['name']}")
        
    try:
        choice = int(input("\nSelect account number: ")) - 1
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
        
        raw_price = p.get('priceNumber')
        if raw_price is None:
            raw_price = p.get('price')
            
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
            
        # Exceptions for explicitly requested IDs if they somehow bypass the check
        if str(p_id) in ['90', '91']:
            is_gold = True
            
        if is_gold and p_id is not None:
            pack_list.append((p_id, name, display_price))
            
    if not pack_list:
        print("No gold-buyable packs found.")
        return
        
    for i, (p_id, name, price) in enumerate(pack_list, 1):
        print(f"{i}. {name} (ID: {p_id}) - {price} Gold")
        
    try:
        pack_choice = int(input("\nSelect pack number to buy: ")) - 1
        if pack_choice < 0 or pack_choice >= len(pack_list):
            print("Error: Invalid selection.")
            return
            
        selected_pack_id, selected_pack_name, selected_pack_price = pack_list[pack_choice]
        qty = int(input(f"How many '{selected_pack_name}' do you want to buy? "))
        
        if qty <= 0:
            print("Error: Quantity must be greater than 0.")
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
            time.sleep(1) # Delay to prevent server rate limiting
            
    print("\n" + "="*30)
    print("      PURCHASE SUMMARY")
    print("="*30)
    print(f"Packs bought successfully : {successful_buys}/{qty}")
    if total_spent > 0:
        print(f"Estimated gold spent      : {total_spent}")
    print("="*30)

def main():
    """Main execution loop for the CLI."""
    am = AccountManager()
    
    while True:
        print("\n┌─────────────────────────────────┐")
        print("│  FruitCraft Account Manager     │")
        print("├─────────────────────────────────┤")
        print("│  1. New Account                 │")
        print("│  2. Edit Account                │")
        print("│  3. Card Shop                   │")
        print("│  4. Exit                        │")
        print("└─────────────────────────────────┘")
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            menu_new_account(am)
        elif choice == '2':
            menu_edit_account(am)
        elif choice == '3':
            menu_card_shop(am)
        elif choice == '4':
            print("\nExiting FruitCraft Account Manager. Goodbye!")
            sys.exit(0)
        else:
            print("Error: Invalid option. Please try again.")

if __name__ == "__main__":
    main()
