from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from tracker.models import CalorieMetric, ActivityMetric


class HealthTrackingTests(TestCase):
    """
    Test class for health tracking features. Includes tests for:
    - Tracking calories
    - Logging activities
    - Tracking weight
    - Generating weekly reports
    - Editing and deleting tracked entries
    """

    def setUp(self):
        """
        Set up a test user and mock database context.
        This method runs before every individual test method to ensure a clean state.
        """
        # Create a test user for authentication purposes
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Simulate user login for authenticated routes
        self.client.login(username="testuser", password="testpass")

    def test_track_daily_calories(self):
        """
        Test case for tracking valid daily calorie entries.
        - Simulates a user entering a meal and its calorie content.
        - Verifies that the entry is tracked successfully.
        """
        response = self.client.post(reverse('calorie_tracking'), {'meal': 'Lunch', 'calories': 500})
        self.assertEqual(response.status_code, 200, "Failed to track daily calorie entry.")
        self.assertIn("Calories tracked successfully", response.content.decode(), "Success message not returned.")

    def test_activity_logging(self):
        """
        Test case for logging valid activity entries.
        - Simulates a user entering an activity and its duration.
        - Verifies that the activity is logged successfully.
        """
        response = self.client.post(reverse('activity_tracking'), {'activity': 'Walking', 'duration': 30})
        self.assertEqual(response.status_code, 200, "Failed to log activity entry.")
        self.assertIn("Activity recorded", response.content.decode(), "Success message not returned.")

    def test_weight_tracking(self):
        """
        Test case for tracking user weight entries.
        - Simulates a user recording their weight.
        - Verifies that the weight entry is logged successfully.
        """
        response = self.client.post(reverse('weight_tracking'), {'weight': 70})
        self.assertEqual(response.status_code, 200, "Failed to track weight entry.")
        self.assertIn("Weight tracked successfully", response.content.decode(), "Success message not returned.")

    def test_generate_weekly_report(self):
        """
        Test case for generating a weekly report.
        - Simulates a user requesting a report with sufficient data.
        - Verifies that the report is generated and returned successfully.
        """
        response = self.client.get(reverse('weekly_report'))
        self.assertEqual(response.status_code, 200, "Failed to generate weekly report.")
        self.assertIn("Weekly report generated", response.content.decode(), "Success message not returned.")

    def test_edit_tracking_entry(self):
        """
        Test case for editing a previously recorded calorie tracking entry.
        - Creates a calorie entry in the test database.
        - Simulates editing the entry with updated calorie information.
        - Verifies that the entry is updated correctly.
        """
        # Create a sample calorie entry in the database
        calorie_entry = CalorieMetric.objects.create(user=self.user, calories=200, date=date.today())

        # Update the entry using a POST request
        response = self.client.post(
            reverse('edit_calorie_entry', args=[calorie_entry.id]),
            {'calories': 300}  # Updated data
        )

        # Verify the response and data update
        self.assertEqual(response.status_code, 200, "Failed to edit calorie tracking entry.")
        calorie_entry.refresh_from_db()  # Reload the instance from the database
        self.assertEqual(
            calorie_entry.calories, 300,
            "Calorie entry was not updated as expected."
        )
        self.assertIn("Entry updated successfully", response.content.decode(), "Success message not returned.")

    def test_delete_tracking_entry(self):
        """
        Test case for deleting an activity tracking entry.
        - Creates an activity entry in the test database.
        - Simulates deleting the entry.
        - Verifies that the entry is removed from the database.
        """
        # Create a sample activity entry in the database
        activity_entry = ActivityMetric.objects.create(user=self.user, activity_minutes=30, date=date.today())

        # Delete the entry using a POST request
        response = self.client.post(reverse('delete_activity_entry', args=[activity_entry.id]))

        # Verify the response and that the entry no longer exists
        self.assertEqual(response.status_code, 200, "Failed to delete activity tracking entry.")
        with self.assertRaises(ActivityMetric.DoesNotExist):
            ActivityMetric.objects.get(id=activity_entry.id)  # Confirm the entry is deleted
        self.assertIn("Entry deleted", response.content.decode(), "Success message not returned.")
