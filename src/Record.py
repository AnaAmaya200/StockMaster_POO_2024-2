from datetime import datetime
from src.JSONHandler import JSONHandler

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