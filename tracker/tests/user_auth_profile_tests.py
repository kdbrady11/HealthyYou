from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UserAuthenticationAndProfileTests(TestCase):
    """
    Test class for user authentication and profile management functionality.
    Includes tests for:
    - Logging in with valid and invalid credentials
    - Password reset
    - Profile updates (e.g., weight, DOB)
    - Age calculation
    - User logout
    """

    def setUp(self):
        """
        Set up a test user for authentication-related tests.
        Called before each test method to ensure a clean slate.
        """
        # Create a test user with default credentials
        self.user = User.objects.create_user(username="testuser", password="testpass", email="testuser@example.com")

    def test_login_valid_credentials(self):
        """
        Test case to verify successful login with valid credentials.
        - Simulates a user entering correct username and password.
        - Verifies the user is logged in successfully (checks response).
        """
        # Simulate login with valid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})

        # Check for successful response
        self.assertEqual(response.status_code, 200, "Login with valid credentials failed.")
        # Verify if the response contains the success message (e.g., welcome message)
        self.assertContains(response, "Welcome", msg_prefix="Login success message not found.")

    def test_login_invalid_credentials(self):
        """
        Test case to verify login functionality with incorrect credentials.
        - Simulates a failed login using invalid username or password.
        - Verifies that appropriate error messages are shown.
        """
        # Simulate login attempt with incorrect credentials
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpass'})

        # Check for successful page load even on failure (stay on login page)
        self.assertEqual(response.status_code, 200, "Unexpected error page on login failure.")
        # Verify if the response contains an error message
        self.assertContains(response, "Invalid username or password", msg_prefix="Login failure message not found.")

    def test_password_reset(self):
        """
        Test case to verify password reset functionality.
        - Simulates the user submitting their email to request a password reset.
        - Verifies that the appropriate success message is shown and email is handled.
        """
        # Simulate submitting a password reset request
        response = self.client.post(reverse('password_reset'), {'email': self.user.email})

        # Check for successful response
        self.assertEqual(response.status_code, 200, "Password reset request failed.")
        # Verify if the response contains the password reset success message
        self.assertContains(response, "Password reset email sent",
                            msg_prefix="Password reset success message not found.")

    def test_profile_update(self):
        """
        Test case to verify updating user profile information.
        - Simulates the user updating profile fields like weight.
        - Verifies that the profile is updated successfully.
        """
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        # Simulate profile update request with new weight
        response = self.client.post(reverse('profile'), {'weight': 70})

        # Check for successful response
        self.assertEqual(response.status_code, 200, "Profile update request failed.")
        # Verify if the response contains the success message
        self.assertContains(response, "Profile updated", msg_prefix="Profile update success message not found.")

    def test_age_calculation(self):
        """
        Test case to verify automatic age calculation upon profile update.
        - Simulates the user submitting their date of birth (DOB).
        - Verifies that the age is calculated and a success message is shown.
        """
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        # Simulate profile update request with user's DOB
        response = self.client.post(reverse('profile'), {'dob': '1990-01-01'})

        # Check for successful response
        self.assertEqual(response.status_code, 200, "Age calculation request failed.")
        # Verify if the response contains the age calculation success message
        self.assertContains(response, "Age calculated", msg_prefix="Age calculation success message not found.")

    def test_logout(self):
        """
        Test case to verify user logout functionality.
        - Logs in the user and initiates a logout request.
        - Verifies that the user is logged out successfully.
        """
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        # Send a logout request
        response = self.client.get(reverse('logout'))

        # Check for successful response
        self.assertEqual(response.status_code, 200, "Logout request failed.")
        # Verify if the response contains the logout message
        self.assertContains(response, "You have been logged out", msg_prefix="Logout success message not found.")
