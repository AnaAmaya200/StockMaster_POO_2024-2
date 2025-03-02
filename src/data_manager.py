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

# Class to handle JSON files
class JSONHandler:
    # Method to load data
    @classmethod
    def load_from_json(cls, json_file: str, data_name: str) -> dict:
        try:
            with open(json_file, 'r') as file:  # Open the file in read mode
                data = json.load(file)  # Load the data
                return data     # Return the data
        except FileNotFoundError:   # Captures the exception if the file does not exist
            print(f"Error: File '{json_file}' does not exist")
            return None
        except json.JSONDecodeError:    # Captures the exception if the file is not a valid JSON
            print(f"The file '{json_file}' is corrupt or is not a valid JSON")

    # Method to save data
    @classmethod
    def save_to_json(cls, data: dict, json_file: str) -> None:
        try:
            with open(json_file, 'w') as file:  # Open the file in write mode
                json.dump(data, file, indent=4)     # Write the data to the file
        except Exception as e:  # Captures any exception
            print(f"Error: Could not save data to '{json_file}. Reason: {e}")

    # Method to initialize a JSON file
    @classmethod
    def initialize_json_file(cls, json_file: str, defauld_data: dict) -> None:
        if not os.path.exists(json_file):   # Check if the file exists
            cls.save_to_json(defauld_data, json_file)               # Save the default data
            print(f"Inicialized file at '{json_file} with default data")
        else:
            print(f"File '{json_file}' already exists")


# Class to manage users
class User(JSONHandler):
    users = []  # List to store the users

    def __init__(self, account: str, password: str, role: str):
        self.account = account      # User account
        self.password = password    # User password
        self.role = role            # User role

    def __str__(self):
        return f'Account: {self.account}, Role: {self.role}'

    # Method to load users
    @classmethod
    def load_users(cls, json_file: str) -> None:
        data = cls.load_from_json(json_file, 'Users')    # Load the data
        if data:    # Check if the data exists
            cls.users = [   # Create a list of users
                User(user_data['account'], user_data['password'], user_data['role'])
                for user_data in data.get('Users', [])
            ]

    # Method to save users
    @classmethod
    def save_users(cls, json_file: str) -> None:
        # Create a dictionary with the users
        data = {'Usuarios': [user.__dict__ for user in cls.users]}
        cls.save_to_json(data, json_file)   # Guarda los datos
        print(f"Users successfully saved to '{json_file}'")

    # Method to add a user
    @classmethod
    def login(cls, account: str, password: str, role: str) -> bool:
        for user in cls.users:  # Itera on the users
            if user.account == account:    # Check user account
                if user.password == password and user.role == role:
                    print("Successful login")
                    return True
        else:
            print("Account does not exist")
            return False


# Class to manage records
class Record(JSONHandler):
    def __init__(
            self, record_id: int, id:int, name: str, amount: int, movement: str
            ):
        now = datetime.now()    # Gets the current date and time
        self.record_id = record_id              # Record ID
        self.product_id = id                    # Product ID
        self.name = name                        # Product name
        self.amount = amount                    # Amount
        self.movement = movement                # Movement
        self.date = now.strftime("%Y-%m-%d")    # Date

    # Method to convert the record to a dictionary
    def to_dict(self) -> dict:
        return {
            'record_id': self.record_id,
            'product_id': self.product_id,
            'name': self.name,
            'amount': self.amount,
            'movement': self.movement,
            'date': self.date
        }

    # Method to initialize a JSON file
    @classmethod
    def initialize_json_file(cls, json_file: str, default_data: dict) -> None:
        if default_data is None:    
            default_data = {'Records': []}  # Valor por defecto
        super().initialize_json_file(json_file, default_data)   # Inicializa el archivo JSON

    # Method to get the next ID
    @classmethod
    def get_next_id(cls, json_file: str) -> int:
        data = cls.load_from_json(json_file, 'Records')    # Carga los datos
        if data and data['Records']:    
            return data['Records'][-1]['record_id'] + 1
        return 1

    # Method to add a record to the JSON file
    @classmethod
    def add_record_to_json(
        cls, product_id: int, name: str, amount: int, movement: str, json_file: str
        ) -> None:
        next_id = cls.get_next_id(json_file)    # Get the next ID
        record = Record(next_id, product_id, name, amount, movement)  # Create a record object
        data = cls.load_from_json(json_file, 'Records') or {'Records': []}   # Load the data
        data['Records'].append(record.to_dict())    # Add the record to the list
        cls.save_to_json(data, json_file)   # Save the data
        print("Record added successfully")