"""
data_manager.py - User and Record Management for JSON Files

This module provides classes and methods to manage users and records using JSON files. 
It includes functionality to load, save, and update JSON data, as well as user authentication.

Classes:
    JSONHandler: Provides methods to load, save, and initialize JSON files.
    User: Manages user data, authentication, and saves users to JSON files.
    Record: Handles record creation, storage, and management in JSON files.

Constants:
    INVENTORY_JSON_PATH: Path to the JSON file storing the inventory data.
"""

import json
import os
from datetime import datetime



# Clase para manejar archivos JSON
class JSONHandler:
    # Método para cargar datos
    @classmethod
    def load_from_json(cls, json_file, data_name: str):
        try:
            with open(json_file, 'r') as file:  # Abre el archivo en modo lectura
                data = json.load(file)  # Carga los datos del archivo JSON
                print(f"Data successfully loaded from '{json_file} | {data_name}'")
                return data     # Retorna los datos cargados
        except FileNotFoundError:   # Captura la excepción si el archivo no se encuentra
            print(f"Error: File '{json_file}' does not exist")
            return None
        except json.JSONDecodeError:    # Captura la excepción si el archivo no es un JSON válido
            print(f"The file '{json_file}' is corrupt or is not a valid JSON")

    # Método para guardar datos
    @classmethod
    def save_to_json(cls, data, json_file):
        try:
            with open(json_file, 'w') as file:  # Abre el archivo en modo escritura
                json.dump(data, file, indent=4)     # Escribe los datos en el archivo JSON
                print(f"Data successfully saved to '{json_file}'")
        except Exception as e:  # Captura cualquier excepción
            print(f"Error: Could not save data to '{json_file}. Reason: {e}")

    # Método para inicializar un archivo JSON
    @classmethod
    def initialize_json_file(cls, json_file, defauld_data):
        if not os.path.exists(json_file):   # Verifica si el archivo no existe
            # Guarda los datos por defecto
            cls.save_to_json(defauld_data, json_file)
            print(f"Inicialized file at '{json_file} with default data")
        else:   # Si el archivo ya existe
            print(f"File '{json_file}' already exists")
    
    @classmethod
    def show_elements_of_json(cls, json_file, data_name: str):
        data = cls.load_from_json(json_file, data_name)  # Carga los datos del archivo JSON
        if data:
            elements = data.get(data_name, [])
            print(f"\nElements in '{data_name}':")
            for element in elements:
                print(json.dumps(element, indent=4))  # Imprime cada elemento en formato JSON legible
        else:
            print(f"No data found in '{data_name}'.")

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
        data = {'Users': [user.__dict__ for user in cls.users]}
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
                    
    
# Clase para manejar los registros
class Record(JSONHandler):
    def __init__(self, record_id, id, name, amount, movement):
        now = datetime.now()                    # Obtiene la fecha y hora actual
        self.record_id = record_id              # ID del registro
        self.product_id = id                    # ID del producto
        self.name = name                        # Nombre del producto
        self.amount = amount                    # Cantidad
        self.movement = movement                # Movimiento
        self.date = now.strftime("%Y-%m-%d")    # Fecha

    # Método para convertir los datos a un diccionario
    def to_dict(self):
        return {
            'record_id': self.record_id,
            'product_id': self.product_id,
            'name': self.name,
            'amount': self.amount,
            'movement': self.movement,
            'date': self.date
        }

    # Método para inicializar un archivo JSON
    @classmethod
    def initialize_json_file(cls, json_file, default_data=None):
        if default_data is None:    
            default_data = {'Records': []}  # Valor por defecto
        super().initialize_json_file(json_file, default_data)   # Inicializa el archivo JSON

    # Método para obtener el siguiente ID
    @classmethod
    def get_next_id(cls, json_file):
        data = cls.load_from_json(json_file, 'Records')    # Carga los datos
        if data and data['Records']:    
            return data['Records'][-1]['record_id'] + 1
        return 1

    # Método para agregar un registro al archivo JSON
    @classmethod
    def add_record_to_json(cls, product_id, name, amount, movement, json_file):
        next_id = cls.get_next_id(json_file)    # Obtiene el siguiente ID
        record = Record(next_id, product_id, name, amount, movement)  # Crea un registro
        data = cls.load_from_json(json_file, 'Records') or {'Records': []}   # Carga los datos
        data['Records'].append(record.to_dict())    # Agrega el registro a la lista
        cls.save_to_json(data, json_file)   # Guarda los datos
    
    @classmethod
    def clear_json_file(cls, json_file: str) -> None:
        empty_data = {'Records': []}  # Data vacía
        cls.save_to_json(empty_data, json_file)  # Guardar datos vacíos en el archivo JSON
        print("JSON file cleared successfully")
    
    @classmethod
    def show_records(cls, json_file: str):
        cls.show_elements_of_json(json_file, 'Records')