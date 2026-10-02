import json 
import os

def display_all():
        print(
            """
    =======================================
    INVENTORY MANAGEMENT SYSTEM
    =======================================

    ------------ MENU ----------------------
    1. Display All Product 
    2. Add Product
    3. Update Stock
    4. Search Product
    5. Save Inventory
    6. Exit
    ----------------------------------------
    """
    )


def display_products(inventory):
    print("""
===================
Current Inventory
===================
            """)
    for inventory_item in inventory:
         print(f" ID:{inventory_item['ID']}  | Name:{inventory_item['Name']} | Price:{inventory_item['Price']} | Stock:{inventory_item['Stock']} ")


def add_product(inventory):
    id_input = input('Enter Product ID: ')
    name_input = input('Enter Product Name: ')
    price_input = input('Enter Product Price: ')
    stock_input = input('Enter Product Stock Quantity')

    inventory_item = {
        "ID" : id_input,
        "Name" : name_input,
        "Price" :price_input,
        "Stock" : stock_input
    }

    inventory = inventory.append(inventory_item)
    print("Product Added Successfully")
    return inventory

def update_product(inventory):
    print('Update Stock')
    product_id = input('Enter Product ID: ')

    for item in inventory:
        if product_id == item["ID"]:
            print('Product Found!')
            print(f"Name: {item['Name']} ")
            print(f"Current Stock: {item['Stock']}")

            item["Stock"] = input('New Stock Quantity')
            return inventory

            print("Stock updated successfully")

def search_product(inventory):
    print('Search Product')
    product_id = input('Enter Product ID: ').strip()

    found = False
    for item in inventory:
        if item["ID"] == product_id:
            print("Product Found")
            print("-----------------------------------")
            print(f"Product ID: {item['ID']}")
            print(f"Product Name {item['Name']}")
            print(f"Product Price: {item['Price']}")
            print(f"Product Stock: {item['Stock']}")
            found = True
            break
            print("------------------------------------")

    if not found:
            print("Product Not Found")

def save_inventory(inventory, filename="inventory.json"):
    print("\nSaving inventory...")
    with open(filename, "w") as file:
        json.dump(inventory, file, indent=4)
    print(f"Inventory saved successfully to {filename}.\n")
     


inventory_item1 = {
    "ID": "1001",
    "Name": "laptop",
    "Price" :  "178.56",
    "Stock" : 5
}

inventory_item2 = {
        "ID": "1002",
        "Name": "computer",
        "Price" :  "166",
        "Stock" : 7
    }

inventory_item3 = {
        "ID": "1003",
        "Name": "mouse",
        "Price" :  "120.3",
        "Stock" : 2
    }
inventory = [inventory_item1, inventory_item2, inventory_item3]

while True:
    display_all()
    option_input = input('Enter Option: ')

    if option_input == "1":
         display_products(inventory)
    
    elif option_input == "2":
         add_product(inventory)

    elif option_input == "3":
         update_product(inventory)

    elif option_input == "4":
         search_product(inventory)

    elif option_input == "5":
         save_inventory(inventory)

    elif option_input == "6":
        print("\nSaving inventory before exit...")
        with open("inventory.json", "w") as file:
            json.dump(inventory, file, indent=4)
        print("Inventory saved successfully.")
        print("\nThank you for using Inventory Management System.\nProgram terminated.")
        break
          