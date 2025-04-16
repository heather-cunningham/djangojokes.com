from django import forms


class JobApplicationForm(forms.Form):
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
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    website = forms.URLField(required=False)
    employment_type = forms.ChoiceField(choices=EMPLOYMENT_TYPES) ## `choices=` takes in a Tuple of Tuples
    start_date = forms.DateField(
        help_text="The earliest date you're available to start."
    )
    ## `choices=` takes in a Tuple of Tuples, same here
    available_days = forms.MultipleChoiceField(
        choices=DAYS,
        help_text="Select all the days you're available to work."
    )
    desired_hourly_wage = forms.DecimalField()
    cover_letter = forms.CharField()
    ## Note!!!  CheckboxInput is a widget, not a form field. 
    ## So, you can't use `forms.CheckboxInput` here for a checkbox...
    ## *Yeah, that makes toooootaaaallll sense, Django*, WTF
    confirmation = forms.BooleanField(
        label="I certify the information I have provided is true and correct."
    )