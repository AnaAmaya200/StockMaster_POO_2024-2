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