import unittest
from unittest import mock
import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
from unittest.mock import MagicMock, patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Order_Placement import OrderPlacement, Cart, UserProfile, RestaurantMenu, CartItem, PaymentMethod
from main import LoginFrame, Application, CheckoutPopup

class TestModuleIntegrations(unittest.TestCase):
    """Integration tests."""
    def setUp(self):
        self.app = Application()
        self.app.show_login_frame()
        self.login_frame = self.app.current_frame

        # Mock user data
        self.app.registration.users = {
            "testuser@example.com": {"password": "password123"}
        }

       

    def test_successful_login(self):
        self.login_frame.email_entry.insert(0, "testuser@example.com")
        self.login_frame.pass_entry.insert(0, "password123")
        self.login_frame.login()

        # Check if the user is logged in and the main app frame is shown
        self.assertEqual(self.app.logged_in_email, "testuser@example.com")
        #self.assertIsInstance(self.app.current_frame, MainAppFrame)

    def test_unsuccessful_login(self):
        self.login_frame.email_entry.insert(0, "wronguser@example.com")
        self.login_frame.pass_entry.insert(0, "wrongpassword")

        with mock.patch('tkinter.messagebox.showerror') as mock_showerror:
            self.login_frame.login()
            mock_showerror.assert_called_once_with("Error", "Invalid email or password")

        # Check if the user is not logged in and the login frame is still shown
        self.assertIsNone(self.app.logged_in_email)
        self.assertIsInstance(self.app.current_frame, LoginFrame)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_checkout_success(self, mock_showerror, mock_showinfo):
        self.app.login_user("testuser@example.com")
        self.main_frame = self.app.current_frame

        # Mock order placement
        self.cart = Cart()
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.order_placement = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)

        # Add items to cart
        self.cart.add_item("Pizza", 10.0, 2)
        # Mock the order placement confirmation
        self.order_placement.confirm_order = MagicMock(return_value={"success": True, "order_id": "12345", "estimated_delivery": "30 minutes"})

        # Create the checkout popup
        checkout_popup = CheckoutPopup(self.main_frame, self.order_placement)
        checkout_popup.payment_method.set("credit_card")
        checkout_popup.card_entry.insert(0, "1234567812345678")

        # Simulate confirming the order
        checkout_popup.confirm_order()

        # Check if the success message box was shown
        mock_showinfo.assert_called_once_with("Order Confirmed", "Order ID: 12345\nEstimated Delivery: 30 minutes")
        mock_showerror.assert_not_called()

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_checkout_failure(self, mock_showerror, mock_showinfo):
        self.app.login_user("testuser@example.com")
        self.main_frame = self.app.current_frame

        # Mock order placement
        self.cart = Cart()
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.order_placement = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)

        # Add items to cart
        self.cart.add_item("Pizza", 10.0, 2)
        # Mock the order placement confirmation
        self.order_placement.confirm_order = MagicMock(return_value={"success": False, "message": "Payment failed"})

        # Create the checkout popup
        checkout_popup = CheckoutPopup(self.main_frame, self.order_placement)
        checkout_popup.payment_method.set("credit_card")
        checkout_popup.card_entry.insert(0, "1234567812345678")

        # Simulate confirming the order
        checkout_popup.confirm_order()

        # Check if the error message box was shown
        mock_showerror.assert_called_once_with("Error", "Payment failed")
        mock_showinfo.assert_not_called()


if __name__ == "__main__":
    unittest.main()