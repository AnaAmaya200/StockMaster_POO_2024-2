class Product():
    """The Product class designed to hold essential information about a product, including its unique: identifier (id)
    name (name)
    price (price)
    and the number of items in stock (stock).
    When an instance of the Product class is created, these attributes are initialized with the provided values. 
    The class includes a method called __str__ which returns a formatted string representation of the product, making it easy to display the product's details in a readable format.
    This class provides a straightforward way to manage and display product information within an inventory system.


    """
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

