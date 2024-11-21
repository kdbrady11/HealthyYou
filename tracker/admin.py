from django.contrib import admin
from .models import ActivityMetric, MedicationSchedule, MedicationAdherence, Profile

admin.site.register(ActivityMetric)
admin.site.register(MedicationSchedule)
admin.site.register(MedicationAdherence)
admin.site.register(Profile)
