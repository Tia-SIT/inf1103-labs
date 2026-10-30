import json
import os
import tempfile

from inventory_manager import (
    Product, PhysicalProduct, DigitalProduct, CanBeShipped, Inventory,
    save_inventory, load_inventory,
)

results = []

def check(description, condition):
    results.append(condition)
    print(f"[{'PASS' if condition else 'FAIL'}] {description}")

guitar = PhysicalProduct("P100", "Guitar", 450.0, 5, 3.2)
os_disc = DigitalProduct("D100", "Operating System", 99.0, 1000, 4500)

# 1. Physical products store and display their weights
check("Physical product stores its weight", guitar.get_weight() == 3.2)
print("--- display_information() for physical product ---")
guitar.display_information()

# 2. Digital products store and display their download sizes
check("Digital product stores its download size", os_disc.get_download_size() == 4500)
print("--- display_information() for digital product ---")
os_disc.display_information()

# 3. Both subclasses implement get_fulfilment_info()
check("PhysicalProduct implements get_fulfilment_info()", "shipping" in guitar.get_fulfilment_info())
check("DigitalProduct implements get_fulfilment_info()", "digitally" in os_disc.get_fulfilment_info())

# 4. Abstract Product cannot be instantiated
try:
    Product("X001", "Generic", 10.0, 1)
    check("Product cannot be instantiated directly", False)
except TypeError as error:
    print("TypeError:", error)
    check("Product cannot be instantiated directly", True)

# 5. Physical products can calculate shipping costs
check("Shipping cost for 0.5 kg is 6.00", PhysicalProduct("A", "A", 1.0, 1, 0.5).calculate_shipping_cost() == 6.0)
check("Shipping cost for 10 kg is 25.00", PhysicalProduct("B", "B", 1.0, 1, 10).calculate_shipping_cost() == 25.0)
check("PhysicalProduct is a CanBeShipped", isinstance(guitar, CanBeShipped))

# 6. Digital products are not required to implement shipping
check("DigitalProduct is not a CanBeShipped", not isinstance(os_disc, CanBeShipped))
check("DigitalProduct has no calculate_shipping_cost", not hasattr(os_disc, "calculate_shipping_cost"))

# 7. Inventory operations
inventory = Inventory()
inventory.add_product(guitar)
inventory.add_product(os_disc)
check("Inventory.add_product / get_all_products", len(inventory.get_all_products()) == 2)
check("Inventory.search_product finds an existing product", inventory.search_product("D100") is os_disc)
check("Inventory.search_product returns None when missing", inventory.search_product("NOPE") is None)
inventory.search_product("P100").update_stock(12)
check("Updating stock works", guitar.get_stock() == 12)
try:
    guitar.update_stock(-1)
    check("Negative stock is rejected", False)
except ValueError:
    check("Negative stock is rejected", True)
print("--- Inventory.display_all() ---")
inventory.display_all()

# 8. JSON saving and loading preserve the types (uses a temporary folder,
#    so your real inventory.json is not touched)
original_dir = os.getcwd()
with tempfile.TemporaryDirectory() as temp_dir:
    os.chdir(temp_dir)
    save_inventory(inventory)

    with open("inventory.json") as file:
        saved = json.load(file)
    check("JSON contains 'physical' and 'digital' types", [p["type"] for p in saved] == ["physical", "digital"])

    restored = Inventory()
    load_inventory(restored)
    os.chdir(original_dir)

check("Loading produced exactly 2 products", len(restored.get_all_products()) == 2)
loaded_guitar = restored.search_product("P100")
loaded_os = restored.search_product("D100")
check("Loaded guitar is a PhysicalProduct", type(loaded_guitar) is PhysicalProduct)
check("Loaded guitar keeps its weight and stock", loaded_guitar.get_weight() == 3.2 and loaded_guitar.get_stock() == 12)
check("Loaded OS is a DigitalProduct", type(loaded_os) is DigitalProduct)
check("Loaded OS keeps its download size", loaded_os.get_download_size() == 4500)

print()
print(f"{sum(results)} of {len(results)} checks passed")
