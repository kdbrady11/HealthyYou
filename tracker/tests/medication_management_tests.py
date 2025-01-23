from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from tracker.models import MedicationSchedule, MedicationAdherence


class MedicationManagementTests(TestCase):
    """
    Test class for managing medication reminders.
    Includes adding, editing, deleting reminders, and checking medication adherence.
    """

    def setUp(self):
        """
        Set up a test user and mock database context.
        Called before each test method to ensure isolation.
        """
        # Create a test user for authentication
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

    def test_add_new_medication_reminder(self):
        """
        Test case for adding a new medication reminder.
        - Simulates a user adding a reminder for a specific medication.
        - Verifies that the reminder is saved successfully.
        """
        # Simulate form submission to add a medication reminder
        response = self.client.post(reverse('add_medication'), {
            'medication_name': 'TestMed',
            'dosage': '500mg',
            'time_of_day': '08:00',
            'medication_date': date.today()
        })

        # Verify the response and success message
        self.assertEqual(response.status_code, 200, "Failed to add medication reminder.")
        self.assertContains(response, "Medication reminder added", msg_prefix="Success message not found.")

        # Verify the medication reminder exists in the database
        medication = MedicationSchedule.objects.filter(medication_name="TestMed", user=self.user).first()
        self.assertIsNotNone(medication, "Medication reminder was not saved to the database.")

    def test_edit_medication_reminder(self):
        """
        Test case for editing an existing medication reminder.
        - Simulates updating the dosage of a medication reminder.
        - Verifies that the change is persisted successfully.
        """
        # Create a sample medication reminder
        medication = MedicationSchedule.objects.create(
            user=self.user, medication_name="TestMed", dosage="500mg", time_of_day="08:00", medication_date=date.today()
        )

        # Simulate updating the dosage
        response = self.client.post(reverse('edit_medication', args=[medication.id]), {'dosage': '600mg'})

        # Verify the response and success message
        self.assertEqual(response.status_code, 200, "Failed to edit medication reminder.")
        self.assertContains(response, "Medication updated", msg_prefix="Success message not found.")

        # Verify the changes are reflected in the database
        medication.refresh_from_db()  # Reload medication from the database
        self.assertEqual(medication.dosage, "600mg", "Medication dosage was not updated as expected.")

    def test_delete_medication_reminder(self):
        """
        Test case for deleting a medication reminder.
        - Simulates a user deleting an existing medication reminder.
        - Verifies that the reminder is removed from the database.
        """
        # Create a sample medication reminder
        medication = MedicationSchedule.objects.create(
            user=self.user, medication_name="TestMed", dosage="500mg", time_of_day="08:00", medication_date=date.today()
        )

        # Simulate deleting the medication reminder
        response = self.client.post(reverse('delete_medication', args=[medication.id]))

        # Verify the response and success message
        self.assertEqual(response.status_code, 200, "Failed to delete medication reminder.")
        self.assertContains(response, "Medication reminder deleted", msg_prefix="Success message not found.")

        # Verify the medication reminder is removed from the database
        with self.assertRaises(MedicationSchedule.DoesNotExist,
                               msg="Medication reminder was not deleted from the database."):
            MedicationSchedule.objects.get(id=medication.id)

    def test_missed_medication_alert(self):
        """
        Test case for handling missed medication alerts.
        - Creates a medication reminder and marks it as missed.
        - Verifies that the `is_taken` status is correctly set to False.
        """
        # Create a sample medication reminder
        medication = MedicationSchedule.objects.create(
            user=self.user, medication_name="TestMed", dosage="500mg", time_of_day="08:00", medication_date=date.today()
        )

        # Create a missed adherence record
        adherence = MedicationAdherence.objects.create(user=self.user, medication_schedule=medication, is_taken=False)

        # Verify the adherence record and missed status
        self.assertFalse(adherence.is_taken, "Missed medication alert was not triggered as expected.")
