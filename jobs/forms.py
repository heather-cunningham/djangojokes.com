from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_future_date(date_value):
    if (date_value < datetime.now().date()):
        raise ValidationError(message=f'{date_value} is in the past.', code='past_date')


class JobApplicationForm(forms.Form):
    ## These work, too:
    #  EMPLOYMENT_TYPES = [
    #     (None, '--Please choose--'),
    #     ('ft', 'Full-time'),
    #     ('pt', 'Part-time'),
    #     ('contract', 'Contract work')
    # ]
    # DAYS = [
    #     (1, 'MON'),
    #     (2, 'TUE'),
    #     (3, 'WED'),
    #     (4, 'THU'),
    #     (5, 'FRI')
    # ]
    ##
    # EMPLOYMENT_TYPES = {
    #     'none': '--Please choose--',
    #     'ft': 'Full-time',
    #     'pt': 'Part-time',
    #     'contract': 'Contract work'
    # }
    # DAYS = {
    #     1: 'MON',
    #     2: 'TUE',
    #     3: 'WED',
    #     4: 'THU',
    #     5: 'FRI'
    # }
    EMPLOYMENT_TYPES = (
        (None, '--Please choose--'),
        ('ft', 'Full-time'),
        ('pt', 'Part-time'),
        ('contract', 'Contract work')
    )
    DAYS = (
        (1, 'MON'),
        (2, 'TUE'),
        (3, 'WED'),
        (4, 'THU'),
        (5, 'FRI')
    )
    START_YEARS = range(datetime.now().year, (datetime.now().year + 2))
    #
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,}))
    last_name = forms.CharField()
    email = forms.EmailField()
    website = forms.CharField(required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'https://www.example.com','size': '50'}
        ),
        validators=[URLValidator(schemes=['http', 'https'])]
    )
    employment_type = forms.ChoiceField(choices=EMPLOYMENT_TYPES)
    ## Django help_text is UGLY!!! U. G. L. Y., Django got no alibi
    start_date = forms.DateField(help_text="The earliest date you're available to start work.",
        widget=forms.SelectDateWidget(
            years=START_YEARS,
            attrs={'style': 'width: 31%; display: inline-block; margin: 0 1%;'}
        ),
        validators=[validate_future_date,],
        error_messages={'past_date': 'Please, enter a date in the future.'})
    ## `choices=` takes in any Iterable w/ 2 values, like a Tuple of Tuples, a Dict, a List of Tuples or 
    ## a List of Dicts, ea. el in the Iterable must have two els
    available_days = forms.TypedMultipleChoiceField(choices=DAYS,
        coerce=int(),  ## coerce takes a fcn                                          
        help_text="Select all the days you're available to work.",
        widget=forms.CheckboxSelectMultiple(attrs={'checked': True}))
    desired_hourly_wage = forms.DecimalField(widget=forms.NumberInput(
        attrs={
            'min': '10.00',
            'max': '100.00',
            'step': '.25',
            'placeholder': '10.00'
        }
    ))
    cover_letter = forms.CharField(widget=forms.Textarea(
        attrs={
            'cols': '70', 
            'rows': '5'
        }
    ))
    ## Note!!!  CheckboxInput is a widget, not a form field. 
    ## So, you can't use `forms.CheckboxInput` here for a checkbox...
    ## *Yeah, that makes toooootaaaallll sense, Django*, WTF
    confirmation = forms.BooleanField(
        label="I certify the information I have provided is true and correct."
    )