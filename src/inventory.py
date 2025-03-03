"""
inventory.py - Inventory and Product Management

This module provides classes and methods to manage products and inventory, 
including adding, updating, searching, and deleting products. 
It also allows saving and loading the inventory from a JSON file.

Classes:
    Product: Represents a product with ID, name, price, and stock.
    Inventory: Manages a collection of products and handles JSON file operations.

Constants:
    INVENTORY_JSON_PATH: Path to the JSON file storing the inventory data.
"""

import json

from src.json_handler import JSONHandler

class Product():
    def __init__(self, id: int, name: str, price: float, stock: int):
        self.id = id            # Product ID
        self.name = name        # Product name
        self.price = price      # Product price
        self.stock = stock      # Product stock

    def __str__(self):
        return (
        f'Id: {self.id}\n'
        f'    Name: {self.name}\n'
        f'    Price: ${self.price}\n'
        f'    Stock: {self.stock}')
    
    # Convert product data to a dictionary
    def product_to_dict(self) -> dict:  
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }


class Inventory(JSONHandler):
    def __init__(self, json_file: str):
        self.products = {}  # Diccionario para almacenar productos
        self.json_file = json_file
        self.load_inventory()  # Cargar inventario desde JSON
        super().__init__()  # Inicializa JSONHandler

    # Load inventory from JSON
    def load_inventory(self) -> None:
        try:
            with open(self.json_file, 'r') as file:     # Open the file in read mode
                data = json.load(file)  # Load the data
                for item in data['Products']:   # Iterate over the products
                    item['id'] = int(item['id'])
                    product = Product(**item)   # Create a product object
                    self.products[product.id] = product # Add the product to the dictionary
                print(f"Inventory succesfully loaded from '{self.json_file}'")
            
        except FileNotFoundError:
            print(
                f"The JSON file was not found, starting with an empty inventory."
                )
        return None

    # Save inventory to JSON
    def save_inventory(self) -> None:
        data = {
            'Products': [
                product.product_to_dict() for product in self.products.values()
            ]
        }
        self.save_to_json(data, self.json_file)  # Usar método heredado
        print(f"Inventory successfully saved to {self.json_file}")
        return None

    # Add a product to the inventory
    def add_product(self, product: dict) -> bool:
        if product.id in self.products:   # Check if the product already exists
            print('Product already exists')
            return False
        else:
            self.products[product.id] = product  # Add the product to the dictionary
            self.save_inventory()   # Save the inventory to the JSON file
            print('\nProduct added successfully\n')

    # Show the products in the inventory
    def show_products(self) -> None:
        print('Products in inventory\n')
        for product in self.products.values():  # Iterate over the products
            print(product)   
        return None 

    # Search for a product in the inventory
    def search_product(self, id: int):
        product = self.products.get(id)  # Get the product from the dictionary
        if product:
            print(product) 
            return product    # Return the product
        else:
            print('Product not found')
            return None
    
    # Change the stock of a product
    def change_stock(self, id: int, change_stock: int) -> bool:
        product = self.search_product(id)
        if product:
            product.stock = change_stock    # Update the stock of the product
            self.save_inventory()   # Save the inventory to the JSON file
            print('Stock updated successfully')
            return True
        return False

    # Update the product information
    def update_product(self, product: dict) -> bool:
        if product:     # Update the product information
            self.products[product.id] = product
            self.save_inventory()   # Save the inventory in the JSON file
            print('Product updated successfully')
            return True
        return False
    
    # Elimina un producto del inventario
    def delete_product(self, id: int) -> bool:
        product = self.search_product(id)   # Busca el producto
        if product:
            self.products.pop(id)   # Elimina el producto del diccionario
            self.save_inventory()   # Save the inventory in the JSON file
            print('Product deleted successfully')
            return product
        return None
