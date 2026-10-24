import json
import os

class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_name(self):
        return self.__name

    def get_product_id(self):
        return self.__product_id

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        if quantity < 0:
            raise ValueError("Stock cannot be negative")

        else:
            self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")  

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        print("Current Inventory")
        print("------------------------------------------------")
        for product in self.__products:
            product.display_information()
        print("--------------------------------------------")

    def get_all_products(self):
        return list(self.__products)

def show_menu():
    print("----------------- MENU -----------------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------------------")


def add_product_flow(inventory):
    user_id = input("Input your ID: ").strip().upper()

    if user_id == "":
        print("ID cannot be empty.")
        return

    if inventory.search_product(user_id) is not None:
        print("A product with that ID already exists.")
        return 

    user_name = input("Input your Name: ").strip()

    if user_name == "":
        print("Name cannot be empty.")
        return
    
    try:
        user_price = float(input("Input your Price: "))
        user_stock = int(input("Input your Stock: "))

        if (user_price < 0) or (user_stock < 0):
            print('Enter a valid number')
            return

    except ValueError:
        print("Please enter a valid number: ")
        return

    newProduct = Product(user_id, user_name, user_price, user_stock)

    inventory.add_product(newProduct)
    print("Product added successfully!")

def update_stock_flow(inventory):
    user_id = input("Input your ID: ").strip().upper()
    product = inventory.search_product(user_id)

    if product is None:
        print("Product not Found")
        return

    print(f"Product Found: {product.get_name()} | {product.get_stock()}")

    try:
        new_quantity = int(input('Enter your new quantity: '))
        product.update_stock(new_quantity)
        print('Stock has been updated')

    except ValueError as error:
        print(error)

def search_flow(inventory):
    product_id = input("Enter product_id: ").strip().upper()
    product = inventory.search_product(product_id)

    
    if product is None:
        print("Product not Found")
        
    else:
        print(f"-Name: {product.get_name()} \n-ID: {product.get_product_id()} \n-Price: ${product.get_price():.2f} \n-Stock: {product.get_stock()}")

def save_inventory(inventory):
    print("saving Inventory...")
    product_list = []

    for product in inventory.get_all_products():
        product_dict = {
            "product_id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock()
        }

        product_list.append(product_dict)

    with open("inventory.json", "w") as file:
        json.dump(product_list, file, indent=4)

    print("Inventory saved successfully to inventory.json.")

def load_inventory(inventory):
    if not os.path.exists("inventory.json"):
        print("No inventory.json found. Starting with an empty inventory.")
        return

    print("inventory.json found.")

    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)

        loaded_products = []
        for item in data:
            loaded_products.append(
                Product(item["product_id"], item["name"], item["price"], item["stock"])
            )
    except (json.JSONDecodeError, KeyError, TypeError):
        print("inventory.json is damaged. Starting with an empty inventory.")
        return

    for product in loaded_products:
        inventory.add_product(product)

    print("Saving inventory...")


def main():
    inventory = Inventory()

    print("="*40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("="*40)

    load_inventory(inventory)

    while True:
        show_menu()
        choice = input("Enter option: ")

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            add_product_flow(inventory)

        elif choice == "3":
            update_stock_flow(inventory)

        elif choice == "4":
            search_flow(inventory)

        elif choice == "5":
            save_inventory(inventory)

        elif choice == "6":
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        elif choice == "7":
            break

        else:
            print("An invalid option has been entered")

if __name__ == "__main__":
    main()











# p = Product("P001", "Laptop", 1200.00, 15)
# p.display_information()

# inventory = Inventory()
# inventory.add_product(p)
# inventory.add_product(Product("P002", "Mouse", 25.50, 40))

# found = inventory.search_product("P002")
# print(found)
# print(inventory.search_product("P9999"))
# inventory.display_all()

# found.display_information()




