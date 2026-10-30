from inventory_manager import Product, PhysicalProduct, DigitalProduct, CanBeShipped

print("--- Shipping cost at different weights ---")
for name, weight in [("Pen", 0.5), ("Guitar", 3.2), ("Piano", 10)]:
    item = PhysicalProduct("P" + name, name, 10.0, 1, weight)
    print(f"{name} ({weight} kg): ${item.calculate_shipping_cost():.2f}")

os_disc = DigitalProduct("D100", "Operating System", 99.0, 1000, 4500)
guitar = PhysicalProduct("P100", "Guitar", 450.0, 5, 3.2)

print("--- Interface checks ---")
print("Guitar can be shipped:", isinstance(guitar, CanBeShipped))
print("Guitar is a Product:", isinstance(guitar, Product))
print("OS can be shipped:", isinstance(os_disc, CanBeShipped))
print("OS is a Product:", isinstance(os_disc, Product))

try:
    CanBeShipped()
except TypeError as error:
    print("TypeError:", error)
