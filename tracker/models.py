from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

class ActivityMetric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    activity_minutes = models.IntegerField()


# Medication and Supplement Schedule (name, dosage, and scheduled time)
class MedicationSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    time_of_day = models.CharField(max_length=50)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.medication_name

# Medication Adherence (tracks whether the medication was taken each day)
class MedicationAdherence(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    medication_schedule = models.ForeignKey('MedicationSchedule', on_delete=models.CASCADE)
    is_taken = models.BooleanField(default=False)  # This field should be present in the model
    date = models.DateField()

    def __str__(self):
        return f"{self.medication_schedule.medication_name} - {self.is_taken} - {self.date}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    weight_history = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        # Track weight history
        if self.weight:
            today = date.today().strftime('%Y-%m-%d')  # Format the date as string
            self.weight_history.append({'date': today, 'weight': self.weight})

        # Calculate age
        if self.dob:
            today = date.today()
            self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class CalorieMetric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    calories = models.IntegerField()