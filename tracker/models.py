from django.db import models  # Import Django ORM models
from django.contrib.auth.models import User  # Import the built-in User model for linking to user-specific data
from datetime import date  # Import date class to handle date-related calculations
from django.utils import timezone  # Import timezone utilities for managing time-aware data


# Model to track user activity metrics (e.g., date and number of activity minutes)
class ActivityMetric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each activity to a specific user
    date = models.DateField()  # Date of the recorded activity
    activity_minutes = models.IntegerField()  # Duration of activity in minutes

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.activity_minutes} mins"


# Model for scheduling medications and supplements (e.g., name, dosage, and scheduled time)
class MedicationSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each medication schedule to a user
    medication_name = models.CharField(max_length=200)  # Name of the medication or supplement
    dosage = models.CharField(max_length=100)  # Dosage prescribed (e.g., "500mg")
    time_of_day = models.TimeField()  # Scheduled time for taking the medication
    notes = models.TextField(blank=True)  # Optional notes or instructions
    medication_date = models.DateField()  # Specific date for taking the medication

    def __str__(self):
        return self.medication_name  # Return medication name for readability in admin


# Model to track medication adherence (i.e., record if a medication was taken on schedule)
class MedicationAdherence(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Link adherence to a specific user
    medication_schedule = models.ForeignKey('MedicationSchedule',
                                            on_delete=models.CASCADE)  # Link to the related schedule
    is_taken = models.BooleanField(default=False)  # Boolean flag to track if the medication was taken
    date = models.DateField()  # Date of the adherence record

    def __str__(self):
        return f"{self.medication_schedule.medication_name} - {self.is_taken} - {self.date}"


# Model for managing user profiles (e.g., age, weight, weight history)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship per user
    dob = models.DateField(null=True, blank=True)  # Date of birth (optional)
    age = models.PositiveIntegerField(null=True, blank=True)  # Automatically calculated age
    weight = models.FloatField(null=True, blank=True)  # Current weight in pounds
    weight_history = models.JSONField(default=list, blank=True)  # History of weight as a list of {date, weight}

    # Custom save method to maintain weight tracking and automatically calculate age
    def save(self, *args, **kwargs):
        # Automatically add or update today's weight in the weight history
        if self.weight:
            today = date.today().strftime('%Y-%m-%d')  # Format today's date as YYYY-MM-DD
            weight_entry = next(  # Check if a weight entry already exists for today
                (entry for entry in self.weight_history if entry['date'] == today), None
            )
            if weight_entry:
                # Update the weight entry for today
                weight_entry['weight'] = self.weight
            else:
                # Append a new weight entry if none exists for today
                self.weight_history.append({'date': today, 'weight': self.weight})

        # Calculate the user's age based on their date of birth
        if self.dob:
            today = date.today()
            self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

        super(Profile, self).save(*args, **kwargs)  # Call the superclass save method

    def __str__(self):
        return self.user.username  # Display the username in admin or other representations


# Model to track calorie metrics (e.g., daily calorie intake)
class CalorieMetric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link calorie metric to a specific user
    date = models.DateField()  # Date of the calorie record
    calories = models.IntegerField()  # Total calorie intake for the day in calories

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.calories} calories"
