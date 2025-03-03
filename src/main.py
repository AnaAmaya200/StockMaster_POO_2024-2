"""
main.py - Inventory Management System

This module provides a command-line interface to manage product inventory, 
including adding, updating, searching, and deleting products. 
It also records all actions in a JSON file for tracking purposes.

Modules:
    - inventory: Manages products and stock.
    - data_manager: Handles user and record data.

Functions:
    get_user_credentials(): Prompts the user to enter their login credentials.
    main(): Runs the main menu loop for inventory management.

JSON Files:
    - users.json: Stores user data for login authentication.
    - records.json: Logs all actions performed on the inventory.
"""

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
    return account, password

def main():
    User.load_users(USER_JSON_PATH)   # Load users from JSON file
    # Initialize JSON file for records
    Record.initialize_json_file(RECORDS_JSON_PATH, {'Records': []})    
    inventory = Inventory()    # Create an inventory object

    # Loop to login
    while True:
        print('\nWelcome to StockMaster')
        account, password = get_user_credentials()    # Get user credentials
        access, role = User.login(account, password)  # Login
        if access:
            print(f'Welcome, {account}, you have {role} access')
            break
        else:
            print('Login failed. Please try again.')
   # Loop to show the menu
    while role == "Employee":
        print('\nMenu:')   
        print('1. Add product')
        print('2. Show products')
        print('3. Search product')
        print('4. Change stock')
        print('5. Update product')
        print('6. Delete product')
        print('7. Exit')
        option = input('  Select an option: ')  # Opción seleccionada por el usuario
        print()

        match option: 
            case '1':   # Add product
                id = int(input('Enter product id: '))
                name = str(input('Enter product name: '))
                price = float(input('Enter product price: '))
                stock = int(input('Enter product stock: '))
                product = Product(id, name, price, stock)
                inventory.add_product(product)
                Record.add_record_to_json(
                    id, name, stock, 'added', json_file=RECORDS_JSON_PATH
                    )

            case '2':  # Show products
                inventory.show_products()

            case '3':   # Search product
                id = int(input('Enter product id: '))
                inventory.search_product(id)

            case '4':   # Change stock
                id = int(input('Enter product id: '))
                stock = int(input('Enter the value to adjust the stock: '))
                name = inventory.products[id].name
                inventory.change_stock(id, stock)
                Record.add_record_to_json(
                    id, name, stock, 'Stock Changed', json_file=RECORDS_JSON_PATH
                    )

            case '5':   # Update product
                id = int(input('Enter product id: '))
                name = input('Enter product name: ')
                price = float(input('Enter product price: '))
                stock = int(input('Enter product stock: '))
                product = Product(id, name, price, stock)
                inventory.update_product(product)
                Record.add_record_to_json(
                    id, name, stock, 'updated', json_file=RECORDS_JSON_PATH
                    )

            case '6':   # Delete product
                id = int(input('Enter product id: '))
                product = inventory.delete_product(id)
                if product:
                    Record.add_record_to_json(
                        id, product.name, product.stock, 'removed', json_file=RECORDS_JSON_PATH
                        )
                else:
                    print('Product not found')

            case '7':   # Exit
                print("Exiting the program...")
                break

            case _  :     # Invalid option
                print('Invalid option. Please try again.')

    while role == "Boss":
        print('\nMenu:')   
        print('1. Show records')
        print('2. Show products')
        print('3. Show users')
        print('4. Export records')
        print('5. Export products')
        print('6. Clean records')
        print('7. Exit')
        option = input('  Select an option: ')  # Opción seleccionada por el usuario
        print()

        match option: 
            case '1':   # show records
                Record.show_records(RECORDS_JSON_PATH)
                
            case '2':  # Show products
                inventory.show_products()

            case '3':   # Search users
                User.show_users(USER_JSON_PATH)

            case '4':   # Export records
                pass

            case '5':   # Export products
                pass

            case '6':   # Clean records
                Record.clean_records(RECORDS_JSON_PATH)

            case '7':   # Exit
                print("Exiting the program...")
                break

            case _:     # Invalid option
                print('Invalid option. Please try again.')


    while role == "Administrative":
            print('\nMenu:')   
            print('1. Show users')
            print('2. Add user')
            print('3. Delete user')
            print('4. Update user')
            print('5. Exit')
            option = input('  Select an option: ')  # Opción seleccionada por el usuario
            print()

            match option: 
                case '1':   # Show users
                    User.show_users(USER_JSON_PATH)

                case '2':  # Add user
                    account = input('Enter account: ')
                    password = getpass('Enter password: ')
                    role1 = input('Enter role: ')
                    User.add_user(account, password, role1, USER_JSON_PATH)

                case '3':   # Delete user
                    account = input('Enter account: ')
                    User.delete_user(account, USER_JSON_PATH)

                case '4':   #  Update user
                    account = input('Enter account: ')
                    new_password = getpass('Enter new password: ')
                    new_role = input('Enter new role: ')

                    User.update_user(account, new_password, new_role, USER_JSON_PATH)

                case '5':   # Exit
                    print("Exiting the program...")
                    break

                case _:     # Invalid option
                    print('Invalid option. Please try again.')

if __name__ == '__main__':
    main()
