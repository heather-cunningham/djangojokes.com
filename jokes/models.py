from django.db import models
from django.urls import reverse ## Gets and returns the URL based on the passed-in URL pattern name.
from common.utils.text import create_unique_url_slug

# Create your models here.
## BEGIN class
class Joke(models.Model):
    question = models.TextField(max_length=200)
    answer = models.TextField(max_length=100, blank=True)
    ## Since the Category model class is below this Joke model class, “lazy” reference it by wrapping in 
    #### quotation marks, meaning that Django sees the reference, 
    #### and says “I’ll do that later, after I find the Category model.”
    ## Or, you could reverse the order of these classes in this file.
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, unique=True, null=False, editable=False)


    ## @override -- Python doesn't have this decorator
    def get_absolute_url(self):
        # return reverse("jokes:detail", args=[str(self.pk)])
        ## Now use the newly created URL slug, instead of the Joke's primary key 
        return reverse("jokes:detail", args=[str(self.slug)])


    ## @override 
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
## END class Joke()


## BEGIN class
class Category(models.Model):
    category = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50, unique=True, null=False, editable=False
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    ## @override
    def get_absolute_url(self):
        return reverse('jokes:category', args=[self.slug])
    

    ## @override
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = create_unique_url_slug(value, type(self))
        super().save(*args, **kwargs)


    ## @override
    def __str__(self):
        return self.category
    

    #### Meta Subclass
    class Meta:
        verbose_name_plural = 'Categories'
## END class Category()