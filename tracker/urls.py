from django.urls import path  # Import path for defining URL routes
from . import views  # Import views.py from the current directory
from django.contrib.auth import views as auth_views  # Import authentication views

# Define the URL patterns for the application
urlpatterns = [
    # Route for the activity dashboard page
    path('activity/', views.activity_dashboard, name='activity_dashboard'),

    # Route for the user profile page
    path('profile/', views.profile, name='profile'),

    # Route for displaying the medication dashboard
    path('medication/', views.medication_dashboard, name='medication_dashboard'),

    # Route for viewing the medication schedule
    path('medication-schedule/', views.medication_schedule_view, name='medication_schedule'),

    # Route for editing a specific medication schedule (requires the schedule's ID)
    path('medication-schedule/<int:id>/', views.medication_schedule_view, name='medication_schedule_edit'),

    # Route for displaying the medication adherence dashboard for tracking doses
    path('medication-adherence/', views.medication_adherence_dashboard, name='medication_adherence_dashboard'),

    # Route for editing medication entries (accepts the ID of the medication to be edited)
    path('medication/edit/<int:id>/', views.medication_schedule_view, name='edit_medication'),

    # Alternative route for accessing the medication adherence dashboard
    path('medication-adherence-dashboard/', views.medication_adherence_dashboard,
         name='medication_adherence_dashboard'),

    # Route for updating the status of medications (e.g., marking doses as taken or missed)
    path('update-medication-status/', views.update_medication_status, name='update_medication_status'),
]
