import unittest
from unittest import mock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Order_Placement import OrderPlacement, Cart, UserProfile, RestaurantMenu, CartItem, PaymentMethod

class TestOrderPlacement(unittest.TestCase):
    """Unit tests for the OrderPlacement class."""

    def setUp(self):
        """Sets up the test environment by creating instances of necessary classes."""
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.cart = Cart()
        self.order = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)

    def test_validate_order_empty_cart(self):
        """Test case for validating an order with an empty cart."""
        result = self.order.validate_order()
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Cart is empty")

    def test_validate_order_item_not_available(self):
        """Test case for validating an order with an unavailable item."""
        self.cart.add_item("Pasta", 15.99, 1)
        result = self.order.validate_order()
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Pasta is not available")

    def test_validate_order_success(self):
        """Test case for successfully validating an order."""
        self.cart.add_item("Burger", 8.99, 2)
        result = self.order.validate_order()
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order is valid")

    def test_validate_multiple_order_success(self):
        """Test case for multiple orders."""
        self.cart.add_item("Burger", 8.99, 2)
        self.cart.add_item("Burger", 8.99, 1)  # Oletamme, että tämä lisää määrän olemassa olevaan tuotteeseen
        self.cart.add_item("Pizza", 12.99, 1)
        self.cart.add_item("Pizza", 12.99, 15)
        self.cart.add_item("Pizza", 12.99, 1)

        result = self.order.validate_order()

        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order is valid")

        # Varmistetaan, että samat tuotteet yhdistyvät eikä niitä lisätä erillisinä riveinä
        self.assertEqual(len(self.cart.items), 2)  # Oletamme, että tuotteet yhdistyvät oikein

        # Etsitään oikeat tuotteet listasta
        burger = next(item for item in self.cart.items if item.name == "Burger")
        pizza = next(item for item in self.cart.items if item.name == "Pizza")

        self.assertEqual(burger.quantity, 3)  # Varmistetaan, että Burger-määrä on 4
        self.assertEqual(pizza.quantity, 17)

    def test_confirm_order_success(self):
        """Test case for confirming an order with successful payment."""
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()
        result = self.order.confirm_order(payment_method)
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order confirmed")
        self.assertEqual(result["order_id"], "ORD123456")

    def test_confirm_order_failed_payment(self):
        """Test case for confirming an order with failed payment."""
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()

        # Use unittest.mock.patch to simulate failed payment processing.
        with mock.patch.object(payment_method, 'process_payment', return_value=False):
            result = self.order.confirm_order(payment_method)
            self.assertFalse(result["success"])
            self.assertEqual(result["message"], "Payment failed")

    def test_get_subtotal(self):
        """Test case for calculating subtotal of a CartItem."""
        item = CartItem("Burger", 8.99, 3)
        self.assertEqual(item.get_subtotal(), 26.97)  # 8.99 * 3 = 26.97

if __name__ == "__main__":
    unittest.main()