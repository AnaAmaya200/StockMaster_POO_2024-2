"""
main.py - Inventory Management System

This module provides a command-line interface to manage product inventory, 
including adding, updating, searching, and deleting products. 
It also records all actions in a JSON file for tracking purposes.

The system supports different user roles (Employee, Boss, Administrative) 
with specific permissions and functionalities for each role.

Modules:
    - inventory: Manages products and stock.
    - user: Handles user authentication and management.
    - record: Manages action logs and records.

Functions:
    get_user_credentials(): Prompts the user to enter their login credentials.
    main(): Runs the main menu loop for inventory management based on user role.

JSON Files:
    - users.json: Stores user data for login authentication.
    - records.json: Logs all actions performed on the inventory.

User Roles:
    - Employee: Can manage products (add, update, delete, change stock).
    - Boss: Can view records, products, users, and clean records.
    - Administrative: Can manage users (add, delete, update).

Usage:
    Run the script to start the inventory management system. 
    Users must log in with valid credentials to access the system.
"""

from getpass import getpass     # Hide password input

from src.menu import handler_admin_menu, handler_boss_menu, handler_employee_menu
from src.inventory import Inventory
from src.user import User
from src.record import Record

# JSON file paths
DATA_DIR = 'data'                                   # Directory for data files
USER_JSON_PATH = f'{DATA_DIR}/users.json'           # JSON file for users
INVENTORY_JSON_PATH = f'{DATA_DIR}/inventory.json'  # JSON file for inventory
RECORDS_JSON_PATH = f'{DATA_DIR}/records.json'      # JSON file for records

# Function to obtain user credentials
def get_user_credentials() -> tuple:
    print("\nPlease login")
    account = input('  User: ')     # Get username
    password = getpass('  Password: ')  # Hide password
    account = ' '.join(word.capitalize() for word in account.split())   # Capitalize username
    return account, password

def main():
    print('\n| StockMaster Inventory Management System |')
    User.load_users(USER_JSON_PATH)   # Load users from JSON file
    inventory = Inventory(INVENTORY_JSON_PATH)    # Create an inventory object
    Record.initialize_json_file(RECORDS_JSON_PATH) # Initialize records JSON file   
    
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
   
    # Main menu loop based on user role
    if role == 'Administrative':
        handler_admin_menu(USER_JSON_PATH)
    elif role == 'Boss':
        handler_boss_menu(inventory, RECORDS_JSON_PATH, USER_JSON_PATH)
    else:
        handler_employee_menu(inventory, RECORDS_JSON_PATH)

if __name__ == '__main__':
    main()
