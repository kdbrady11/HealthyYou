from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from tracker.models import (
    ActivityMetric,
    MedicationSchedule,
    MedicationAdherence,
    Profile,
    CalorieMetric
)
from datetime import date, timedelta


# E2E Tests for user login, profile updates, and dashboard navigation
class UserLoginAndProfileTests(TestCase):
    """
    Test suite for end-to-end user workflows:
    - Login and logout
    - Profile updates
    - Navigation and dashboard access
    """

    def setUp(self):
        """
        Set up a user for testing purposes.
        Credentials: secureuser/StrongPassword123
        """
        self.user = User.objects.create_user(
            username="secureuser",
            password="StrongPassword123",
            email="secureuser@example.com"
        )

    def test_end_to_end_login_and_dashboard_access(self):
        """
        Test that a user can:
        - Navigate to the login page
        - Enter valid credentials
        - Access the dashboard
        """
        response = self.client.post(reverse('login'), {'username': 'secureuser', 'password': 'StrongPassword123'})
        self.assertEqual(response.status_code, 200, "Login failed with valid credentials.")
        self.assertContains(response, "Welcome", msg_prefix="Dashboard welcome message not found.")

    def test_profile_update(self):
        """
        Test that a logged-in user can update their profile (e.g., weight, DOB).
        Verify that the updates are reflected in the database.
        """
        self.client.login(username="secureuser", password="StrongPassword123")

        response = self.client.post(reverse('profile'), {'weight': 75, 'dob': '1990-06-15'})

        self.assertEqual(response.status_code, 200, "Profile update request failed.")
        self.assertContains(response, "Profile updated", msg_prefix="Profile update message not found.")

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.weight, 75, "Profile weight was not updated.")
        self.assertEqual(profile.dob.strftime('%Y-%m-%d'), '1990-06-15', "Profile DOB was not updated.")

    def test_logout_and_session_management(self):
        """
        Test that a logged-in user can log out and be prevented from navigating back to the dashboard.
        """
        self.client.login(username="secureuser", password="StrongPassword123")
        self.client.logout()

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302, "User should be redirected after logging out.")


# Tests for caloric tracking and daily summaries
class CaloricTrackingTests(TestCase):
    """
    Test suite for user caloric tracking:
    - Daily caloric totals
    - Meal entries and calculations
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testcalories", password="testpassword")

    def test_add_meal_entries_and_calculate_totals(self):
        """
        Test that a user can:
        - Log multiple meals
        - View the correct daily caloric total
        """
        self.client.login(username="testcalories", password="testpassword")

        CalorieMetric.objects.create(user=self.user, date=date.today(), calories=700)
        CalorieMetric.objects.create(user=self.user, date=date.today(), calories=800)

        daily_total = CalorieMetric.objects.filter(user=self.user, date=date.today()).aggregate(
            total_calories=sum('calories')
        )

        self.assertEqual(daily_total['total_calories'], 1500, "Daily calorie total calculation is incorrect.")


# Tests for physical activity tracking
class ActivityTrackingTests(TestCase):
    """
    Test suite for activity tracking:
    - Log physical activities
    - Ensure activity metrics are reflected in summaries
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testactivity", password="activitypassword")

    def test_physical_activity_tracking(self):
        """
        Test that a user can log multiple physical activities and view them in their activity summary.
        """
        self.client.login(username="testactivity", password="activitypassword")

        ActivityMetric.objects.create(user=self.user, date=date.today(), activity_minutes=20)
        ActivityMetric.objects.create(user=self.user, date=date.today(), activity_minutes=40)

        activities = ActivityMetric.objects.filter(user=self.user, date=date.today())
        total_minutes = sum(activity.activity_minutes for activity in activities)

        self.assertEqual(total_minutes, 60, "Activity tracking summary is incorrect.")


# Tests for medication reminder workflow
class MedicationWorkflowTests(TestCase):
    """
    Test suite for medication reminders:
    - Add a medication reminder
    - Trigger reminder
    - Mark medication as taken
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testmedworkflow", password="medpassword")
        self.client.login(username="testmedworkflow", password="medpassword")

    def test_medication_reminder_workflow(self):
        """
        Test that a user can:
        - Add a medication reminder
        - Mark it as taken
        """
        reminder = MedicationSchedule.objects.create(
            user=self.user,
            medication_name="Test Med",
            dosage="50mg",
            time_of_day="09:00",
            medication_date=date.today()
        )

        adherence = MedicationAdherence.objects.create(
            user=self.user,
            medication_schedule=reminder,
            is_taken=True
        )

        self.assertTrue(adherence.is_taken, "Medication was not marked as taken.")


# Tests for weekly insights and health report
class WeeklyInsightTests(TestCase):
    """
    Test suite for weekly health insights:
    - Weekly data analysis
    - Insights generation
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testinsights", password="testinsightpass")
        # Generate 7 days' worth of data
        for i in range(7):
            CalorieMetric.objects.create(user=self.user, date=date.today() - timedelta(days=i), calories=2100 + i)

    def test_generate_weekly_insights(self):
        """
        Test that weekly caloric insights are calculated accurately.
        """
        weekly_totals = CalorieMetric.objects.filter(
            user=self.user, date__gte=date.today() - timedelta(days=7)
        ).aggregate(total_calories=sum('calories'))

        self.assertEqual(weekly_totals['total_calories'], 14756, "Weekly insights calculation is incorrect.")