"""
This module defines the JSONHandler class for handling JSON file operations.

The JSONHandler class provides functionalities to load data from a JSON file, 
save data to a JSON file, initialize a JSON file with default data, and display 
elements from a JSON file.

Classes:
    JSONHandler: A class to handle JSON file operations.
"""

import json
import os

# Clase para manejar archivos JSON
class JSONHandler:
    # Método para cargar datos
    @classmethod
    def load_from_json(cls, json_file: str, data_name: str) -> dict:
        try:
            with open(json_file, 'r') as file:  # Abre el archivo en modo lectura
                data = json.load(file)  # Carga los datos del archivo JSON
                print(f"{data_name} successfully loaded from '{json_file}'")
                return data     # Retorna los datos cargados
        except FileNotFoundError:   # Captura la excepción si el archivo no se encuentra
            print(f"Error: File '{json_file}' does not exist")
            return None
        except json.JSONDecodeError:    # Captura la excepción si el archivo no es un JSON válido
            print(f"The file '{json_file}' is corrupt or is not a valid JSON")

    # Método para guardar datos
    @classmethod
    def save_to_json(cls, data: dict, json_file: str) -> None:
        try:
            with open(json_file, 'w') as file:  # Abre el archivo en modo escritura
                json.dump(data, file, indent=4)     # Escribe los datos en el archivo JSON
                print(f"Data successfully saved to '{json_file}'")
        except Exception as e:  # Captura cualquier excepción
            print(f"Error: Could not save data to '{json_file}. Reason: {e}")

    # Método para inicializar un archivo JSON
    @classmethod
    def initialize_json_file(
        cls, json_file: str, defauld_data: str, data_name: str
        ) -> None:
        if not os.path.exists(json_file):   # Verifica si el archivo no existe
            # Guarda los datos por defecto
            cls.save_to_json(defauld_data, json_file)
            print(f"Inicialized file at '{json_file} with default data")
        else:   # Si el archivo ya existe
            print(f"{data_name} already exists from '{json_file}'")       
    
    @classmethod
    def show_elements_of_json(cls, json_file: str, data_name: str) -> None:
        data = cls.load_from_json(json_file, data_name)  # Carga los datos del archivo JSON
        if data:
            elements = data.get(data_name, [])
            print(f"\nElements in '{data_name}':")
            for element in elements:
                print(json.dumps(element, indent=4)) 
        else:
            print(f"No data found in '{data_name}'.")
