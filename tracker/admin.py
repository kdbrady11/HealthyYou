from django.contrib import admin  # Import Django's built-in admin module for model registration
from .models import ActivityMetric, MedicationSchedule, MedicationAdherence, Profile  # Import project models

# Registering models with the Django admin site
# This makes these models manageable through the Django admin interface
admin.site.register(ActivityMetric)  # Register ActivityMetric model to track user activity metrics
admin.site.register(MedicationSchedule)  # Register MedicationSchedule model to manage medication schedules
admin.site.register(MedicationAdherence)  # Register MedicationAdherence model to track medication adherence
admin.site.register(Profile)  # Register Profile model to manage user profile information
