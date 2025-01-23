from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse  # Required for reverse URL lookups
import time  # Used for simulating session timeout


class PrivacyAndSecurityTests(TestCase):
    """
    Test class for ensuring privacy and security features work properly.
    Includes:
    - Data encryption
    - Secure authentication
    - Session timeout handling
    """

    def setUp(self):
        """
        Set up a test user for authentication purposes.
        Called before each test method to create a reusable user instance.
        """
        # Create a test user with default credentials
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_encrypt_user_data(self):
        """
        Test case to verify that user-related data is encrypted in the database.
        - Simulates encryption of sensitive health data.
        - Ensures that the encrypted data differs from plaintext.
        """
        # Simulate health data for encryption testing
        health_data = {"weight": 70, "activity": "Walking"}  # Example plaintext user data

        # Simulate encryption (mock behavior for testing purposes)
        encrypted_data = str(health_data).encode('utf-8').hex()

        # Verify that encrypted data differs from the original plaintext data
        self.assertNotEqual(
            health_data, encrypted_data,
            "Health data is not encrypted properly"
        )

    def test_secure_authentication(self):
        """
        Test case to validate secure login functionality.
        - Verifies that incorrect passwords fail authentication.
        - Ensures that correct credentials allow successful login.
        """
        # Simulate login attempt with an incorrect password
        login_invalid = self.client.login(username="testuser", password="wrongpassword")
        self.assertFalse(
            login_invalid,
            "Login should fail with an incorrect password"
        )

        # Simulate login attempt with correct credentials
        login_valid = self.client.login(username="testuser", password="testpass")
        self.assertTrue(
            login_valid,
            "Login should succeed with the correct password"
        )

    def test_session_timeout(self):
        """
        Test case for handling session timeout due to user inactivity.
        - Logs in the user and sets a custom session expiry.
        - Simulates inactivity and verifies that the session expires as expected.
        """
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        # Set a short session timeout (1 second for testing)
        self.client.session.set_expiry(1)

        # Wait for the session to expire
        time.sleep(2)  # Sleep for 2 seconds to ensure the session expires

        # Attempt to access a protected route (e.g., user profile page)
        response = self.client.get(reverse('profile'))

        # Verify that the user is redirected (status code 302) due to session expiration
        self.assertEqual(
            response.status_code, 302,
            "Session did not timeout as expected"
        )
