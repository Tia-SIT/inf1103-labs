from abc import ABC, abstractmethod
import csv

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_email = contact_email

    def display_information(self) -> None:
        print(f"Supplier [{self.supplier_id}] : {self.name} ({self.contact_email})")

class CanBeShipped(ABC):
    # why doesn't this have any init method or any attributes and just one method?
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass

class Product(ABC):  # blueprint for storing and managing an individual product's data
    # question: where are we supposed to put the @abstractmethod? and why do we need it? 

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
        if price <= 0:
            raise ValueError("A product price must be greater than zero.")

        if stock < 0:
            raise ValueError("A product’s stock quantity cannot be negative.")
        self._product_id = product_id
        self._name = name
        self.price = price      # goes through the setter, so validation runs
        self.stock = stock      # goes through the setter, so validation runs
        self.supplier = supplier

        # question : are these variables private, protected or public? when do we generally use which
        # Access Modifiers in Python:
        # self.name   -> PUBLIC (+):    Accessible anywhere. Use for public methods/API.
        # self._name  -> PROTECTED (#): Used within this class & child subclasses (convention).
        # self.__name -> PRIVATE (-):   Name-mangled. Restricted strictly to this class only.

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Price must be greater than zero.")
        self._price = value

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        if value < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock = value

    def update_stock(self, quantity: int) -> None: # adding new stock to the current stock
        new_stock = self._stock + quantity
        if new_stock < 0:
            raise ValueError("Resulting stock cannot be negative.") 
        # why do we validate only after we calculate the new stock shouldn't we be validating the quantity?
        # ans: validates final balance so quantity can be positive (add stock) or negative (remove stock)
        self._stock = new_stock

    def display_information(self) -> None: # why does it return a none type? i thought it prints out some text?
        # returns None because it prints text to console rather than returning data
        print(f"[{self._product_id}] [{self._name}] | Price: ${self._price:.2f} | Stock: {self._stock}")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.weight = weight # question : why is this a public class?

    def display_information(self) -> None:
        super().display_information() # question: when do you print in a method and when do you return in a method?
        print(f" | Weight: {self.weight}kg | Shipping: {self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return f"Physical shipping required. Item weight: {self.weight}kg"

    def calculate_shipping_cost(self) -> float:
        return self.weight * 2.50

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.download_size = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f" | Download Size: {self.download_size} MB")

    def get_fulfilment_info(self) -> str:
        return f"Instant digital download. File size: {self.download_size} MB"

class Inventory:
    def __init__(self):
        self.products: list[Product] = [] # it is a list type with items of Product type inside because they are Product objects

    def add_product(self, product: Product) -> None: # the product added is of Product type
        self.products.append(product) # why is this variable public which is different from the rest?

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.product_id == product_id: # explain how the @property works here to be able to use "product.price"
                return product
        return None

    def display_all(self) -> None: # still kinda don't get why it's None here
        print("===== Current Inventory =====")
        for product in self.products:
            product.display_information()

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Order line quantity must be greater than zero.")
        self.product = product
        self.quantity = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float) -> None:
        if not (0 <= percent <= 100):
            raise ValueError("Percentage must be between 0 and 100.")
        self._percentage = percent

    def apply(self, total: float) -> float:
        return (1 - self._percentage / 100.0) * total

class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, discount_amount: float):
        self.threshold = threshold
        self.discount_amount = discount_amount

    def apply(self, total: float) -> float:
        return (total - self.discount_amount) if total >= self.threshold else total

class StudentDiscount(DiscountStrategy):
    def __init__(self, fixed_rebate: float = 15.0):
        self.fixed_rebate = fixed_rebate

    def apply(self, total: float) -> float:
        return max(0.0, total - self.fixed_rebate)

class ProductFactory:
    # what is a static method?

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, extra_val: float = 0.0) -> Product:
        ptype = product_type.strip().lower()

        if ptype == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, weight=extra_val)

        elif ptype == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, download_size=extra_val)

        else:
            raise ValueError(f"Unknown product type: '{product_type}'")

class Order:
    def __init__(self, order_id: str, discount_strategy: DiscountStrategy | None = None):
        self.order_id = order_id
        self.order_lines: list[OrderLine] = [] # this is an example of composition
        self._discount: DiscountStrategy = discount_strategy if discount_strategy is not None else NoDiscount()

    def set_discount(self, discount_strategy: DiscountStrategy) -> None:
        self._discount = discount_strategy

    def add_order_line(self, product: Product, quantity: int) -> None:
        line = OrderLine(product, quantity)
        self.order_lines.append(line)

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self._discount.apply(total) # polymorphic delegation


supplier = Supplier("S1", "Acme", "acme@example.com")
desk_lamp = ProductFactory.create("physical", "P1", "Desk Lamp", 50.0, 10, supplier, 1.5)
photo_editor = ProductFactory.create("digital", "D1", "Photo Editor", 100.0, 100, supplier, 250)

order = Order("O1", BulkDiscount(200, 20))
order.add_order_line(desk_lamp, 1)      # 1 x 50  =  50
order.add_order_line(photo_editor, 2)   # 2 x 100 = 200

print(f"Total before any discount: {sum(l.calculate_subtotal() for l in order.order_lines):.2f}")
print(f"BulkDiscount(200, 20):      {order.calculate_total():.2f}")

order.set_discount(PercentageDiscount(10))
print(f"PercentageDiscount(10):     {order.calculate_total():.2f}")

def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")

# price = get_positive_float("Enter a price: ")
# print(f"Returned: {price}")

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            loaded = 0
            for row in reader:
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock), supplier)
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as error:
                    print(f"Skipping row {reader.line_num}: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
inventory = Inventory()
load_products("products.csv", inventory, supplier)
inventory.display_all()
