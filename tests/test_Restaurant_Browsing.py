import unittest
from unittest import mock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Restaurant_Browsing import RestaurantBrowsing, RestaurantDatabase, RestaurantSearch

class TestRestaurantBrowsing(unittest.TestCase):
    """
    Unit tests for the RestaurantBrowsing class, testing various search functionalities.
    """

    def setUp(self):
        # """
        # Set up the test case by initializing a RestaurantDatabase and RestaurantBrowsing instance.
        # """
        # self.database = RestaurantDatabase()
        # self.browsing = RestaurantBrowsing(self.database)

        """
        Set up the test case by initializing a mock and stubb for RestaurantDatabase
        """
        # Stubbs the RestaurantDatabase
        self.database = mock.MagicMock()
        self.database.get_restaurants.return_value = [
            {"name": "Pekan pitsa","cuisine": "Pizza", "location": "NYC", "phonenumber": "123-456", "rating": 4.5},
            {"name": "Pirjon pitsa","cuisine": "Italian", "location": "LA", "phonenumber": "987-654", "rating": 4.5},
            {"name": "Pirjon pitsa","cuisine": "Italian", "location": "Downtown", "phonenumber": "987-654", "rating": 3.0},
            {"name": "Kallen pitsa","cuisine": "Finlandian", "location": "Kannus", "phonenumber": "987-654", "rating": 5.0},
            {"name": "Italian Bistro","cuisine": "Italian Bistro", "location": "Downtown", "phonenumber": "987-654", "rating": 4.0}
        ]
        
        # Creates a RestaurantBrowsing-object
        self.browsing = RestaurantBrowsing(self.database)


    def test_search_by_cuisine(self):
        """
        Test searching for restaurants by cuisine type.
        """
        results = self.browsing.search_by_cuisine("Italian")
        self.assertEqual(len(results), 2)  # There should be 2 Italian restaurants
        self.assertTrue(all([restaurant['cuisine'] == "Italian" for restaurant in results]))  # Check if all returned restaurants are Italian

    def test_search_by_location(self):
        """
        Test searching for restaurants by location.
        """
        results = self.browsing.search_by_location("Downtown")
        self.assertEqual(len(results), 2)  # There should be 2 restaurants located Downtown
        self.assertTrue(all([restaurant['location'] == "Downtown" for restaurant in results]))  # Check if all returned restaurants are in Downtown

    def test_search_by_rating(self):
        """
        Test searching for restaurants by minimum rating.
        """
        results = self.browsing.search_by_rating(4.0)
        self.assertEqual(len(results), 4)  # There should be 4 restaurants with a rating >= 4.0
        self.assertTrue(all([restaurant['rating'] >= 4.0 for restaurant in results]))  # Check if all returned restaurants have a rating >= 4.0

    def test_search_by_filters(self):
        """
        Test searching for restaurants by multiple filters (cuisine type, location, and minimum rating).
        """
        results = self.browsing.search_by_filters(cuisine_type="Italian", location="Downtown", min_rating=4.0)
        self.assertEqual(len(results), 1)  # Only one restaurant should match all the filters
        self.assertEqual(results[0]['name'], "Italian Bistro")  # The result should be "Italian Bistro"

    def test_search_by_partial_search_filters(self):
        """
        Test searching for restaurants by multiple filters (partially words) (cuisine type, location, and minimum rating).
        """
        results = self.browsing.search_by_filters(cuisine_type="Itali", location="Downtown", min_rating=4.0)
        self.assertGreater(len(results), 0, "Expected at least one result")
        results = self.browsing.search_by_filters(cuisine_type="Itali", location="Downto", min_rating=4.0)
        self.assertGreater(len(results), 0, "Expected at least one result")
        results = self.browsing.search_by_filters(cuisine_type="ali", location="ownto", min_rating=4.0)
        self.assertGreater(len(results), 0, "Expected at least one result")

    def test_search_filters_rating(self):
        """
        Test searching for restaurants by only rating filter.
        """
        results = self.browsing.search_by_filters(cuisine_type=None, location=None, min_rating=4.0)
        for restaurant in results:
            self.assertGreaterEqual(restaurant['rating'], 4.0, f"Expected rating to be >= 4.0 for restaurant {restaurant['name']}")
        results = self.browsing.search_by_filters(cuisine_type=None, location=None, min_rating=2)
        for restaurant in results:
            self.assertGreaterEqual(restaurant['rating'], 2.0, f"Expected rating to be >= 4.0 for restaurant {restaurant['name']}")

    def test_search_filter_rating_with_none_value(self):
        """
        Test searching for restaurants by only rating filter with none value.
        """
        results = self.browsing.search_by_filters(cuisine_type=None, location=None, min_rating=None)
        self.assertGreater(len(results), 0, "Expected at least one result")

if __name__ == '__main__':
    unittest.main()
