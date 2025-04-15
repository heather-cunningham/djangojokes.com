from django.db import models
from django.urls import reverse ## Gets and returns the URL based on the passed-in URL pattern name.
from common.utils.text import create_unique_url_slug

# Create your models here.
## BEGIN class
class Joke(models.Model):
    question = models.TextField(max_length=200)
    answer = models.TextField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, unique=True, null=False, editable=False)


    def get_absolute_url(self):
        # return reverse("jokes:detail", args=[str(self.pk)])
        ## Now use the newly created URL slug, instead of the Joke's primary key 
        return reverse("jokes:detail", args=[str(self.slug)])


    ## @override -- Python doesn't have this decorator
    def save(self, *args, **kwargs):
        if (not self.slug): ## Only create the slug if the record doesn’t already have one
            value = str(self)
            self.slug = create_unique_url_slug(value, type(self))
        super().save(*args, **kwargs)


    ## @override -- Overrides calling/casting of the str(<value>)
    #### Rtns `self.question` when str(<any Joke Obj>) is called
    def __str__(self):
        """" To string """
        return self.question
## END class
