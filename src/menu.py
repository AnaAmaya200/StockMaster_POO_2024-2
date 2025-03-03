from getpass import getpass

from src.inventory import Inventory, Product
from src.user import User
from src.record import Record

def handler_admin_menu(USER_JSON_PATH: str) -> None:
    while True:
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
    return None

def handler_boss_menu(inventory: Inventory, RECORDS_JSON_PATH: str, USER_JSON_PATH: str) -> None:
    while True:
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
    return None

def handler_employee_menu(inventory: Inventory, RECORDS_JSON_PATH: str) -> None:
    while True:
        print('\nMenu:')   
        print('1. Show products')
        print('2. Add product')
        print('3. Update product')
        print('4. Delete product')
        print('5. Change stock')
        print('6. Exit')
        option = input('  Select an option: ')  # Opción seleccionada por el usuario
        print()

        match option: 
            case '1':   # Show products
                inventory.show_products()

            case '2':  # Add product
                id = int(input('Enter id: '))
                name = input('Enter name: ')
                price = float(input('Enter price: '))
                stock = int(input('Enter stock: '))
                product = Product(id, name, price, stock)
                inventory.add_product(product)
                # Registrar la acción en el archivo JSON
                Record.add_record_to_json(id, name, stock, 'added', json_file=RECORDS_JSON_PATH)

            case '3':   # Update product
                id = int(input('Enter id: '))
                name = input('Enter name: ')
                price = float(input('Enter price: '))
                stock = int(input('Enter stock: '))
                product = Product(id, name, price, stock)
                inventory.update_product(product)
                # Registrar la acción en el archivo JSON
                Record.add_record_to_json(id, name, stock, 'updated', json_file=RECORDS_JSON_PATH)

            case '4':   # Delete product
                id = int(input('Enter id: '))
                deleted_product = inventory.delete_product(id)
                if deleted_product:
                    # Registrar la acción en el archivo JSON
                    Record.add_record_to_json(
                        id, deleted_product.name, deleted_product.stock, 'removed', json_file=RECORDS_JSON_PATH
                    )
                else:
                    print('Product not found')

            case '5':   # Change stock
                id = int(input('Enter id: '))
                stock = int(input('Enter new stock: '))
                product = inventory.change_stock(id, stock)
                if product:
                    # Registrar la acción en el archivo JSON
                    Record.add_record_to_json(
                        id, product.name, stock, 'stock_changed', json_file=RECORDS_JSON_PATH
                    )
                else:
                    print('Product not found')

            case '6':   # Exit
                print("Exiting the program...")
                break

            case _:     # Invalid option
                print('Invalid option. Please try again.')
    return None