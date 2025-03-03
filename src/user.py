"""
User Class - Manages user authentication and user data.

This class handles user-related operations such as loading users from a JSON file,
saving users to a JSON file, user authentication (login), and displaying user information.

Inherits from:
    JSONHandler: Provides methods to load and save data in JSON format.

Class Attributes:
    users (list): A list to store User objects.

Methods:
    __init__(account: str, password: str, role: str): Initializes a User object.
    __str__(): Returns a string representation of the User object.
    load_users(json_file: str): Loads users from a JSON file into the `users` list.
    save_users(json_file: str): Saves the current list of users to a JSON file.
    login(account: str, password: str): Authenticates a user and returns their role if successful.
    show_users(json_file: str): Displays all users stored in the JSON file.

Attributes:
    account (str): The username of the user.
    password (str): The password of the user.
    role (str): The role of the user (e.g., Employee, Boss, Administrative).
"""

from src.json_handler import JSONHandler

# Clase para manejar los usuarios
class User(JSONHandler):
    users = []  # Lista de usuarios

    def __init__(self, account: str, password: str, role: str):
        self.account = account      # Nombre de usuario
        self.password = password    # Contraseña
        self.role = role            # Rol del usuario

    def __str__(self):
        return f'Account: {self.account}, Role: {self.role}'

    # Método para cargar los usuarios
    @classmethod
    def load_users(cls, json_file: str):
        data = cls.load_from_json(json_file, 'Users')    # Carga los datos
        if data:    # Si hay datos
            cls.users = [   # Crea una lista de usuarios
                User(user_data['account'], user_data['password'], user_data['role'])
                for user_data in data.get('Users', [])
            ]


    # Método para guardar los usuarios
    @classmethod
    def save_users(cls, json_file: str):
        # Crea un diccionario con los usuarios
        data = {'Usuarios': [user.__dict__ for user in cls.users]}
        cls.save_to_json(data, json_file)   # Guarda los datos
        print(f"Users successfully saved to '{json_file}'")

    # Método para agregar un usuario
    @classmethod
    def login(cls, account: str, password: str):
        for user in cls.users:  # Recorre la lista de usuarios
            if user.account == account:  # Verifica si el usuario existe
                if user.password == password:  # Verifica las credenciales
                    print("Successful login")
                    return True, user.role
                else:
                    print("Incorrect password")
                    return False, None
        print("Account does not exist")
        return False, None
    
    @classmethod
    def show_users(cls, json_file: str):
        cls.show_elements_of_json(json_file, 'Users')

    @classmethod
    def add_user(cls, account: str, password: str, role: str, json_file: str):
        new_user = User(account, password, role)
        cls.users.append(new_user)
        cls.save_users(json_file)  # Guarda los usuarios actualizados en el archivo JSON
        print(f"User '{account}' added successfully.")

    # Método para eliminar un usuario
    @classmethod
    def delete_user(cls, account: str, json_file: str):
        for user in cls.users:
            if user.account == account:
                cls.users.remove(user)
                cls.save_users(json_file)  
                print(f"User '{account}' deleted successfully.")
                return True
        print(f"User '{account}' not found.")
        return False

    @classmethod
    def update_user(cls, account: str, new_password: str = None, new_role: str = None, json_file: str = None):
        for user in cls.users:
            if user.account == account:
                if new_password:
                    user.password = new_password
                if new_role:
                    user.role = new_role
                cls.save_users(json_file)  
                print(f"User '{account}' updated successfully.")
