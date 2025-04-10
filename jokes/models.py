from django.db import models
from django.urls import reverse
## The reverse() function, imported above, gets and returns 
# the URL based on the passed-in URL pattern name.

# Create your models here.
## BEGIN class
class Joke(models.Model):
    question = models.TextField(max_length=200)
    answer = models.TextField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        return reverse("jokes:detail", args=[str(self.pk)])

    
    def __str__(self):
        """" To string """
        return self.question
## END class
