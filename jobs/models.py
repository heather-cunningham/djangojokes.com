from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


## helper fcns
def validate_future_date(date_value):
    if (date_value < datetime.now().date()):
        raise ValidationError(message=f'{date_value} is in the past.', code='past_date')



## BEGIN class
class Job(models.Model):
    title = models.CharField(max_length=200) ##CharField with max_length set to 200.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    ## @override
    def __str__(self):
        """" To string """
        return self.title
## END model class Job()


## BEGIN class
class Applicant(models.Model):
    EMPLOYMENT_TYPES = (
        (None, '--Please choose--'),
        ('ft', 'Full-time'),
        ('pt', 'Part-time'),
        ('contract', 'Contract work')
    )
    #
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(help_text='A valid email address.')
    website = models.URLField(blank=True, 
                              validators=[URLValidator(schemes=['http', 'https'])])
    employment_type = models.CharField(max_length=10, choices=EMPLOYMENT_TYPES)
    start_date = models.DateField(help_text="The earliest date you're available to start work.",
                                    validators=[validate_future_date])
    available_days = models.CharField(max_length=20)
    desired_hourly_wage = models.DecimalField(max_digits=5, decimal_places=2)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to="private/resumes", blank=True, 
                              help_text="PDFs only, please.")
    confirmation = models.BooleanField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    ## override
    def __str__(self):
        return f'{self.first_name} {self.last_name}, Applying to - ({self.job})'
## END model class Applicant()


