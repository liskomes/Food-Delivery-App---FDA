import unittest
from unittest import mock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from User_Registration import UserRegistration

class TestUserRegistration(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by creating an instance of the UserRegistration class.
        This instance will be used across all test cases.
        """
        self.registration = UserRegistration()

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
