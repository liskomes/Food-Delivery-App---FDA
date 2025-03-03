import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

from User_Registration import UserRegistration
from Order_Placement import Cart, OrderPlacement, UserProfile, RestaurantMenu, PaymentMethod
from Payment_Processing import PaymentProcessing
from Restaurant_Browsing import RestaurantDatabase, RestaurantBrowsing

# Utility functions for user data storage
USERS_FILE = "users.json"

def load_users():
    """Loading users from users.json"""
    
    if not os.path.exists(USERS_FILE): #jos ei löyty niin palautetaan tyhjää
        return {}
    with open(USERS_FILE, "r") as f: #avataan f:nä 
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mobile Food Delivery App")
        self.geometry("600x400")

        # Load user registration data from file
        self.user_data = load_users()

        # Initialize core classes
        self.registration = UserRegistration()
        self.registration.users = self.user_data  # Load existing users into registration system

        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)

        # Initially no user logged in
        self.logged_in_email = None

        # Create initial frame
        self.current_frame = None
        self.show_startup_frame()

    def show_startup_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = StartupFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_register_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = RegisterFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_login_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def login_user(self, email):
        self.logged_in_email = email
        # After login, show main app frame
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MainAppFrame(self, email)
        self.current_frame.pack(fill="both", expand=True)


class StartupFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Welcome to the Mobile Food Delivery App", font=("Arial", 16)).pack(pady=30)

        tk.Button(self, text="Register", command=self.go_to_register, width=20).pack(pady=10)
        tk.Button(self, text="Login", command=self.go_to_login, width=20).pack(pady=10)

    def go_to_register(self):
        self.master.show_register_frame()

    def go_to_login(self):
        self.master.show_login_frame()


class RegisterFrame(tk.Frame):
    """Class representing a RegisterFrame"""

    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Register New User", font=("Arial", 14)).pack(pady=20)

        self.email_entry = self.create_entry("Email:")
        self.pass_entry = self.create_entry("Password:", show="*")
        self.conf_pass_entry = self.create_entry("Confirm Password:", show="*")

        tk.Button(self, text="Register", command=self.register_user).pack(pady=10)
        tk.Button(self, text="Back", command=self.go_back).pack()

    def create_entry(self, label_text, show=None):
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, width=15, anchor="e").pack(side="left")
        entry = tk.Entry(frame, show=show)
        entry.pack(side="left")
        return entry

    def register_user(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()
        confirm_password = self.conf_pass_entry.get()

        result = self.master.registration.register(email, password, confirm_password)
        if result["success"]:
            # Save the updated users to file
            save_users(self.master.registration.users)
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.master.show_login_frame()
        else:
            messagebox.showerror("Error", result["error"])

    def go_back(self):
        self.master.show_startup_frame()


class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="User Login", font=("Arial", 14)).pack(pady=20)

        self.email_entry = self.create_entry("Email:")
        self.pass_entry = self.create_entry("Password:", show="*")

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Back", command=self.go_back).pack()

    def create_entry(self, label_text, show=None):
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, width=15, anchor="e").pack(side="left")
        entry = tk.Entry(frame, show=show)
        entry.pack(side="left")
        return entry

    def login(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()
        # Validate login
        # For simplicity, just check if user exists and password matches
        users = self.master.registration.users
        if email in users and users[email]["password"] == password:
            self.master.login_user(email)
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def go_back(self):
        self.master.show_startup_frame()


class MainAppFrame(tk.Frame):
    def __init__(self, master, user_email):
        self.sort_ascending = True
        super().__init__(master)
        tk.Label(self, text=f"Welcome, {user_email}", font=("Arial", 14)).pack(pady=10)

        self.user_email = user_email
        self.database = master.database
        self.browsing = master.browsing

        # Create user's profile and cart
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.cart = Cart()
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.order_placement = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)

        # Search Frame
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Cuisine:").pack(side="left")
        self.cuisine_var = tk.Entry(search_frame)
        self.cuisine_var.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.search_restaurants).pack(side="left")

        tk.Label(search_frame, text="Rating at least:").pack(side="left", padx=5)
        self.num_rating_value = tk.Spinbox(search_frame, from_=0, to=5)
        self.num_rating_value.pack(side="left", padx=5)

        # Results Treeview
        self.results_tree = ttk.Treeview(self, columns=("cuisine", "location","phonenumber", "rating"), show="headings")
        self.results_tree.heading("cuisine", text="Cuisine")
        self.results_tree.heading("location", text="Location")
        self.results_tree.heading("phonenumber", text="Phone number")
        self.results_tree.heading("rating", text="Rating", command=self.sort_by_rating)  #Added sort

        # Define widths and alignment
        self.results_tree.column("cuisine", width=150, anchor="w")
        self.results_tree.column("location", width=150, anchor="w")
        self.results_tree.column("phonenumber", width=150, anchor="w")
        self.results_tree.column("rating", width=100, anchor="w")
        self.results_tree.pack(pady=10, fill="x")

        # Buttons for actions
        action_frame = tk.Frame(self)
        action_frame.pack(pady=5)
        tk.Button(action_frame, text="View All Restaurants", command=self.view_all_restaurants).pack(side="left", padx=5)
        tk.Button(action_frame, text="Add Item to Cart", command=self.add_item_to_cart).pack(side="left", padx=5)
        tk.Button(action_frame, text="View Cart", command=self.view_cart).pack(side="left", padx=5)
        tk.Button(action_frame, text="Checkout", command=self.checkout).pack(side="left", padx=5)

    def sort_by_rating(self):
        items = [(self.results_tree.item(child, "values"), child) for child in self.results_tree.get_children()]
    
        # Järjestetään arvostelun mukaan, käännetään tarvittaessa
        sorted_items = sorted(items, key=lambda x: float(x[0][3]), reverse=self.sort_ascending)
    
        # Päivitetään järjestys
        for index, (values, child) in enumerate(sorted_items):
            self.results_tree.move(child, "", index)
    
        # Vaihdetaan järjestyssuuntaa seuraavaa klikkausta varten
        self.sort_ascending = not self.sort_ascending

    def search_restaurants(self):
        self.results_tree.delete(*self.results_tree.get_children())
        cuisine = self.cuisine_var.get().strip()
        rating = self.num_rating_value.get().strip()
        try:
            rating = float(rating)
        except ValueError:
            rating = None
        results = self.browsing.search_by_filters(cuisine_type=cuisine if cuisine else None, min_rating=rating)
        for r in results:
            self.results_tree.insert("", "end", values=(r["cuisine"], r["location"], r["phonenumber"], r["rating"]))

    def view_all_restaurants(self):
        self.results_tree.delete(*self.results_tree.get_children())
        results = self.database.get_restaurants()
        for r in results:
            self.results_tree.insert("", "end", values=(r["cuisine"], r["location"], r["phonenumber"], r["rating"]))

    def add_item_to_cart(self):
        # For simplicity, let's assume user always adds "Pizza"
        # A more sophisticated approach: Let user select from menu items.
        # We will show a small popup to choose items.
        menu_popup = AddItemPopup(self, self.restaurant_menu, self.cart)
        self.wait_window(menu_popup)

    def view_cart(self):
        cart_view = CartViewPopup(self, self.cart)
        self.wait_window(cart_view)

    def checkout(self):
        # Validate order and proceed if valid
        validation = self.order_placement.validate_order()
        if not validation["success"]:
            messagebox.showerror("Error", validation["message"])
            return

        # Show Checkout Popup
        checkout_popup = CheckoutPopup(self, self.order_placement)
        self.wait_window(checkout_popup)


class AddItemPopup(tk.Toplevel):
    def __init__(self, master, menu, cart):
        super().__init__(master)
        self.title("Add Item to Cart")
        self.menu = menu
        self.cart = cart

        tk.Label(self, text="Select an item to add to cart:").pack(pady=10)

        self.item_var = tk.StringVar()
        self.item_var.set(self.menu.available_items[0] if self.menu.available_items else "")
        tk.OptionMenu(self, self.item_var, *self.menu.available_items).pack(pady=5)

        tk.Label(self, text="Quantity:").pack()
        self.qty_entry = tk.Entry(self)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(pady=5)

        tk.Button(self, text="Add to Cart", command=self.add_to_cart).pack(pady=10)

    def add_to_cart(self):
        item = self.item_var.get()
        qty = int(self.qty_entry.get())
        price = 10.0  # Static price for simplicity
        msg = self.cart.add_item(item, price, qty)
        messagebox.showinfo("Cart", msg)
        self.destroy()


class CartViewPopup(tk.Toplevel):
    def __init__(self, master, cart):
        super().__init__(master)
        self.title("Cart Items")

        self.cart = cart
        items = self.cart.view_cart()

        self.update_cart_view(items=items)
        
    def update_cart_view(self, items):
        if not items:
            tk.Label(self, text="Your cart is empty").pack(pady=20)
        else:
            for i in items:
                # Create a frame for each item to contain the label and button
                item_frame = tk.Frame(self)
                item_frame.pack(pady=5, anchor="w")  # Adjust padding as needed

                # Create label for the item
                item_label = tk.Label(item_frame, text=f"{i['name']} x{i['quantity']} = ${i['subtotal']:.2f}")
                item_label.pack(side="left", padx=10)

                # Create a "Remove" button for the item
                remove_button = tk.Button(item_frame, text="Remove", command=lambda item=i: self.remove_item(item))
                remove_button.pack(side="left")

    def remove_item(self, item):
        for cart_item in self.cart.items:
            if cart_item.name == item['name'] and cart_item.quantity == item['quantity']:
                print(f"Removing {cart_item.name} from cart.")
                self.master.cart.items.remove(cart_item) 
                self.update_cart_view(items = self.cart.items)
                self.destroy()
                break


class CheckoutPopup(tk.Toplevel):
    def __init__(self, master, order_placement):
        super().__init__(master)
        self.title("Checkout")
        self.order_placement = order_placement

        order_data = order_placement.proceed_to_checkout()
        tk.Label(self, text="Review your order:", font=("Arial", 12)).pack(pady=10)

        # Show items
        for item in order_data["items"]:
            tk.Label(self, text=f"{item['name']} x{item['quantity']} = ${item['subtotal']:.2f}").pack()

        total = order_data["total_info"]
        tk.Label(self, text=f"Subtotal: ${total['subtotal']:.2f}").pack()
        tk.Label(self, text=f"Tax: ${total['tax']:.2f}").pack()
        tk.Label(self, text=f"Delivery Fee: ${total['delivery_fee']:.2f}").pack()
        tk.Label(self, text=f"Total: ${total['total']:.2f}").pack()

        tk.Label(self, text=f"Delivery Address: {order_data['delivery_address']}").pack(pady=5)

        # Payment method selection
        tk.Label(self, text="Payment Method:").pack(pady=5)
        self.payment_method = tk.StringVar()
        self.payment_method.set("credit_card")
        tk.Radiobutton(self, text="Credit Card", variable=self.payment_method, value="credit_card").pack()
        tk.Radiobutton(self, text="Paypal", variable=self.payment_method, value="paypal").pack()

        tk.Label(self, text="For credit card enter a 16-digit card number:").pack(pady=5)
        self.card_entry = tk.Entry(self)
        self.card_entry.insert(0, "1234567812345678")
        self.card_entry.pack(pady=5)

        tk.Button(self, text="Confirm Order", command=self.confirm_order).pack(pady=10)

    def confirm_order(self):
        # Process order confirmation with the given payment method
        payment_method_obj = PaymentMethod()  # Mock payment method handling in the old code
        # Actually, we have PaymentProcessing class. Let's just rely on PaymentMethod for simplicity here.
        # If you wanted to use PaymentProcessing, you could do so by integrating it as well.
        # For now, we'll simulate PaymentMethod.process_payment by checking if total > 0.
        # In a full scenario, integrate PaymentProcessing similarly.

        # Confirm the order
        result = self.order_placement.confirm_order(payment_method_obj)
        if result["success"]:
            messagebox.showinfo("Order Confirmed", f"Order ID: {result['order_id']}\nEstimated Delivery: {result['estimated_delivery']}")
            self.destroy()
        else:
            messagebox.showerror("Error", result["message"])


if __name__ == "__main__":
    app = Application()
    app.mainloop()

# import unittest
# # Unit tests for OrderPlacement class
# class TestMain(unittest.TestCase):
#     def setUp(self):
#         """Set up the test case by initializing a MainAppFrame instance."""
#         self.app = Application()
#         self.app.show_login_frame()
        
#         # Login by user
#         self.app.login_user("testuser@example.com")
        
#         # Wait for UI to be loaded and shows then mainappframe, get results_tree component
#         self.main_frame = self.app.current_frame
#         self.results_tree = self.main_frame.results_tree

#         """Set up the test case by initializing the cart and adding sample items."""
#         self.cart = Cart()

#     def test_main_table_columns(self):
#         """Test case for validating amount of columns and that columns are the same."""
#         expected_columns = ("cuisine", "location","phonenumber", "rating")
#         actual_columns = self.results_tree["columns"]
        
#         # Check that the number of columns is the same
#         self.assertEqual(len(actual_columns), len(expected_columns))
#         # Check that columns are the same
#         self.assertListEqual(list(actual_columns), list(expected_columns))
    

#     def test_remove_item_existing(self):
#         """Test that removing an existing item from the cart works correctly."""
#         # Add an item to the cart
#         self.cart.add_item("Pizza", 12.99, 2)
        
#         # Remove the item from the cart
#         self.cart.remove_item("Pizza")
        
#         # Check that the item is no longer in the cart
#         remaining_items = [item.name for item in self.cart.items]
#         self.assertNotIn("Pizza", remaining_items)
    
#     def test_remove_item_empty_cart(self):
#         """Test that attempting to remove an item from an empty cart does not break the program."""
#         self.cart.items = []
#         # Try to remove an item
#         self.cart.remove_item("Pizza")  
#         # Make sure the cart remains empty (should still contain 0 items)
#         self.assertEqual(len(self.cart.items), 0)

# import unittest
# from unittest.mock import MagicMock
# from tkinter import ttk
# from main import MainAppFrame, Application

# class TestSortByRating(unittest.TestCase):
#     def setUp(self):
#         self.app = Application()
#         self.app.login_user("testuser@example.com")
#         self.main_frame = self.app.current_frame
#         self.main_frame.sort_ascending = True  # Asetetaan oletusjärjestys nousevaksi
#         self.results_tree = self.main_frame.results_tree
#         self.results_tree.get_children = MagicMock()
#         self.results_tree.item = MagicMock()
#         self.results_tree.move = MagicMock()

#     def test_sort_by_rating_ascending(self):
#     # Simuloidaan Treeviewin tietoja
#         self.results_tree.get_children.return_value = ["id1", "id2", "id3"]
#         self.results_tree.item.side_effect = lambda x, option: {
#             "id1": ("Pizza", "NYC", "123-456", "3.5"),
#             "id2": ("Burger", "LA", "987-654", "4.5"),
#             "id3": ("Salad", "SF", "555-111", "2.0"),
#         }[x]
        
#         # Kutsutaan testattavaa metodia
#         self.main_frame.sort_by_rating()

#         print("Sort ascending:", self.main_frame.sort_ascending)
#         print("Move calls:", self.results_tree.move.mock_calls)
        
#         # Tarkistetaan, että arvot järjestetään oikein nousevasti
#         self.results_tree.move.assert_any_call("id2", "", 0)
#         self.results_tree.move.assert_any_call("id1", "", 1)
#         self.results_tree.move.assert_any_call("id3", "", 2)
#         self.assertFalse(self.main_frame.sort_ascending)  # Tarkistetaan, että suunta vaihtui

    
#     def test_sort_by_rating_descending(self):
#         self.main_frame.sort_ascending = False  # Vaihdetaan järjestys laskevaksi
#         self.results_tree.get_children.return_value = ["id1", "id2", "id3"]
#         self.results_tree.item.side_effect = lambda x, option: {
#             "id1": ("Pizza", "NYC", "123-456", "3.5"),
#             "id2": ("Burger", "LA", "987-654", "4.5"),
#             "id3": ("Salad", "SF", "555-111", "2.0"),
#         }[x]
        
#         # Kutsutaan testattavaa metodia
#         self.main_frame.sort_by_rating()
        
#         # Tarkistetaan, että arvot järjestetään oikein laskevasti
#         self.results_tree.move.assert_any_call("id3", "", 0)
#         self.results_tree.move.assert_any_call("id1", "", 1)
#         self.results_tree.move.assert_any_call("id2", "", 2)
#         self.assertTrue(self.main_frame.sort_ascending)  # Tarkistetaan, että suunta vaihtui takaisin

# if __name__ == "__main__":
#     unittest.main()
