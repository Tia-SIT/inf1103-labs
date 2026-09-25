import os

inventory = 0
failed_entries = 0
total_tax = 0
order_id = 0
inventory_list = []


def get_valid_input():
    while True:
        product_name = input('Enter Product Name: ')
        stock_quantity = input('Enter Quantity: ').strip()

        if stock_quantity.lower() == "quit":
            return "quit",0

        try:
            quantity = int(stock_quantity)

        except(ValueError):
            print('This is not a valid error, enter a valid error')
            return "invalid",0

        if quantity < 0:
            print('This is a negative number - please provide a positive number')
            return "invalid"

        return product_name, quantity

def process_delivery(current_total, new_value):
        new_value = current_total + new_value

        if new_value > 500:
            print('Alert! Your inventory has exceeded 500 unit')

        return new_value
    

def calculate_tax(amount):
    tax = 0.1*amount
    return tax
    

def generate_report(total_units, failed_attempts, tax_amount):
    print(f"""----- Summary Report ---------
    inventory : {inventory}
    failed entries : {failed_entries}
    tax: {tax_amount}

    
    """)

while True:
    if os.path.exists("inventory.txt") and os.path.getsize("inventory.txt") > 0:
        print("Current Orders:\n")
        with open("inventory.txt", "r") as f:
            print(f.read().strip())
        print()

    product_name, quantity = get_valid_input()

    if product_name == "quit":
        break 

    elif product_name == "invalid":
        failed_entries += 1

    else: 
        def get_next_order_id():
            if not os.path.exists('inventory.txt') or os.path.getsize('inventory.txt') == 0:
                return 1001

            with open("inventory.txt", "r") as file:
                lines = [line.strip() for line in file if line.strip()]

            if not lines:
                return 1001

            last_line = lines[-1]

            last_id = int(last_line.split(",")[0])

            return last_id + 1

        order_id = get_next_order_id()
                     
                 
        inventory = process_delivery(inventory, quantity)
        tax = total_tax + calculate_tax(quantity)

        new_order = [order_id, product_name, quantity]
        inventory_list.append(new_order)

        with open("inventory.txt", 'a') as file:
            line = ", ".join(str(item) for item in new_order)
            file.write(line + "\n")
            print("        ")
            print("New order added: ")
            print(line)
        break 

