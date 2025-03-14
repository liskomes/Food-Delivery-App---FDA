import unittest
from unittest import mock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Order_Placement import OrderPlacement, Cart, UserProfile, RestaurantMenu, CartItem, PaymentMethod

class TestOrderPlacement(unittest.TestCase):
    """Integration tests."""

if __name__ == "__main__":
    unittest.main()