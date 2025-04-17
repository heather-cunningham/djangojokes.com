from datetime import datetime
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Applicant


## Helper fcn
def validate_checked(value):
    if (not value):
        raise ValidationError("Required.")
    return


## BEGIN class
class JobApplicationForm(forms.ModelForm):
    DAYS = (
        (1, 'MON'),
        (2, 'TUE'),
        (3, 'WED'),
        (4, 'THU'),
        (5, 'FRI')
    )
    available_days = forms.TypedMultipleChoiceField(
        choices=DAYS,
        coerce=int,
        help_text = "Check all the days you're available to work.",
        widget = forms.CheckboxSelectMultiple(
            attrs = {'checked':True}
        )
    )
    confirmation = forms.BooleanField(
        label = 'I certify the information I have provided is true and correct.',
        validators=[validate_checked]
    )

    #### subclass
    class Meta():
        model = Applicant
        START_YEARS = range(datetime.now().year, (datetime.now().year + 2))
        fields = (
            'first_name', 'last_name', 'email', 'website', 'employment_type',
            'start_date', 'available_days', 'desired_hourly_wage',
            'cover_letter', 'confirmation', 'job')
        widgets = {
            'first_name': forms.TextInput(attrs={'autofocus': True}),
            'website': forms.TextInput(attrs={
                'placeholder':'https://www.example.com',
                'required': False
            }),
            'start_date': forms.SelectDateWidget(
                attrs = {'style': 'width: 21%; display: inline-block; margin: 0 1%;'},
                years=START_YEARS,
            ),
            'desired_hourly_wage': forms.NumberInput(
                attrs = {'min':'10.00', 'max':'100.00', 'step':'.25', 'placeholder':'10:00'}
            ),
            'cover_letter': forms.Textarea(attrs={'cols': '100', 'rows': '5'})
        }
        error_messages = {
            'start_date': {'past_date': 'Please enter a date in the future.'},
        }
## END class JobApplicationForm()
