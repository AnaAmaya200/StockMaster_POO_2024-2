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
    def login(cls, account: str, password: str, role: str) -> None:
        for user in cls.users:  # Recorre la lista de usuarios
            if user.account == account:    # Verifica si el usuario existe
                if user.password == password and user.role == role: # Verifica las credenciales
                    print("Successful login")
                    return True
            else:
                return False
        print("Account does not exist")
        return False


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
            return data['Records'][-1]['Record_id'] + 1
        return 1

    # Método para agregar un registro al archivo JSON
    @classmethod
    def add_record_to_json(cls, product_id, name, amount, movement, json_file):
        next_id = cls.get_next_id(json_file)    # Obtiene el siguiente ID
        record = Record(next_id, product_id, name, amount, movement)  # Crea un registro
        data = cls.load_from_json(json_file, 'Records') or {'Records': []}   # Carga los datos
        data['Records'].append(record.to_dict())    # Agrega el registro a la lista
        cls.save_to_json(data, json_file)   # Guarda los datos