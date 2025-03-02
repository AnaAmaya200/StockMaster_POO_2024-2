from src.inventory import Inventory, Product
from src.data_manager import Record, User

from getpass import getpass  # Hides passwords

# JSON files path
DATA_DIR = 'data'
USER_JSON_PATH = f'{DATA_DIR}/users.json'  # JSON file for users
RECORDS_JSON_PATH = f'{DATA_DIR}/records.json'  # JSON file for logs

# Get user's credentials
def get_user_credentials():
    print("\nPlease login")
    account = input('  User: ')
    password = getpass('  Password: ')  # Hides passwords
    role = input('  Role (boss/administrative/employee): ').strip().lower()  # Normalize role input
    return account, password, role

def main():
    User.load_users(USER_JSON_PATH)  # Loads users
    Record.initialize_json_file(RECORDS_JSON_PATH, {'Records': []})  # Creates an empty JSON file
    inventory = Inventory()  # Instances Inventory class

    # Login loop
    while True:
        print('\nWelcome to StockMaster')
        account, password, role = get_user_credentials()  # Gets user's ID
        
        if User.login(account, password, role):  # Checks user's ID
            break
    
    # Options loop
    while True:
        print('\nMenu:')
        print('1. Add product')     # Boss & Administrative
        print('2. Show products')   # Boss & Employee
        print('3. Search product')  # Boss & Employee
        print('4. Change stock')    # Boss & Administrative
        print('5. Update product')  # Boss & Administrative
        print('6. Delete product')  # Boss only
        print('7. Exit')
        
        option = input('  Select an option: ')  # Input for user's selection

        match option:
            case '1':  # Add product (Boss & Administrative)
                if role not in ['boss', 'administrative']:
                    print("Access denied: Only bosses and administrative staff can add products.")
                    continue
                id = int(input('Enter product id: '))
                name = str(input('Enter product name: '))
                price = float(input('Enter product price: '))
                stock = int(input('Enter product stock: '))
                product = Product(id, name, price, stock)
                inventory.add_product(product)
                Record.add_record_to_json(id, name, stock, 'added', json_file=RECORDS_JSON_PATH)

            case '2':  # Show products (Boss & Employee)
                if role not in ['boss', 'employee']:
                    print("Access denied: Only bosses and employees can view products.")
                    continue
                inventory.show_products()

            case '3':  # Search products (Boss & Employee)
                if role not in ['boss', 'employee']:
                    print("Access denied: Only bosses and employees can search for products.")
                    continue
                id = int(input('Enter product id: '))
                inventory.search_product(id)

            case '4':  # Change stock (Boss & Administrative)
                if role not in ['boss', 'administrative']:
                    print("Access denied: Only bosses and administrative staff can change stock.")
                    continue
                id = int(input('Enter product id: '))
                stock = int(input('Enter the value to adjust the stock: '))
                name_4 = inventory.products[id].name
                inventory.change_stock(id, stock)
                Record.add_record_to_json(id, name_4, stock, 'Stock Changed', json_file=RECORDS_JSON_PATH)

            case '5':  # Update products (Boss & Administrative)
                if role not in ['boss', 'administrative']:
                    print("Access denied: Only bosses and administrative staff can update products.")
                    continue
                id = int(input('Enter product id: '))
                name = input('Enter product name: ')
                price = float(input('Enter product price: '))
                stock = int(input('Enter product stock: '))
                inventory.update_product(id, name, price, stock)
                Record.add_record_to_json(id, name, stock, 'updated', json_file=RECORDS_JSON_PATH)

            case '6':  # Delete products (Boss only)
                if role != 'boss':
                    print("Access denied: Only bosses can delete products.")
                    continue
                id = int(input('Enter product id: '))
                inventory.delete_product(id)
                Record.add_record_to_json(id, name, stock, 'removed', json_file=RECORDS_JSON_PATH)

            case '7':  # Exit program
                print("Exiting the program...")
                break

            case _:  # Invalid option
                print('Invalid option. Please try again.')


if __name__ == '__main__':
    main()
