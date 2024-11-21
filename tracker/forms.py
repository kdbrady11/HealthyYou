from django import forms
from .models import ActivityMetric, MedicationSchedule, MedicationAdherence, Profile, CalorieMetric


class ActivityMetricForm(forms.ModelForm):
    class Meta:
        model = ActivityMetric
        fields = ['date', 'activity_minutes']

    # Adding a date picker for the date field
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


# Form to create a new medication schedule (medication name, dosage, etc.)
class MedicationScheduleForm(forms.ModelForm):
    class Meta:
        model = MedicationSchedule
        fields = ['medication_name', 'dosage', 'time_of_day', 'notes']
        widgets = {
            'time_of_day': forms.TimeInput(attrs={'type': 'time'}),  # Adding a time picker for time of day
        }


# Form for tracking medication adherence
class MedicationAdherenceForm(forms.ModelForm):
    class Meta:
        model = MedicationAdherence
        fields = ['medication_schedule', 'is_taken', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Make sure the user sees a dropdown of their medications in the adherence form
    medication_schedule = forms.ModelChoiceField(queryset=MedicationSchedule.objects.none(), empty_label="Select Medication")

    def __init__(self, *args, **kwargs):
        user = kwargs.get('user', None)
        super(MedicationAdherenceForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['medication_schedule'].queryset = MedicationSchedule.objects.filter(user=user)

    # Automatically set the current date if not provided
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            date = forms.fields.DateField().clean(forms.utils.datetime_safe.today())
        return date


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'weight']  # Only include these fields in the form
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }


class CalorieMetricForm(forms.ModelForm):
    class Meta:
        model = CalorieMetric
        fields = ['date', 'calories']

    # Adding a date picker for the date field
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
