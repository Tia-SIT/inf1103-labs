import contextlib
import inspect
import io
import os
import tempfile
import unittest
from unittest.mock import patch

# If your file has a different name (e.g. tia_oop_revision.py), change "lab9" here.
from lab9 import (
    BulkDiscount, DigitalProduct, DiscountStrategy, Inventory, Order,
    OrderLine, PercentageDiscount, PhysicalProduct, Product, ProductFactory,
    StudentDiscount, Supplier, get_positive_float, load_products,
)



LAB_CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""

def capture(func, *args, **kwargs):
    """Run func, return (its result, everything it printed)."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args, **kwargs)
    return result, buffer.getvalue()

def make_supplier():
    return Supplier("S1", "Acme", "acme@example.com")

def make_order_totalling_250(discount=None):
    supplier = make_supplier()
    lamp = ProductFactory.create("physical", "P1", "Desk Lamp", 50.0, 10, supplier, 1.5)
    editor = ProductFactory.create("digital", "D1", "Photo Editor", 100.0, 100, supplier, 250)
    order = Order("O1", discount)
    order.add_order_line(lamp, 1)     # 50
    order.add_order_line(editor, 2)   # 200
    return order

class RecordingStrategy(DiscountStrategy):
    """A stand-in strategy that remembers what Order passed to it."""
    def __init__(self):
        self.received_total = None

    def apply(self, total: float) -> float:
        self.received_total = total
        return 42.0

class HalfPriceDiscount(DiscountStrategy):
    """A brand-new strategy, defined here without touching Order."""
    def apply(self, total: float) -> float:
        return total / 2

class TestOrderUsesDiscountStrategy(unittest.TestCase):
    def test_total_goes_through_the_strategy(self):
        strategy = RecordingStrategy()
        order = make_order_totalling_250(strategy)
        self.assertEqual(order.calculate_total(), 42.0)         # strategy's answer is returned
        self.assertEqual(strategy.received_total, 250.0)        # it received the raw line total

    def test_default_strategy_is_no_discount(self):
        self.assertEqual(make_order_totalling_250().calculate_total(), 250.0)

    def test_order_contains_no_discount_if_elif_logic(self):
        order_source = inspect.getsource(Order)
        self.assertNotIn("elif", order_source)
        for name in ("PercentageDiscount", "BulkDiscount", "StudentDiscount"):
            self.assertNotIn(name, order_source)
        total_source = inspect.getsource(Order.calculate_total)
        self.assertNotIn(" if ", total_source)

    def test_new_strategy_works_without_changing_order(self):
        order = make_order_totalling_250(HalfPriceDiscount())
        self.assertEqual(order.calculate_total(), 125.0)

    def test_set_discount_changes_strategy_on_existing_order(self):
        order = make_order_totalling_250(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)   # from the raw 250, not stacked

    def test_student_discount(self):
        self.assertEqual(StudentDiscount().apply(250.0), 235.0)
        self.assertEqual(StudentDiscount().apply(10.0), 0.0)     # never goes below zero

class TestProductFactory(unittest.TestCase):
    def test_creates_the_right_child_class(self):
        supplier = make_supplier()
        physical = ProductFactory.create("physical", "P1", "Lamp", 10.0, 5, supplier, 2.0)
        digital = ProductFactory.create("digital", "D1", "Editor", 10.0, 5, supplier, 100)
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertIsInstance(physical, Product)
        self.assertIsInstance(digital, Product)
        self.assertEqual(physical.weight, 2.0)
        self.assertEqual(digital.download_size, 100)

    def test_unknown_type_raises_value_error_with_clear_message(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Install", 30.0, 5, make_supplier())
        self.assertIn("Unknown product type", str(context.exception))
        self.assertIn("service", str(context.exception))

    def test_load_products_creates_products_through_the_factory(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="") as f:
                f.write(LAB_CSV)
            with patch.object(ProductFactory, "create", wraps=ProductFactory.create) as spy:
                capture(load_products, path, Inventory(), make_supplier())
        requested = [call.args[0] for call in spy.call_args_list]
        # The "abc" price row fails on float() before the factory is reached.
        self.assertEqual(requested, ["physical", "digital", "service", "physical"])

class TestValidation(unittest.TestCase):
    def test_invalid_prices_are_rejected(self):
        for bad_price in (0, -1, -0.01):
            with self.subTest(price=bad_price):
                with self.assertRaisesRegex(ValueError, "greater than zero"):
                    ProductFactory.create("physical", "P1", "Lamp", bad_price, 5, make_supplier(), 1.0)

    def test_negative_stock_is_rejected_but_zero_is_allowed(self):
        with self.assertRaisesRegex(ValueError, "negative"):
            ProductFactory.create("digital", "D1", "Editor", 10.0, -1, make_supplier(), 1.0)
        product = ProductFactory.create("digital", "D1", "Editor", 10.0, 0, make_supplier(), 1.0)
        self.assertEqual(product.stock, 0)

    def test_stock_cannot_be_updated_below_zero(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 10.0, 5, make_supplier(), 1.0)
        with self.assertRaisesRegex(ValueError, "negative"):
            product.update_stock(-6)
        self.assertEqual(product.stock, 5)        # unchanged after the rejected update

    def test_invalid_order_quantities_are_rejected(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 10.0, 5, make_supplier(), 1.0)
        for bad_quantity in (0, -1):
            with self.subTest(quantity=bad_quantity):
                with self.assertRaisesRegex(ValueError, "greater than zero"):
                    OrderLine(product, bad_quantity)
                with self.assertRaisesRegex(ValueError, "greater than zero"):
                    Order("O1").add_order_line(product, bad_quantity)
        self.assertEqual(OrderLine(product, 1).quantity, 1)

class TestGetPositiveFloat(unittest.TestCase):
    def test_keeps_asking_until_the_input_is_valid(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as fake_input:
            result, output = capture(get_positive_float, "Enter a price: ")
        self.assertEqual(result, 12.5)
        self.assertEqual(fake_input.call_count, 3)
        self.assertIn("Please enter a valid number", output)
        self.assertIn("Please enter a number greater than zero.", output)

    def test_zero_is_rejected(self):
        with patch("builtins.input", side_effect=["0", "3"]):
            result, output = capture(get_positive_float, "Enter a price: ")
        self.assertEqual(result, 3.0)
        self.assertIn("greater than zero", output)

class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = os.path.join(self.folder.name, "products.csv")

    def write_csv(self, text):
        with open(self.path, "w", newline="") as f:
            f.write(text)

    def test_bad_rows_are_reported_and_skipped_and_valid_rows_load(self):
        self.write_csv(LAB_CSV)
        inventory = Inventory()
        _, output = capture(load_products, self.path, inventory, make_supplier())
        self.assertEqual([p.product_id for p in inventory.products], ["P001", "D001", "P003"])
        self.assertIn("Skipping row 4", output)            # unknown product type
        self.assertIn("Unknown product type", output)
        self.assertIn("Skipping row 5", output)            # price is not a number
        self.assertIn("3 products loaded.", output)
        self.assertTrue(output.rstrip().endswith("Load attempt finished."))

    def test_missing_file_is_handled_gracefully(self):
        inventory = Inventory()
        _, output = capture(load_products, self.path, inventory, make_supplier())  # file never written
        self.assertIn("Products file not found", output)
        self.assertIn("Load attempt finished.", output)
        self.assertNotIn("products loaded", output)
        self.assertEqual(inventory.products, [])

    def test_header_only_file_loads_zero_products(self):
        self.write_csv("product_type,product_id,name,price,stock_quantity")
        inventory = Inventory()
        _, output = capture(load_products, self.path, inventory, make_supplier())
        self.assertIn("0 products loaded.", output)

class TestExceptClausesAreSpecific(unittest.TestCase):
    def test_no_bare_or_broad_except(self):
        for func in (get_positive_float, load_products):
            source = inspect.getsource(func)
            with self.subTest(function=func.__name__):
                self.assertNotIn("except:", source)
                self.assertNotIn("except Exception", source)

if __name__ == "__main__":
    unittest.main()
