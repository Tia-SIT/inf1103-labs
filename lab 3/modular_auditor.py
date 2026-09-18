inventory = 0
failed_entries = 0
total_tax = 0


def get_valid_input():
    while True:
        failed_entries = 0
        stock_quantity = input('Enter your stock_quantity: ').strip()

        if stock_quantity.lower() == "quit":
            return "quit"

        try:
            quantity = int(stock_quantity)

        except(ValueError):
            print('This is not a valid error, enter a valid error')
            return "invalid"

        if quantity < 0:
            print('This is a negative number - please provide a positive number')
            return "invalid"

        return quantity

def process_delivery(current_total, new_value):
        new_value = current_total + new_value

        if new_value > 500:
            print('Alert! Your inventory has exceeded 500 unit')

        return new_value
    

def calculate_tax(amount):
    tax = 0.1*amount
    return tax
    

def generate_report(total_units, failed_attempts):
    print(f""""----- Summary Report ---------
    inventory : {inventory}
    failed entries : {failed_entries}
    tax: {tax}

    
    """)

while True:
    result = get_valid_input()
    if result == "quit":
        break

    elif result == "invalid":
        failed_entries = failed_entries + 1

    else:
        inventory = process_delivery(inventory, result)
        tax = total_tax + calculate_tax(inventory)

generate_report(inventory, failed_entries)
