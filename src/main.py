from src.inventory import Inventory, Product
from src.data_manager import Record, User

from getpass import getpass     # Hide password

# JSON file paths
DATA_DIR = 'data'
USER_JSON_PATH = f'{DATA_DIR}/users.json'   # JSON file for users
RECORDS_JSON_PATH = f'{DATA_DIR}/records.json'   # JSON file for records

# Function to obtain user credentials
def get_user_credentials() -> tuple:
    print("\nPlease login")
    account = input('  User: ')
    password = getpass('  Password: ')  # Hide password
    role = input('  Role: ')
    
    return account, password, role

def main():
    User.load_users(USER_JSON_PATH)   # Load users from JSON file
    # Initialize JSON file for records
    Record.initialize_json_file(RECORDS_JSON_PATH, {'Records': []})    
    inventory = Inventory()    # Create an inventory object

    # Loop to login
    while True:
        print('\nWelcome to StockMaster')
        account, password, role = get_user_credentials()    # Get user credentials
        
        if User.login(account, password, role):     # Verify user credentials
            break
   
   # Loop to show the menu
    while True:
        print('\nMenu:')   
        print('1. Add product')
        print('2. Show products')
        print('3. Search product')
        print('4. Change stock')
        print('5. Update product')
        print('6. Delete product')
        print('7. Exit')
        option = input('  Select an option: ')  # Opción seleccionada por el usuario

        match option: 
            case '1':   # Add product
                id = int(input('Enter product id: '))
                name = str(input('Enter product name: '))
                price = float(input('Enter product price: '))
                stock = int(input('Enter product stock: '))
                product = Product(id, name, price, stock)
                inventory.add_product(product)
                Record.add_record_to_json(
                    id, name, name, stock, 'added', json_file=RECORDS_JSON_PATH
                    )

            case '2':  # Show products
                inventory.show_products()

            case '3':   # Search product
                id = int(input('Enter product id: '))
                inventory.search_product(id)

            case '4':   # Change stock
                id = int(input('Enter product id: '))
                stock = int(input('Enter the value to adjust the stock: '))
                name_4 = inventory.products[id].name
                inventory.change_stock(id, stock)
                Record.add_record_to_json(
                    id, name_4, stock, 'Stock Changed', json_file=RECORDS_JSON_PATH
                    )

            case '5':   # Update product
                id = int(input('Enter product id: '))
                name = input('Enter product name: ')
                price = float(input('Enter product price: '))
                stock = int(input('Enter product stock: '))
                inventory.update_product(id, name, price, stock)
                Record.add_record_to_json(
                    id, name, stock, 'updated', json_file=RECORDS_JSON_PATH
                    )

            case '6':   # Delete product
                id = int(input('Enter product id: '))
                inventory.delete_product(id)
                Record.add_record_to_json(
                    id, name, stock, 'removed', json_file=RECORDS_JSON_PATH
                    )

            case '7':   # Exit
                print("Exiting the program...")
                break

            case _:     # Invalid option
                print('Invalid option. Please try again.')


if __name__ == '__main__':
    main()
