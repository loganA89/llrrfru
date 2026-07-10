import os
import sys
import subprocess
from api.account_manager import AccountManager

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n========================================")
    print(f"  {title}")
    print("========================================")

def manage_accounts(am):
    while True:
        print_header("Account Management")
        print("1. New Account")
        print("2. Edit Account")
        print("3. List Accounts")
        print("4. Back")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            name = input("Enter account name: ").strip()
            code = input("Enter recovery code: ").strip()
            if name and code:
                if am.add_account(name, code):
                    print("Success! Account created.")
                else:
                    print("Error: Account already exists.")
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            accounts = am.list_accounts()
            if not accounts:
                print("No accounts found.")
                input("\nPress Enter to continue...")
                continue
            
            names = list(accounts.keys())
            for i, name in enumerate(names, 1):
                status = "DISABLED" if accounts[name].get("disabled") else "ACTIVE"
                print(f"{i}. {name} [{status}]")
            
            try:
                acc_choice = int(input("\nSelect account number: ")) - 1
                if acc_choice < 0 or acc_choice >= len(names):
                    print("Invalid selection.")
                    continue
                selected_name = names[acc_choice]
            except ValueError:
                print("Invalid input.")
                continue
                
            print(f"\nEditing: {selected_name}")
            print("1. Edit Name")
            print("2. Edit Recovery Code")
            print("3. Disable Account")
            print("4. Enable Account")
            print("5. Delete Account")
            opt = input("\nEnter choice: ").strip()
            
            if opt == '1':
                new_name = input("Enter new name: ").strip()
                if new_name and am.edit_account(selected_name, new_name=new_name):
                    print("Name updated.")
            elif opt == '2':
                new_code = input("Enter new recovery code: ").strip()
                if new_code:
                    am.edit_account(selected_name, new_code=new_code)
                    print("Recovery code updated.")
            elif opt == '3':
                am.disable_account(selected_name)
                print("Account disabled.")
            elif opt == '4':
                am.enable_account(selected_name)
                print("Account enabled.")
            elif opt == '5':
                if input("Type 'yes' to delete: ").strip().lower() == 'yes':
                    am.delete_account(selected_name)
                    print("Account deleted.")
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            accounts = am.list_accounts()
            for name, acc in accounts.items():
                status = "DISABLED" if acc.get("disabled") else "ACTIVE"
                print(f"- {name} [{status}]")
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            break

def run_scripts():
    while True:
        print_header("Run Scripts")
        if not os.path.exists('scripts'):
            os.makedirs('scripts')
            
        scripts = [f for f in os.listdir('scripts') if f.endswith('.py') and not f.startswith('__')]
        if not scripts:
            print("No scripts found in /scripts/ folder.")
            input("\nPress Enter to back...")
            break
            
        for i, s in enumerate(scripts, 1):
            print(f"{i}. {s}")
        print(f"{len(scripts) + 1}. Back")
        
        try:
            choice = int(input("\nEnter choice: ")) - 1
            if choice == len(scripts):
                break
            if choice < 0 or choice >= len(scripts):
                print("Invalid selection.")
                continue
            selected_script = scripts[choice]
        except ValueError:
            print("Invalid input.")
            continue
            
        print(f"\nRunning {selected_script}...\n")
        subprocess.call([sys.executable, os.path.join('scripts', selected_script)])
        input("\nScript finished. Press Enter to continue...")

def main():
    am = AccountManager()
    while True:
        clear_screen()
        print("┌─────────────────────────────────┐")
        print("│  FruitCraft Script Manager      │")
        print("├─────────────────────────────────┤")
        print("│  1. Manage Accounts             │")
        print("│  2. Run Scripts                 │")
        print("│  3. Exit                        │")
        print("└─────────────────────────────────┘")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            manage_accounts(am)
        elif choice == '2':
            run_scripts()
        elif choice == '3':
            print("Exiting...")
            break

if __name__ == '__main__':
    main()
