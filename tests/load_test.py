import time
import sys
import os
import tkinter as tk
from unittest.mock import patch

# Add the directory containing main.py to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import Application

def simulate_user_actions(user_id):
    app = Application()
    app.show_register_frame()

    # Simulate user registration
    register_frame = app.current_frame
    email = f"user{user_id}@example.com"
    password = "Password123"  # Ensure the password meets the strength requirements
    register_frame.email_entry.insert(0, email)
    register_frame.pass_entry.insert(0, password)
    register_frame.conf_pass_entry.insert(0, password)
    register_frame.register_user()

    # Simulate user login
    app.show_login_frame()
    login_frame = app.current_frame
    login_frame.email_entry.insert(0, email)
    login_frame.pass_entry.insert(0, password)
    login_frame.login()

    # Check if login was successful
    if app.logged_in_email != email:
        print(f"User {user_id} login failed.")
        app.destroy()
        return

    print(f"User {user_id} actions completed.")
    app.destroy()

def load_test(num_users):
    for i in range(num_users):
        simulate_user_actions(i)

if __name__ == "__main__":
    num_users = 100  # Number of users to simulate
    start_time = time.time()
    with patch('tkinter.messagebox.showinfo', return_value=None), patch('tkinter.messagebox.showerror', return_value=None):
        load_test(num_users)

    end_time = time.time()
    print(f"Load test completed in {end_time - start_time} seconds.")