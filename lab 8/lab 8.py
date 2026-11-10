from abc import ABC, abstractmethod
import weakref

class Supplier():
    def __init__(self, supplier_id, supplier_name, supplier_contact_email):
        self._supplier_id = supplier_id
        self._supplier_name = supplier_name
        self._contact_email = supplier_contact_email

    def display_information(self):
        print(f"   Supplier ID: {self._supplier_id}")
        print(f"   Supplier Name: {self._supplier_name}")
        print(f"   Supplier Contact Email: {self._contact_email}")

class Product(ABC):
    def __init__(self, product_id: str, product_name: str, product_price: float, product_stock_quantity: int, supplier: Supplier):
        self._supplier: Supplier = supplier
        self._product_id = product_id
        self._product_name = product_name
        self._product_price = product_price
        self._product_stock_quantity = product_stock_quantity

    def update_stock(self, quantity: int):
        self._product_stock_quantity = quantity

    def display_information(self):
        print(f"   Product ID: {self._product_id}")
        print(f"   Product Name: {self._product_name}")
        print(f"   Product Price: {self._product_price}")
        print(f"   Product Stock Quantity: {self._product_stock_quantity}")
        self._supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self):
        pass

    @property
    def supplier(self):
        return self._supplier

    @property
    def product_id(self):
        return self._product_id

    @property
    def price(self) -> float:
        return self._product_price

    @property
    def name(self) -> str:
        return self._product_name



class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_weight, product_id, product_name, product_price, product_stock_quantity, supplier):
        super().__init__(product_id, product_name, product_price, product_stock_quantity, supplier)
        self._weight = product_weight

    def display_information(self):
        super().display_information()
        print(f"   Weight: {self._weight} kg")

    def get_fulfilment_info(self):
        return f"{self._product_name} will be shipped (weight: {self._weight} kg)."

    def calculate_shipping_cost(self):
        return 5.00 + 1.50 * self._weight

class DigitalProduct(Product):
    def __init__(self, product_download_size, product_id, product_name,
                 product_price, product_stock_quantity, supplier):
        super().__init__(product_id, product_name,
                         product_price, product_stock_quantity, supplier)
        self._download_size = product_download_size

    def display_information(self):
        super().display_information()
        print(f"   Download Size: {self._download_size} MB")

    def get_fulfilment_info(self):
        return f"{self._product_name} will be emailed as a download link ({self._download_size} MB)."

class Inventory:
    def __init__(self, name: str = "Inventory"):
        self._name: str = name
        self._products: list[Product] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def products(self) -> list[Product]:
        return list(self._products)  # copy, so outside code can't edit the list directly

    def add_product(self, product: Product) -> None:
        self._products.append(product)

    def remove_product(self, product_id: str) -> None:
        product = self.find_product(product_id)
        if product is not None:
            self._products.remove(product)

    def find_product(self, product_id: str) -> Product | None:
        for product in self._products:
            if product.product_id == product_id:
                return product
        return None

    def display_all_products(self) -> None:
        for product in self._products:
            product.display_information()

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self._product: Product = product    # a reference to an existing Product object
        self._quantity: int = quantity

    @property
    def product(self) -> Product:
        return self._product

    @property
    def quantity(self) -> int:
        return self._quantity

    def calculate_subtotal(self) -> float:
        return self._product.price * self._quantity

    def display_information(self) -> None:
        print(f"   {self._product.name} x {self._quantity} = {self.calculate_subtotal():.2f}")

class Order:
    def __init__(self, order_id: str):
        self._order_id: str = order_id
        self._order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        return list(self._order_lines)  # copy, so outside code can't add lines it created itself

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)   # the Order creates its own OrderLine
        self._order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> None:
        for order_line in self._order_lines:
            if order_line.product.product_id == product_id:
                self._order_lines.remove(order_line)
                return

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self._order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print(f"   Order {self._order_id}:")
        if not self._order_lines:
            print("   (no order lines)")
        for order_line in self._order_lines:
            order_line.display_information()
        print(f"   Total: {self.calculate_total():.2f}")





# ======================================================================
# TEST HELPERS (only used to make the output readable)
# ======================================================================
def header(title: str) -> None:
    print()
    print("=" * 64)
    print(title)
    print("=" * 64)

def step(text: str) -> None:
    print()
    print(f">> {text}")

def check(description: str, actual, expected) -> None:
    status = "PASS" if actual == expected else "FAIL"
    print(f"   [{status}] {description}  ->  {actual}")

def show_inventory(inventory: Inventory) -> None:
    ids = [p.product_id for p in inventory.products]
    print(f"   {inventory.name} contains: {ids if ids else '(empty)'}")

# ======================================================================
# SECTION 2: ASSOCIATION (Supplier <-> Product)
# ======================================================================
header("SECTION 2: ASSOCIATION  (Supplier and Product)")

step("Create one Supplier, then create two Products that use it")
supplier = Supplier("S1", "Acme", "acme@example.com")
book = PhysicalProduct(2.0, "P1", "Textbook", 49.99, 10, supplier)
ebook = DigitalProduct(15, "D1", "E-book", 19.99, 999, supplier)
print("   Created: supplier S1, book P1, ebook D1")

step("Supplier info, reached through each product")
print("   via book:")
book.supplier.display_information()
print("   via ebook:")
ebook.supplier.display_information()

step("Are they separate objects that share ONE supplier?")
check("book.supplier is the same object as supplier ", book.supplier is supplier, True)
check("ebook.supplier is the same object as supplier", ebook.supplier is supplier, True)
check("book and ebook are different objects         ", book is not ebook, True)
check("supplier and book are different objects      ", supplier is not book, True)

step("A supplier can exist with no products at all")
lonely_supplier = Supplier("S2", "Globex", "globex@example.com")
lonely_supplier.display_information()

# PREDICT FIRST: write your prediction BEFORE running this part
step("del supplier  (removes the NAME 'supplier', not the object)")
del supplier
print("   Products can still reach the supplier:")
book.supplier.display_information()
ebook.supplier.display_information()

# ======================================================================
# SECTION 3: AGGREGATION (Inventory <>- Product)
# ======================================================================
header("SECTION 3: AGGREGATION  (Inventory and Product)")

inventory_a = Inventory("Inventory A")
inventory_b = Inventory("Inventory B")

step("1. Products already exist, but no inventory holds them yet")
show_inventory(inventory_a)
show_inventory(inventory_b)
print(f"   Existing products: {book.product_id}, {ebook.product_id}")

step("2. Add both products to Inventory A")
inventory_a.add_product(book)
inventory_a.add_product(ebook)
show_inventory(inventory_a)

# PREDICT FIRST: write your prediction BEFORE running this part
step("3. Remove book (P1) from Inventory A")
inventory_a.remove_product("P1")
show_inventory(inventory_a)
check("P1 is no longer found in Inventory A", inventory_a.find_product("P1") is None, True)

step("Is the book object still usable?")
print(f"   {book.get_fulfilment_info()}")
book.update_stock(8)
print("   Stock updated to 8")
print(f"   Shipping cost: {book.calculate_shipping_cost()}")

step("4. Add the SAME book object to Inventory B")
inventory_b.add_product(book)
show_inventory(inventory_b)
check("B holds the same object, not a copy", inventory_b.find_product("P1") is book, True)

step("5. Empty both inventories")
inventory_a.remove_product("D1")
inventory_b.remove_product("P1")
show_inventory(inventory_a)
show_inventory(inventory_b)

step("Do the products still exist and work?")
print(f"   {book.get_fulfilment_info()}")
print(f"   {ebook.get_fulfilment_info()}")

# ======================================================================
# SECTION 4: COMPOSITION (Order <>- OrderLine)
# ======================================================================
header("SECTION 4: COMPOSITION  (Order and OrderLine)")

step("1. Create Order O1 and add two products with add_order_line()")
order_1 = Order("O1")
order_1.add_order_line(book, 2)
order_1.add_order_line(ebook, 1)
order_1.display_information()

step("2. Add the SAME book to a different Order (O2)")
order_2 = Order("O2")
order_2.add_order_line(book, 3)
order_2.display_information()

# PREDICT FIRST: write your prediction BEFORE running this part
step("3. How many OrderLine objects and how many Product objects exist?")
all_lines = order_1.order_lines + order_2.order_lines
print(f"   OrderLine objects: {len({id(line) for line in all_lines})}")
print(f"   Product objects:   {len({id(line.product) for line in all_lines})}")
del all_lines   # drop our own list so nothing outside the Orders keeps the lines alive

step("4. Each Order has its OWN line, but both lines point to the SAME book")
line_in_o1 = order_1.order_lines[0]
line_in_o2 = order_2.order_lines[0]
check("O1's book line is a different object from O2's", line_in_o1 is not line_in_o2, True)
check("Both lines refer to the same Product object   ", line_in_o1.product is line_in_o2.product, True)
check("That Product is the original book variable    ", line_in_o1.product is book, True)

step("5. Remove the e-book line from O1 using an Order method")
order_1.remove_order_line("D1")
order_1.display_information()
order_2.display_information()
print(f"   The e-book itself still works: {ebook.get_fulfilment_info()}")

step("6. Delete the whole Order O2: what happens to its OrderLine?")
line_ref = weakref.ref(line_in_o2)   # a weak reference does not keep the line alive
check("O2's line exists before the order is deleted", line_ref() is not None, True)
del line_in_o2
del order_2
check("O2's line is gone after the order is deleted ", line_ref() is None, True)
print(f"   The book still works: {book.get_fulfilment_info()}")

# ======================================================================
# SECTION 6: LISKOV SUBSTITUTION (Product abstraction)
# ======================================================================
def show_product_details(product: Product) -> None:
    # Only uses behaviour that EVERY Product promises to support.
    product.display_information()
    print(f"   {product.get_fulfilment_info()}")

header("SECTION 6: LISKOV SUBSTITUTION  (Product abstraction)")

step("1. One function, two product types (the function is never changed)")
print("   show_product_details(book):")
show_product_details(book)
print()
print("   show_product_details(ebook):")
show_product_details(ebook)

step("2. Both product types can be added to the same Inventory")
lsp_inventory = Inventory("LSP Inventory")
lsp_inventory.add_product(book)
lsp_inventory.add_product(ebook)
show_inventory(lsp_inventory)

step("3. Inventory operations work on both types")
check("find_product('P1') returns the physical product", lsp_inventory.find_product("P1") is book, True)
check("find_product('D1') returns the digital product ", lsp_inventory.find_product("D1") is ebook, True)

print()
print("   update_stock(5) on every product in the Inventory:")
for product in lsp_inventory.products:
    product.update_stock(5)
lsp_inventory.display_all_products()

step("4. remove_product works for both types")
lsp_inventory.remove_product("P1")
lsp_inventory.remove_product("D1")
show_inventory(lsp_inventory)

# ======================================================================
# SECTION 7.2: DEMONSTRATE POLYMORPHISM
# ======================================================================
header("SECTION 7.2: POLYMORPHISM  (one loop, different Product types)")

step("1. Put both product types in the SAME Inventory")
poly_inventory = Inventory("Poly Inventory")
poly_inventory.add_product(book)
poly_inventory.add_product(ebook)
show_inventory(poly_inventory)

# PREDICT FIRST: write what each product will print for get_fulfilment_info()
step("2. ONE loop: display_information() and get_fulfilment_info() on every Product")
for product in poly_inventory.products:
    product.display_information()
    print(f"   -> {product.get_fulfilment_info()}")
    print()

step("3. Check each object gave its OWN specialised result")
expected = {
    "P1": "Textbook will be shipped (weight: 2.0 kg).",
    "D1": "E-book will be emailed as a download link (15 MB).",
}
for product in poly_inventory.products:
    check(f"{product.product_id} message is correct", product.get_fulfilment_info(), expected[product.product_id])
