from django import forms  # Import Django's forms module to create form classes
from .models import ActivityMetric, MedicationSchedule, MedicationAdherence, Profile, \
    CalorieMetric  # Import models for form mapping


# Form for recording activity metrics (e.g., date and activity minutes)
class ActivityMetricForm(forms.ModelForm):
    class Meta:
        model = ActivityMetric  # Map this form to the ActivityMetric model
        fields = ['date', 'activity_minutes']  # Fields to include in the form

    # Adding a custom widget (date picker) for the date field
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


# Form to create or edit a medication schedule
class MedicationScheduleForm(forms.ModelForm):
    class Meta:
        model = MedicationSchedule  # Map this form to the MedicationSchedule model
        fields = ['medication_name', 'dosage', 'time_of_day', 'notes',
                  'medication_date']  # Fields to include in the form
        widgets = {
            # Adding a time picker widget for the time_of_day field
            'time_of_day': forms.TimeInput(attrs={'type': 'time'}),
        }


# Form for tracking medication adherence
class MedicationAdherenceForm(forms.ModelForm):
    class Meta:
        model = MedicationAdherence  # Map this form to the MedicationAdherence model
        fields = ['medication_schedule', 'is_taken', 'date']  # Fields to include for tracking adherence

    # Constructor to customize the form instance
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user instance from the keyword arguments
        super(MedicationAdherenceForm, self).__init__(*args, **kwargs)

        # Filter `medication_schedule` options to show only schedules belonging to the user
        if self.user:
            self.fields['medication_schedule'].queryset = MedicationSchedule.objects.filter(user=self.user)


# Form for editing user profile information
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # Map this form to the Profile model
        fields = ['dob', 'weight']  # Include only the date of birth and weight fields
        widgets = {
            # Adding a date picker widget for the date of birth field
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }


# Form for recording calorie metrics (e.g., date and calorie count)
class CalorieMetricForm(forms.ModelForm):
    class Meta:
        model = CalorieMetric  # Map this form to the CalorieMetric model
        fields = ['date', 'calories']  # Fields to include in the form

    # Adding a custom widget (date picker) for the date field
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
