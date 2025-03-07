import unittest
from unittest import mock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from User_Registration import UserRegistration

import re

"""Faking the UserRegistration"""
class FakeUserRegistration():
    def __init__(self):

        self.users = {'jenni@kissa.fi': {'password': 'kissa12!', 'confirmed': False}, 'jenni@kissafi.fi': {'password': 'kissa12!!', 'confirmed': False}, 'jenni@kissakissa.fi': {'password': 'kissa12!!', 'confirmed': False}, 'jee@jee.fi': {'password': 'kissa12!!', 'confirmed': False}}

    def register(self, email, password, confirm_password):
    
        if not self.is_valid_email(email):
            return {"success": False, "error": "Invalid email format"}  # If email format is invalid, return an error.
        if password != confirm_password:
            return {"success": False, "error": "Passwords do not match"}  # If passwords don't match, return an error.
        if not self.is_strong_password(password):
            return {"success": False, "error": "Password is not strong enough"}  # If password isn't strong, return an error.
        if email in self.users:
            return {"success": False, "error": "Email already registered"}  # If the email is already registered, return an error.

        # Register the user if all conditions are met and return a success message.
        self.users[email] = {"password": password, "confirmed": False}
        return {"success": True, "message": "Registration successful, confirmation email sent"}

    def is_valid_email(self, email): #Add regex pattern (import re)

        return re.match(r'^\w{1,}@(\w{1,}+\.)+[a-zA-Z]{1,}$', email)

    def is_strong_password(self, password):

        return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)



class TestUserRegistration(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by creating an instance of the UserRegistration class.
        This instance will be used across all test cases.
        """
        """self.registration = UserRegistration()"""
        self.registration = FakeUserRegistration()

    def test_successful_registration(self):
        """
        Test case for successful user registration.
        It verifies that a valid email and matching strong password results in successful registration.
        """
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertTrue(result['success'])  # Ensures that registration is successful.
        self.assertEqual(result['message'], "Registration successful, confirmation email sent")  # Checks the success message.

    def test_invalid_email(self):
        """
        Test case for invalid email format.
        It verifies that attempting to register with an incorrectly formatted email results in an error.
        """
        result = self.registration.register("userexample.com", "Password123", "Password123")
        self.assertFalse(result['success'])  # Ensures registration fails due to invalid email.
        self.assertEqual(result['error'], "Invalid email format")  # Checks the specific error message.

        result = self.registration.register("1@1.1", "Password123", "Password123")
        self.assertFalse(result['success'])  # Ensures registration fails due to invalid email.
        self.assertEqual(result['error'], "Invalid email format")  # Checks the specific error message.

    def test_is_email_valid(self):
        """
        Test case for valid email format.
        It verifies that attempting to register with an correctly formatted email results.
        """
        result = self.registration.register("1@1.com", "Password123", "Password123")
        self.assertTrue(result['success'], True)  # Ensures registration passes due to correct email

        result = self.registration.register("1dd@a.d", "Password123", "Password123")
        self.assertTrue(result['success'], True)  # Ensures registration passes due to correct email

    def test_password_mismatch(self):
        """
        Test case for password mismatch.
        It verifies that when the password and confirmation password do not match, registration fails.
        """
        result = self.registration.register("user@example.com", "Password123", "Password321")
        self.assertFalse(result['success'])  # Ensures registration fails due to password mismatch.
        self.assertEqual(result['error'], "Passwords do not match")  # Checks the specific error message.

    def test_weak_password(self):
        """
        Test case for weak password.
        It verifies that a password not meeting the strength requirements results in an error.
        """
        result = self.registration.register("user@example.com", "pass", "pass")
        self.assertFalse(result['success'])  # Ensures registration fails due to a weak password.
        self.assertEqual(result['error'], "Password is not strong enough")  # Checks the specific error message.

    def test_email_already_registered(self):
        """
        Test case for duplicate email registration.
        It verifies that attempting to register an email that has already been registered results in an error.
        """
        self.registration.register("user@example.com", "Password123", "Password123")  # Register a user.
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertFalse(result['success'])  # Ensures registration fails due to the email already being registered.
        self.assertEqual(result['error'], "Email already registered")  # Checks the specific error message.

if __name__ == '__main__':
    unittest.main()
