from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum
from .forms import ActivityMetricForm, MedicationScheduleForm, MedicationAdherenceForm, ProfileForm, CalorieMetricForm
from .models import ActivityMetric, MedicationSchedule, MedicationAdherence, Profile, CalorieMetric

# Activity Dashboard View (unchanged)
@login_required
def activity_dashboard(request):
    # Fetch data from the database and aggregate by date
    activity_metrics = (ActivityMetric.objects
                        .filter(user=request.user)  # Ensure you're filtering by the user
                        .values('date')
                        .annotate(total_activity=Sum('activity_minutes'))
                        .order_by('date'))

    calorie_metrics = (CalorieMetric.objects
                       .filter(user=request.user)  # Ensure you're filtering by the user
                       .values('date')
                       .annotate(total_calories=Sum('calories'))
                       .order_by('date'))

    # Prepare data for the charts
    activity_dates = [metric['date'].strftime('%Y-%m-%d') for metric in activity_metrics]
    activity_minutes = [metric['total_activity'] for metric in activity_metrics]
    calorie_dates = [metric['date'].strftime('%Y-%m-%d') for metric in calorie_metrics]
    calorie_values = [metric['total_calories'] for metric in calorie_metrics]

    # Initialize the forms for both activity and calorie data
    activity_form = ActivityMetricForm()
    calorie_form = CalorieMetricForm()

    # Handle form submission
    if request.method == 'POST':
        if 'activity_submit' in request.POST:  # Activity form submission
            activity_form = ActivityMetricForm(request.POST)
            if activity_form.is_valid():
                activity_form.instance.user = request.user  # Associate the activity with the logged-in user
                activity_form.save()
                return redirect('activity_dashboard')  # Redirect to refresh the page after saving
        elif 'calorie_submit' in request.POST:  # Calorie form submission
            calorie_form = CalorieMetricForm(request.POST)
            if calorie_form.is_valid():
                calorie_form.instance.user = request.user  # Associate the calorie data with the logged-in user
                calorie_form.save()
                return redirect('activity_dashboard')  # Redirect to refresh the page after saving

    # Render the page with both forms and chart data
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

# Medication Dashboard View
@login_required
def medication_dashboard(request):
    # Fetch medications from the MedicationSchedule model
    medications = MedicationSchedule.objects.filter(user=request.user)

    return render(request, 'tracker/medication_dashboard.html', {
        'medications': medications,
    })

# Medication Schedule View for creating or editing medications
@login_required
def medication_schedule_view(request, id=None):
    if id:
        # Fetch existing medication schedule for editing
        medication = MedicationSchedule.objects.get(id=id, user=request.user)
    else:
        # Create a new medication entry (ensure user is assigned)
        medication = MedicationSchedule(user=request.user)

    if request.method == 'POST':
        form = MedicationScheduleForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()  # This will now save the medication with the associated user
            return redirect('medication_dashboard')  # Redirect back to the dashboard after saving
    else:
        form = MedicationScheduleForm(instance=medication)

    return render(request, 'tracker/medication_schedule.html', {
        'form': form,
        'medication': medication
    })

# Medication Adherence Dashboard View
@login_required
def medication_adherence_dashboard(request):
    medications = MedicationSchedule.objects.filter(user=request.user)
    adherence_records = MedicationAdherence.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        form = MedicationAdherenceForm(request.POST, user=request.user)  # Pass the user here
        if form.is_valid():
            form.save()
            return redirect('medication_adherence_dashboard')
    else:
        form = MedicationAdherenceForm(user=request.user)  # Initialize the form with the user

    return render(request, 'tracker/medication_adherence_dashboard.html', {
        'medications': medications,
        'form': form,
        'adherence_records': adherence_records,
    })

# Profile View (unchanged)
@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'tracker/profile.html', {'form': form, 'profile': profile})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirects to the login page
