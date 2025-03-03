class RestaurantBrowsing:
    """
    A class for browsing restaurants in a database based on various criteria like cuisine type, location, and rating.
    
    Attributes:
        database (RestaurantDatabase): An instance of RestaurantDatabase that holds restaurant data.
    """

    def __init__(self, database):
        """
        Initialize RestaurantBrowsing with a reference to a restaurant database.
        
        Args:
            database (RestaurantDatabase): The database object containing restaurant information.
        """
        self.database = database

    def search_by_cuisine(self, cuisine_type):
        """
        Search for restaurants based on their cuisine type.
        
        Args:
            cuisine_type (str): The type of cuisine to filter by (e.g., "Italian").
        
        Returns:
            list: A list of restaurants that match the given cuisine type.
        """
        return [restaurant for restaurant in self.database.get_restaurants() 
                if restaurant['cuisine'].lower() == cuisine_type.lower()]

    def search_by_location(self, location):
        """
        Search for restaurants based on their location.
        
        Args:
            location (str): The location to filter by (e.g., "Downtown").
        
        Returns:
            list: A list of restaurants that are located in the specified area.
        """
        return [restaurant for restaurant in self.database.get_restaurants() 
                if restaurant['location'].lower() == location.lower()]

    def search_by_rating(self, min_rating):
        """
        Search for restaurants based on their minimum rating.
        
        Args:
            min_rating (float): The minimum acceptable rating to filter by (e.g., 4.0).
        
        Returns:
            list: A list of restaurants that have a rating greater than or equal to the specified rating.
        """
        return [restaurant for restaurant in self.database.get_restaurants() 
                if restaurant['rating'] >= min_rating]

    def search_by_filters(self, cuisine_type=None, location=None, min_rating=None):
        """
        Search for restaurants based on multiple filters: cuisine type, location, and/or rating.
        
        Args:
            cuisine_type (str, optional): The type of cuisine to filter by.
            location (str, optional): The location to filter by.
            min_rating (float, optional): The minimum acceptable rating to filter by.
        
        Returns:
            list: A list of restaurants that match all specified filters.
        """
        results = self.database.get_restaurants()  # Start with all restaurants

        if cuisine_type:
            results = [restaurant for restaurant in results 
                       if cuisine_type.lower() in restaurant['cuisine'].lower()]

        if location:
            results = [restaurant for restaurant in results 
                       if location.lower() in restaurant['location'].lower()]

        if min_rating:
            results = [restaurant for restaurant in results 
                       if restaurant['rating'] >= min_rating]

        return results


class RestaurantDatabase:
    """
    A simulated in-memory database that stores restaurant information.
    
    Attributes:
        restaurants (list): A list of dictionaries, where each dictionary represents a restaurant with
                            fields like name, cuisine, location, rating, price range, and delivery status.
    """

    def __init__(self):
        """
        Initialize the RestaurantDatabase with a predefined set of restaurant data.
        """
        self.restaurants = [
            {"name": "Italian Bistro", "cuisine": "Italian", "location": "Downtown","phonenumber": "+535 836 7284", "rating": 4.5, 
             "price_range": "$$", "delivery": True},
            {"name": "Sushi House", "cuisine": "Japanese", "location": "Midtown","phonenumber": "+535 739 9483", "rating": 4.8, 
             "price_range": "$$$", "delivery": False},
            {"name": "Burger King", "cuisine": "Fast Food", "location": "Uptown","phonenumber": "+535 824 9274", "rating": 4.0, 
             "price_range": "$", "delivery": True},
            {"name": "Taco Town", "cuisine": "Mexican", "location": "Downtown","phonenumber": "+535 123 4325", "rating": 4.2, 
             "price_range": "$", "delivery": True},
            {"name": "Pizza Palace", "cuisine": "Italian", "location": "Uptown","phonenumber": "+535 223 5535", "rating": 3.9, 
             "price_range": "$$", "delivery": True}
        ]

    def get_restaurants(self):
        """
        Retrieve the list of restaurants in the database.
        
        Returns:
            list: A list of dictionaries, where each dictionary contains restaurant information.
        """
        return self.restaurants


class RestaurantSearch:
    """
    A class that interfaces with RestaurantBrowsing to perform restaurant searches based on user input.
    
    Attributes:
        browsing (RestaurantBrowsing): An instance of RestaurantBrowsing used to perform searches.
    """

    def __init__(self, browsing):
        """
        Initialize the RestaurantSearch with a reference to a RestaurantBrowsing instance.
        
        Args:
            browsing (RestaurantBrowsing): An instance of the RestaurantBrowsing class.
        """
        self.browsing = browsing

    def search_restaurants(self, cuisine=None, location=None, rating=None):
        """
        Search for restaurants using multiple optional filters: cuisine, location, and rating.
        
        Args:
            cuisine (str, optional): The type of cuisine to filter by.
            location (str, optional): The location to filter by.
            rating (float, optional): The minimum rating to filter by.
        
        Returns:
            list: A list of restaurants that match the provided search criteria.
        """
        results = self.browsing.search_by_filters(cuisine_type=cuisine, location=location, min_rating=rating)
        return results
    