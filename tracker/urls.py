from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('activity/', views.activity_dashboard, name='activity_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('medication/', views.medication_dashboard, name='medication_dashboard'),
    path('medication-schedule/', views.medication_schedule_view, name='medication_schedule'),
    path('medication-schedule/<int:id>/', views.medication_schedule_view, name='medication_schedule_edit'),
    path('medication-adherence/', views.medication_adherence_dashboard, name='medication_adherence_dashboard'),  # Distinct path for adherence dashboard
    path('medication/edit/<int:id>/', views.medication_schedule_view, name='edit_medication'),
]

