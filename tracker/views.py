# Import necessary Django modules and utilities for views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .forms import ActivityMetricForm, MedicationScheduleForm, MedicationAdherenceForm, ProfileForm, CalorieMetricForm
from .models import ActivityMetric, MedicationSchedule, MedicationAdherence, Profile, CalorieMetric
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
from django.db.models import Q, Count


# View: Homepage with user registration functionality
def homepage(request):
    """
    Handles user registration through a UserCreationForm.
    Redirects to the login page upon successful registration.
    """
    if request.method == 'POST':  # POST request indicates form submission
        form = UserCreationForm(request.POST)
        if form.is_valid():  # Validate form data
            form.save()  # Save new user
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created successfully for {username}")
            return redirect('login')  # Redirect to login page
    else:
        form = UserCreationForm()  # Render empty registration form for GET request
    return render(request, 'tracker/homepage.html', {'form': form})


# View: Activity Dashboard
@login_required
def activity_dashboard(request):
    """
    Displays activity statistics and daily calorie tracking for the logged-in user,
    along with forms for adding new activity and calorie metrics.
    """
    # Aggregate user activity metrics by date
    activity_metrics = (ActivityMetric.objects
                        .filter(user=request.user)
                        .values('date')
                        .annotate(total_activity=Sum('activity_minutes'))
                        .order_by('date'))

    # Aggregate user calorie metrics by date
    calorie_metrics = (CalorieMetric.objects
                       .filter(user=request.user)
                       .values('date')
                       .annotate(total_calories=Sum('calories'))
                       .order_by('date'))

    # Prepare data for activity and calorie charts
    activity_dates = [metric['date'].strftime('%Y-%m-%d') for metric in activity_metrics]
    activity_minutes = [metric['total_activity'] for metric in activity_metrics]
    calorie_dates = [metric['date'].strftime('%Y-%m-%d') for metric in calorie_metrics]
    calorie_values = [metric['total_calories'] for metric in calorie_metrics]

    # Initialize forms for new activity and calorie entries
    activity_form = ActivityMetricForm()
    calorie_form = CalorieMetricForm()

    # Handle POST request for form submissions
    if request.method == 'POST':
        if 'activity_submit' in request.POST:  # If submitted activity form
            activity_form = ActivityMetricForm(request.POST)
            if activity_form.is_valid():
                activity_form.instance.user = request.user  # Associate with current user
                activity_form.save()
                return redirect('activity_dashboard')  # Refresh page after saving
        elif 'calorie_submit' in request.POST:  # If submitted calorie form
            calorie_form = CalorieMetricForm(request.POST)
            if calorie_form.is_valid():
                calorie_form.instance.user = request.user  # Associate with current user
                calorie_form.save()
                return redirect('activity_dashboard')  # Refresh page after saving

    # Render dashboard with forms and chart data
    return render(request, 'tracker/activity_dashboard.html', {
        'activity_form': activity_form,
        'calorie_form': calorie_form,
        'activity_metrics': activity_metrics,
        'calorie_metrics': calorie_metrics,
        'activity_dates': activity_dates,
        'activity_minutes': activity_minutes,
        'calorie_dates': calorie_dates,
        'calorie_values': calorie_values,
    })

@login_required
def medication_adherence_dashboard(request):
    """
       Displays a summary of medication adherence for the logged-in user.
       Shows past adherence records and any trends related to taken vs. missed medications.
       """
    # Query adherence records for the current user
    adherence_records = (
        MedicationAdherence.objects.filter(user=request.user)
        .select_related('medication_schedule')
        .order_by('-date')
    )

    # Today's data
    today = now().date()
    adherence_today_data = adherence_records.filter(date=today).aggregate(
        taken=Count('id', filter=Q(is_taken=True)),
        not_taken=Count('id', filter=Q(is_taken=False)),
        not_recorded=Count('id', filter=Q(is_taken__isnull=True)),
    )

    # All-time data
    adherence_all_time_data = adherence_records.aggregate(
        taken=Count('id', filter=Q(is_taken=True)),
        not_taken=Count('id', filter=Q(is_taken=False)),
        not_recorded=Count('id', filter=Q(is_taken__isnull=True)),
    )

    return render(request, 'tracker/medication_adherence_dashboard.html', {
        'adherence_records': adherence_records,
        'adherence_today_data': json.dumps(
            [adherence_today_data['taken'], adherence_today_data['not_taken'], adherence_today_data['not_recorded']]
        ),
        'adherence_all_time_data': json.dumps(
            [adherence_all_time_data['taken'], adherence_all_time_data['not_taken'],
             adherence_all_time_data['not_recorded']]
        ),
    })

# View: Update Medication Status
@login_required
def update_medication_status(request):
    """
    Updates the adherence status ('taken' or 'missed') for medications
    based on user input, ensuring proper tracking of adherence records.
    """
    if request.method == 'POST':  # Process incoming JSON data from AJAX/Fetch
        try:
            data = json.loads(request.body)  # Parse request body
            medication_id = data.get("medication_id")
            status = data.get("status")  # 'taken' or 'missed'

            # Fetch medication schedule for logged-in user
            medication = MedicationSchedule.objects.get(id=medication_id, user=request.user)

            # Check if adherence for today exists, and create or update as needed
            today = now().date()
            adherence, created = MedicationAdherence.objects.get_or_create(
                user=request.user,
                medication_schedule=medication,
                date=today,
                defaults={'is_taken': (status == 'taken')}
            )

            if not created:  # If adherence record already exists, return error
                return JsonResponse({'success': False, 'error': 'Status already recorded for today'})

            adherence.is_taken = (status == 'taken')  # Update adherence status
            adherence.save()

            return JsonResponse({'success': True, 'status': status})  # Success response

        except MedicationSchedule.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Medication not found'})  # Medication not found
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})  # Handle unexpected errors

    return JsonResponse({'success': False, 'error': 'Invalid request'})  # Invalid HTTP method

@login_required
def medication_schedule_view(request, id=None):
    """
       Handles viewing and editing medication schedules. If `id` is provided, it edits an existing
       medication schedule, otherwise, it creates a new one.
       """
    if id:
        # If we have an ID, fetch the specific medication schedule for editing
        medication_schedule = get_object_or_404(MedicationSchedule, id=id, user=request.user)
        form = MedicationScheduleForm(request.POST or None, instance=medication_schedule)
    else:
        # Create a new medication schedule if ID does not exist
        form = MedicationScheduleForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Save form data, associate it with the current user, and redirect
        medication_schedule = form.save(commit=False)
        medication_schedule.user = request.user
        medication_schedule.save()
        return redirect('medication_dashboard')

    return render(request, 'tracker/medication_schedule.html', {
        'form': form,
        'editing': bool(id),  # Flag to determine if we're creating or editing
    })

# View: Medication Dashboard
@login_required
def medication_dashboard(request):
    """
    Displays the list of medications that are scheduled for today for the logged-in user.
    """
    from datetime import date
    import logging

    logger = logging.getLogger(__name__)  # Set up application logging
    logger.debug("Today's date: %s", date.today())  # Debug logging for current date

    # Check for medications scheduled for today's date
    if hasattr(MedicationSchedule, 'medication_date'):
        medications_today = MedicationSchedule.objects.filter(user=request.user, medication_date=date.today())
    else:
        medications_today = MedicationSchedule.objects.filter(user=request.user, date=date.today())

    logger.debug("Medications Today Queryset: %s", medications_today)  # Log queryset for debugging purposes

    # Render medication dashboard
    return render(request, 'tracker/medication_dashboard.html', {
        'medications_today': medications_today,
    })


# View: Profile
@login_required
def profile(request):
    """
    Displays the user's profile information and allows the user to update their details.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)  # Fetch or create profile for user

    if request.method == 'POST':  # If updating profile via POST request
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()  # Save profile updates
            return redirect('profile')  # Redirect to profile page after saving
    else:
        form = ProfileForm(instance=profile)  # Display profile form with current data

    # Render profile page with the form
    return render(request, 'tracker/profile.html', {'form': form, 'profile': profile})


# View: Logout
from django.contrib.auth import logout


def logout_view(request):
    """
    Logs out the currently logged-in user and redirects them to the logout confirmation page.
    """
    logout(request)  # Log out the user
    return render(request, 'tracker/logout.html')  # Render logout confirmation page
