import unittest
from unittest import mock
import unittest
from unittest.mock import MagicMock
from tkinter import ttk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import Application, StartupFrame, RegisterFrame, LoginFrame, MainAppFrame, AddItemPopup, CartViewPopup, CheckoutPopup
from Order_Placement import OrderPlacement, Cart, UserProfile, RestaurantMenu, CartItem, PaymentMethod
from Payment_Processing import PaymentProcessing
from Restaurant_Browsing import RestaurantBrowsing, RestaurantDatabase, RestaurantSearch
from User_Registration import UserRegistration

# Unit tests for OrderPlacement class
class TestMain(unittest.TestCase):
    def setUp(self):
        """Set up the test case by initializing a MainAppFrame instance."""
        self.app = Application()
        self.app.show_login_frame()
        
        # Login by user
        self.app.login_user("testuser@example.com")
        
        # Wait for UI to be loaded and shows then mainappframe, get results_tree component
        self.main_frame = self.app.current_frame
        self.results_tree = self.main_frame.results_tree

        """Set up the test case by initializing the cart and adding sample items."""
        self.cart = Cart()

    def test_main_table_columns(self):
        """Test case for validating amount of columns and that columns are the same."""
        expected_columns = ("cuisine", "location","phonenumber", "rating")
        actual_columns = self.results_tree["columns"]
        
        # Check that the number of columns is the same
        self.assertEqual(len(actual_columns), len(expected_columns))
        # Check that columns are the same
        self.assertListEqual(list(actual_columns), list(expected_columns))
    

    def test_remove_item_existing(self):
        """Test that removing an existing item from the cart works correctly."""
        # Add an item to the cart
        self.cart.add_item("Pizza", 12.99, 2)
        
        # Remove the item from the cart
        self.cart.remove_item("Pizza")
        
        # Check that the item is no longer in the cart
        remaining_items = [item.name for item in self.cart.items]
        self.assertNotIn("Pizza", remaining_items)
    
    def test_remove_item_empty_cart(self):
        """Test that attempting to remove an item from an empty cart does not break the program."""
        self.cart.items = []
        # Try to remove an item
        self.cart.remove_item("Pizza")  
        # Make sure the cart remains empty (should still contain 0 items)
        self.assertEqual(len(self.cart.items), 0)

import unittest
from unittest.mock import MagicMock
from tkinter import ttk
from main import MainAppFrame, Application

class TestSortByRating(unittest.TestCase):
    def setUp(self):
        self.app = Application()
        self.app.login_user("testuser@example.com")
        self.main_frame = self.app.current_frame
        self.main_frame.sort_ascending = True  # Asetetaan oletusjärjestys nousevaksi
        self.results_tree = self.main_frame.results_tree
        self.results_tree.get_children = MagicMock()
        self.results_tree.item = MagicMock()
        self.results_tree.move = MagicMock()

    def test_sort_by_rating_ascending(self):
    # Simuloidaan Treeviewin tietoja
        self.results_tree.get_children.return_value = ["id1", "id2", "id3"]
        self.results_tree.item.side_effect = lambda x, option: {
            "id1": ("Pizza", "NYC", "123-456", "3.5"),
            "id2": ("Burger", "LA", "987-654", "4.5"),
            "id3": ("Salad", "SF", "555-111", "2.0"),
        }[x]
        
        # Kutsutaan testattavaa metodia
        self.main_frame.sort_by_rating()

        print("Sort ascending:", self.main_frame.sort_ascending)
        print("Move calls:", self.results_tree.move.mock_calls)
        
        # Tarkistetaan, että arvot järjestetään oikein nousevasti
        self.results_tree.move.assert_any_call("id2", "", 0)
        self.results_tree.move.assert_any_call("id1", "", 1)
        self.results_tree.move.assert_any_call("id3", "", 2)
        self.assertFalse(self.main_frame.sort_ascending)  # Tarkistetaan, että suunta vaihtui

    
    def test_sort_by_rating_descending(self):
        self.main_frame.sort_ascending = False  # Vaihdetaan järjestys laskevaksi
        self.results_tree.get_children.return_value = ["id1", "id2", "id3"]
        self.results_tree.item.side_effect = lambda x, option: {
            "id1": ("Pizza", "NYC", "123-456", "3.5"),
            "id2": ("Burger", "LA", "987-654", "4.5"),
            "id3": ("Salad", "SF", "555-111", "2.0"),
        }[x]
        
        # Kutsutaan testattavaa metodia
        self.main_frame.sort_by_rating()
        
        # Tarkistetaan, että arvot järjestetään oikein laskevasti
        self.results_tree.move.assert_any_call("id3", "", 0)
        self.results_tree.move.assert_any_call("id1", "", 1)
        self.results_tree.move.assert_any_call("id2", "", 2)
        self.assertTrue(self.main_frame.sort_ascending)  # Tarkistetaan, että suunta vaihtui takaisin

if __name__ == "__main__":
    unittest.main()
