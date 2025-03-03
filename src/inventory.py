import json
from src.Product import Product

INVENTORY_JSON_PATH = 'data/inventory.json'
# Class to manage products

# Class to manage the inventory
class Inventory():
    """The Inventory class manages a collection of products by loading, saving, and manipulating product data stored in a JSON file. 
    When initialized, the class loads the inventory data from the specified JSON file into a dictionary. It offers methods to add, display, search, update, and delete products within this dictionary. 
    Each time a change is made to the inventory (such as adding, updating, or deleting a product), the class saves the updated inventory back to the JSON file. This ensures that the inventory data remains consistent and up-to-date between sessions. The class provides a structured way to manage product information efficiently within an inventory system.
    """
    def __init__(self, json_file: str =INVENTORY_JSON_PATH):
        self.products = {}  # Dictionary to store the products
        self.json_file = json_file
        self.load_inventory()   # Load inventory from JSON

    # Load inventory from JSON
    def load_inventory(self) -> None:
        try:
            with open(self.json_file, 'r') as file:     # Open the file in read mode
                data = json.load(file)  # Load the data
                for item in data['Products']:   # Iterate over the products
                    item['id'] = int(item['id'])
                    product = Product(**item)   # Create a product object
                    self.products[product.id] = product # Add the product to the dictionary
        except FileNotFoundError:
            print(
                f"The JSON file was not found, starting with an empty inventory."
                )

            
    # Save inventory to JSON
    def save_inventory(self) -> None:
        with open(self.json_file, 'w') as file:     # Open the file in write mode
            data = {        # Create a dictionary with the products
                'Products': [
                    product.product_to_dict()   # Convert the product to a dictionary
                    for product in self.products.values()  
                ]
            }
            json.dump(data, file, indent=4)   # Write the data to the JSON file

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
