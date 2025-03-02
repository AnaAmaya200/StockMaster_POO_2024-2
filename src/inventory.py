import json
import csv
import pandas as pd  # Requires `pip install pandas openpyxl`
from fpdf import FPDF  # Requires `pip install fpdf`

INVENTORY_JSON_PATH = 'data/inventory.json'

# Class to manage products
class Product():
    def __init__(self, id: int, name: str, price: float, stock: int) -> None:
        self.id = id            # Product ID
        self.name = name        # Product name
        self.price = price      # Product price
        self.stock = stock      # Product stock

    def __str__(self):
        return (
        f'Id: {self.id}\n'
        f'    Name: {self.name}\n'
        f'    Price: ${self.price:.2f}\n'
        f'    Stock: {self.stock}')
    
    # Converts the product to a dictionary
    def product_to_dict(self) -> dict:  
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }


# Class to manage inventory
class Inventory():
    def __init__(self, json_file=INVENTORY_JSON_PATH):    
        self.products = {}  # Dictionary of products
        self.json_file = json_file
        self.load_inventory()   

    # Load inventory from JSON
    def load_inventory(self):
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                for item in data.get('Products', []):
                    product = Product(**item)
                    self.products[product.id] = product
        except (FileNotFoundError, json.JSONDecodeError):
            print("The JSON file was not found or is corrupted. Starting with an empty inventory.")

    # Save inventory to JSON
    def save_inventory(self):
        with open(self.json_file, 'w') as file:
            data = {'Products': [product.product_to_dict() for product in self.products.values()]}
            json.dump(data, file, indent=4)

    # Export inventory to CSV, Excel, or PDF
    def export_inventory(self):
        print("\nSelect export format:")
        print("1. CSV")
        print("2. Excel (XLSX)")
        print("3. PDF")
        option = input("Enter your choice (1/2/3): ")

        filename = input("Enter the filename (without extension): ")
        
        if option == "1":
            filepath = f"{filename}.csv"
            with open(filepath, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Price", "Stock"])
                for product in self.products.values():
                    writer.writerow([product.id, product.name, product.price, product.stock])
            print(f"Inventory successfully exported to {filepath}")

        elif option == "2":
            filepath = f"{filename}.xlsx"
            df = pd.DataFrame([product.product_to_dict() for product in self.products.values()])
            df.to_excel(filepath, index=False)
            print(f"Inventory successfully exported to {filepath}")

        elif option == "3":
            filepath = f"{filename}.pdf"
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, "Inventory Report", ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", style='B', size=10)
            pdf.cell(30, 10, "ID", border=1)
            pdf.cell(60, 10, "Name", border=1)
            pdf.cell(40, 10, "Price ($)", border=1)
            pdf.cell(30, 10, "Stock", border=1)
            pdf.ln()

            pdf.set_font("Arial", size=10)
            for product in self.products.values():
                pdf.cell(30, 10, str(product.id), border=1)
                pdf.cell(60, 10, product.name, border=1)
                pdf.cell(40, 10, f"${product.price:.2f}", border=1)
                pdf.cell(30, 10, str(product.stock), border=1)
                pdf.ln()

            pdf.output(filepath)
            print(f"Inventory successfully exported to {filepath}")

        else:
            print("Invalid option. Please try again.")

