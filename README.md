![By (Doc Banner)](https://github.com/user-attachments/assets/849f0868-f4eb-493d-b6d7-1d115af4b103)

# UNIVERSIDAD NACIONAL DE COLOMBIA
# Programación Orientada a Objetos 2024-II

> Stockmaster es un sistema de gestión de inventario para una tienda de productos y componentes electrónicos; permite modificar, agregar y eliminar stock de productos que se moverían por un sistema logístico de almacenamiento.
> 
> Es presentado como proyecto final de la asignatura.
>
> Elegimos esta opción porque permite un alto grado de flexibilidad y adaptabilidad para poner en práctica los temas vistos durante el semestre, al igual que darle un enfoque particular al tomar piezas de las distintas ramas de la ingeniería en las cuales elegimos especializarnos.

# 📋 Tabla de contenido
1. [Recomendaciones de uso](#-recomendaciones-de-uso)
2. [Funcionalidades propuestas](#-funcionalidades-propuestas)
3. [Fase 1](#-fase-1)
4. [Fase 2](#-fase-2)
5. [Fase 3](#-fase-3)
8. [Integrantes](#-integrantes)

# 📖 Recomendaciones de uso
- Se recomienda usar Python 3.13 o superior
- No se requieren librerías adicionales no integradas
   
# 🚀 Funcionalidades propuestas
- ✅ Carga masiva de datos desde una base .json
- ✅ Mostrar el inventario actualizado en cualquier momento
- ✅ Login de usuarios protegido por contraseña
- ✅ Consulta detallada de cada operación (fecha, hora, usuario)
- ✅ Interfaz simple para navegar las distintas opciones

## 🏗 Fase 1
En la primera parte nos enfocamos en poner en marcha las funciones básicas:
- Manejo de inventario
- Estructuramiento de objetos
- Base de productos y funcionamiento

### :card_file_box: Diagrama UML fase 1

```mermaid
classDiagram
    class Producto {
        - id_producto: str
        - nombre: str
        - precio: float
        - cantidad: int
        + __init__(id_producto, nombre, categoria, precio, cantidad)
        + to_dict() dict
        + from_dict(data: dict) Producto
    }

    class Registro {
        - id_registro: int
        - id_producto: str
        - cantidad: int
        - tipo: str
        - fecha: str
        + __init__(id_registro, id_producto, cantidad, tipo, fecha)
        + to_dict() dict
    }

    class Inventario {
        - productos: list~Producto~
        - registros: list~Registro~
        + __init__()
        + agregar_producto(id_producto, nombre, precio, cantidad) "Crea registro automáticamente"
        + registrar_entrada(id_producto, cantidad)  "Crea registro automáticamente"
        + registrar_salida(id_producto, cantidad)  "Crea registro automáticamente"
        + listar_inventario()
        + buscar_producto(id_producto) Producto
    }

    Inventario --> Producto : 
    Inventario --> Registro : 
```

### 🛠 Estructura de archivos fase 1

```plaintext
📦 StockMaster/
|── 📌 main.py                    # Punto de entrada del programa
|
│── 📂 models/                    # Clases principales del proyecto
|  |── 📌 product.py              # Clase Producto: representa los productos del inventario
|  |── 📌 records.py              # Clase Registro: representa los movimientos (entradas/salidas)
|
│── 📂 services/                  # Lógica de negocio
|  |── 📌 inventory_service.py    # Manejo de inventario, registros y persistencia
```

### :sparkles: Resultados fase 1
Podemos observar una interfaz rudimentaria de interacción con el usuario
```python
StockMaster
1. Add product
2. Show products
3. Search product
4. Change stock
5. Update product
6. Delete product
7. Exit
Select an option: 1
Enter product id: 12
Enter product name: charger
Enter product price: 123
Enter product stock: 7
Product added successfully
```
ahora exploramos la muestra de elementos
```python
tockMaster
1. Add product
2. Show products
3. Search product
4. Change stock
5. Update product
6. Delete product
7. Exit
Select an option: 2
Products in inventory
Id:12 - Name:charger - Price: 123.0 - Stock: 7
StockMaster
1. Add product
2. Show products
3. Search product
4. Change stock
5. Update product
6. Delete product
7. Exit
Select an option:            
```
como se puede apreciar el elemento nuevo fue creado con éxito 
# 🏗 Fase 2
Para la segunda fase, comenzamos por agregar el sistema de autenticación con contraseña.
Adicional a esto hemos ejecutado el almacenamiento de elementos en formatos json asi mismo como su modificación.

Igualmente se crea la interfaz de usuario para navegar a través de las funcionalidades previas.
### :card_file_box: Diagrama UML fase 2
```mermaid
classDiagram
direction TB
    class Producto {
        - id_producto: str
        - nombre: str
        - precio: float
        - cantidad: int
        + __init__(id_producto, nombre, categoria, precio, cantidad)
        + to_dict() dict
        + from_dict(data: dict) Producto
    }

    class Registro {
        - id_registro: int
        - id_producto: str
        - cantidad: int
        - tipo: str
        - fecha: str
        + __init__(id_registro, id_producto, cantidad, tipo, fecha)
        + to_dict() dict
    }

    class Inventario {
        - productos: list~Producto~
        - registros: list~Registro~
        + __init__()
        + agregar_producto(id_producto, nombre, precio, cantidad) "Crea registro automáticamente"
        + registrar_entrada(id_producto, cantidad) "Crea registro automáticamente"
        + registrar_salida(id_producto, cantidad) "Crea registro automáticamente"
        + listar_inventario()
        + buscar_producto(id_producto) Producto
    }

    class Usuario {
        - cuenta: str
        - Contraseña: str
        - rol: str
        + __init__(cuenta, contraseña, rol)
        + to_dict() dict
        + cargar_usuarios(usuarios.json)
        + login(cuenta,contraseña,rol)
    }

    class inventario.json {
        - Productos: diccionary
    }

    class usuarios.json {
        - usuarios: diccionary
    }

    class registros.json {
        - registros: diccionary
    }

    Inventario --> Producto : "1..*"
    Inventario --> Registro : "1..*"
    Usuario --> Inventario : "2..*"
    inventario.json --> Inventario : "2..*"
    usuarios.json --> Usuario : "2..*"
    registros.json --> Registro : "2..*"

```

### 🛠 Estructura de archivos fase 2
```plaintext
📦 StockMaster/
|── 📌 main.py                    # Punto de entrada del programa
|
│── 📂 models/                    # Clases principales del proyecto
|  |── 📌 product.py              # Clase Producto: representa los productos del inventario
|  |── 📌 records.py              # Clase Registro: representa los movimientos (entradas/salidas)
|  |── 📌 Users.py                # Clase Users: se encarga de gestionar roles y permisos
|
│── 📂 services/                  # Lógica de negocio
|  |── 📌 inventory_service.py    # Manejo de inventario, registros y persistencia
│── 📄 inventory.json             # Archivo para almacenar los datos de los productos
│── 📄 records.json               # Archivo para almacenar los movimientos de inventario
│── 📄 usuarios.json              # Archivo para almacenar los usuarios registrados con sus contraseñas

```
### 💡 Ejemplo
La primera interacción con el usuario es el ingreso al sistema:
```python
Welcome to StockMaster
Please login
Name: Juanito Perez
Password: 1144
Role: employee
Cuenta no existente.
```
Juanito Perez no es un trabajador de la empresa ni está registrado en el sistema

```python
Welcome to StockMaster
Please login
Name: Felipe Gonzalez
Password: 0000
Role: Employee
Información inválida. Por favor, verifique.
```
Felipe Gonzalez está en el sistema pero su ingreso no correponde con los datos regitrados en la base de seguridad.
```python
Welcome to StockMaster
Please login
Name: Felipe Gonzalez
Password: 0000
Role: Boss
Login exitoso

Welcome to our system. Select an option:
1. Add product
2. Show products
3. Search product
4. Change stock
5. Update product
6. Delete product
7. Exit
Select an option: 1
Enter product id: 1000
Enter product name: Digital Camera
Enter product price: 2800
Enter product stock: 3
Product added successfully
Welcome to StockMaster
Please login
Name:

```
La información coincide con la base de datos de seguridad y el jefe pudo ingresar al sistema. Allí logra entrar a lo que se evidenció en la fase 1.

registros en los json
inventario.json
```python
{
    "Productos": [
        {
            "id": 1,
            "name": "Laptop",
            "price": 1200,
            "stock": 5
        },
        {
            "id": 2,
            "name": "Smartphone",
            "price": 800,
            "stock": 10
        },
        {
            "id": 3,
            "name": "Tablet",
            "price": 450,
            "stock": 8
        },
...
        {
            "id": 23,
            "name": "Headphones",
            "price": 250,
            "stock": 15
        }
    ]
}
```
usuarios.json
```python
{
    "Usuarios": [
        {
            "account": "Felipe Gonzalez",
            "Password": "0000",
            "role": "Boss"
        },
        {
            "account": "Santiago Daza",
            "Password": "0001",
            "role": "Administrative"
        },
        {
            "account": "Julian Torres",
            "Password": "0002",
            "role": "employee"
        },
        {
            "account": "Ana Amaya",
            "Password": "0003",
            "role": "employee"
        }
        
    ]
}
```
registros.json
Cabe resaltar que este se actualiza según las acciones hechas en el sistema
```python
{
    "Registros": [
        {
            "Record_id": 1,
            "Product_id": 64,
            "Amount": 1,
            "Movement": "add",
            "Date": "2025-01-29"
        },
        {
            "Record_id": 2,
            "Product_id": 24,
            "Amount": 1,
            "Movement": "removed",
            "Date": "2025-01-29"
        },
        {
            "Record_id": 3,
            "Product_id": 28,
            "Amount": 1,
            "Movement": "removed",
            "Date": "2025-01-29"
        },
        {
            "Record_id": 4,
            "Product_id": 64,
            "Amount": 1,
            "Movement": "removed",
            "Date": "2025-01-29"
        }
    ]
}
```
## 🏗 Fase 3
En el último segmento, se implementaron múltiples funcionalidades planteadas en el avance de proyecto y otros requerimientos finales que buscan garantizar las buenas prácticas al programar:
- Reestructuración de intefaz de login
- Restricción de clases discriminando por cargo
- Persistencia de errores
- Validación de tipo de datos ingresados
- Docstrings para cada módulo
- Consistencia en idioma de anotaciones
- Uso de git para control de versiones y sincronización de archivos
### :card_file_box: Diagrama UML fase 3
```mermaid
classDiagram
    class Product {
        +int productID
        +string name
        +float price
        +int quantity
        +displayProduct()
        +updateProduct()
        +searchProduct()
    }

    class User {
        +string username
        +string password
        +string role
        +login()
        +logout()
    }

    class Boss {
        +addProduct()
        +updateStock()
        +showTransactions()
    }

    class Administrative {
        +addProduct()
        +updateStock()
        +updateProduct()
    }

    class Employee {
        +showProducts()
        +searchProduct()
    }

    class Stock {
        +int productID
        +int stockQuantity
        +updateStock()
        +checkStock()
    }

    class Transaction {
        +int transactionID
        +int productID
        +int quantity
        +float totalPrice
        +processTransaction()
    }

    Product --> Stock : 
    User <|-- Boss : "inherits"
    User <|-- Administrative : "inherits"
    User <|-- Employee : "inherits"
    Transaction --> Product : "involves"
    Transaction --> Stock : "updates"
    Transaction --> User : "belongs to"
```
### 🛠 Estructura de archivos fase 3
```plaintext
📦 StockMaster/
|── 📌 README.md                    # Descripción del proyecto
|
│── 📂 src/                         # Clases principales del proyecto
|  |── 📂 __pycache__/              # Archivo de cache de Python
|  |── 📌 record.py                 # Clase Registro: registra las acciones realizadas por los usuarios
|  |── 📌 user.py                   # Clase Usuarios: gestiona la autenticación y los datos del usuario
|  |── 📌 inventory.py              # Clase Inventario: maneja las modificaciones a los productos
|  |── 📌 JSONHandler.py            # Clase JSON: soporta las operaciones con los archivos JSON
|  |── 📌 main.py                   # Clase Principal: interactúa con el usuario y utiliza las clases necesarias para cada situación
|  |── 📌 menu.py                   # Clase Registro: define las opciones del menú para cada usuario particular
|  |── 📌 product.py                # Clase Producto: representa los productos del inventario
|  |── 📌 records.py                # Clase Registro: representa los movimientos (entradas/salidas)
|
│── 📂 data/                        # Almacena la información en archivos JSON
│── 📄 inventory.json               # Archivo para almacenar los datos de los productos
│── 📄 records.json                 # Archivo para almacenar los movimientos de inventario
│── 📄 users.json                   # Archivo para almacenar los usuarios registrados con sus contraseñas

```
### 💡 Ejemplo:
Se muestra el menú disponible para Felipe González aka "The BOSS", con acceso a registros y exports:
```python
Please login
  User: Felipe Gonzalez
  Password: 
Successful login
Welcome, Felipe Gonzalez, you have Boss access

Menu:
1. Show records
2. Show products
3. Show users
4. Export records
5. Export products
6. Clean records
7. Exit
  Select an option:
```
En contraste, el menú para empleados, donde solo se permite modificar los productos:
```python
Please login
  User: Ana Amaya
  Password: 
Successful login
Welcome, Ana Amaya, you have Employee access

Menu:
1. Show products
2. Add product
3. Update product
4. Delete product
5. Change stock
6. Exit
```

## 🌟 Integrantes  
- 📱 Amaya Gómez Ana María
- 🏭 Daza Yepes Santiago
- 🤖 Torres Zaque Julian Ricardo


---

