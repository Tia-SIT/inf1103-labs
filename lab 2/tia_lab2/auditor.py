inventory = 0 
failed_entries = 0

while True:
    stock_quantity = input('Enter Stock Quantity: ')

    if stock_quantity == "Quit" or stock_quantity == "quit":
        break

    try:
        quanity = int(stock_quantity)

    except ValueError:
        print("This is not a valid number, enter a valid number")
        failed_entries = failed_entries + 1
        continue

    if quanity < 0:
        print('This is a negative number - please print a positive number: ')
        failed_entries = failed_entries + 1
        continue

    inventory = inventory + quanity
    if inventory > 500:
        print('Alert! Your inventory has exceeded 500 units!')
        break

print('Total Units Processed', inventory)
print('No. of failed entries: ', failed_entries)
    




