from django.conf import settings
from django.db import models
from django.urls import reverse ## Gets and returns the URL based on the passed-in URL pattern name.
from common.utils.text import create_unique_url_slug


## Model Manager(s)
##------------------- 
## Models have "managers". Thru those "managers", you create `QuerySet`(s). 
# The manager is held in the model class’s `objects` attribute.
## To get the "managers":
##-----------------------
# `from <app/dir/project>.models import <classname>
# manager = <classname>.objects`    
#
# Main "Manager" main Methods: 
##------------------------------
## 1. all() – Retrieves all the objects in the model class. It is the equivalent of a SQL SELECT statement 
# with no WHERE clause.
#
## 2. filter(**kwargs) – Retrieves objects in the model class meeting the conditions specified in the kwargs. 
# Generally, it is the equivalent of a SQL SELECT statement with a WHERE clause.
#
## 3. exclude(**kwargs) – Like filter(), except that it retrieves all objects NOT matching the conditions
#  specified in kwargs. It is analogous to a SQL SELECT statement with a WHERE NOT (…) clause.
#
## 4. get(**kwargs) – Retrieves one and only one object -- a single model instance (not a QuerySet). 
#  If no object is found matching the conditions specified in the kwargs, it'll raise a DoesNotExist exception. 
#  If more than one object matches the conditions, it'll raise a MultipleObjectsReturned exception.
# 
## Vocab term: "lookups" - The kwargs passed to filter(), exclude(), and get() are called "lookups". 
# In lookups, dots are not used to connect reference fields of related models (i.e., DON'T DO user.username). 
# Instead, a DOUBLE underscore (__) is used, (i.e., DO user__username)  LAME! Django, LAME!!!!
#-------------------------------------------------------------------
## THREE **Gotchas with related_name and Backward/Reverse Relationships in LOOKUPS:
#---------------------------------------------------------------------------------
# 1. If you have used related_name, then you should use that related_name value in the “reverse” relationship.
# 2. If you have not used related_name, then you should use the lowercase name of the model
#  in the “reverse” relationship
# 3. CAVEAT: When two foreign keys point to the same model, they cannot both have the same related_name.
#
# LOOKUP Examples
## Ex 1: All Jokes by Nat Dunn:
#-------------------------------
# Joke.objects.filter(user__username='ndunn')
## -- OR --
# Joke.objects.filter(user__first_name='Nat', user__last_name='Dunn')
#
## Ex 2: The Category of a Joke by question w/ related name
#------------------------------------------------------------
# `Category.objects.get(jokes__question='What do you call a polar bear in the desert?')``
#
## Ex 3: The User of a Joke by question w/o related name
#--------------------------------------------------------
# `User.objects.get(joke__question='What do you call a polar bear in the desert?')``


## BEGIN class
class Joke(models.Model):
    question = models.TextField(max_length=200)
    answer = models.TextField(max_length=100, blank=True)
    ## Since the Category model class is below this Joke model class, “lazy” reference it by wrapping in 
    #### quotation marks, meaning that Django sees the reference, 
    #### and says “I’ll do that later, after I find the Category model.”
    ## Or, you could reverse the order of these classes in this file.
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='jokes')
    ## Above and below `related_name='jokes'` renames the related manager `joke_set` to `jokes`.
    tags = models.ManyToManyField('Tag', blank=True, related_name='jokes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, unique=True, null=False, editable=False)
    ## user FK w/o a related name, like would use above in Ex 3
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    #
    ### user FK w/ a related name, like would use above in Ex 2
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='jokes')


    ## Class properties (aka calculated fields) allow you to access a class method as if it were an attribute, 
    # and allow you to access info/attrs easily in HTML templates.
    ## You can access these properties in HTML templates as attributes of the Joke instance.
    @property
    def num_votes(self):
        return self.jokevotes.count()


    @property
    def num_likes(self):
        return self.jokevotes.filter(vote=1).count()


    @property
    def num_dislikes(self):
        return self.jokevotes.filter(vote=-1).count()


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
        if (not self.slug):
            value = str(self)
            self.slug = create_unique_url_slug(value, type(self))
        super().save(*args, **kwargs)


    ## @override
    def __str__(self):
        return self.category
    

    #### Meta Subclass
    class Meta():
        verbose_name_plural = 'Categories'
        ordering = ['category'] ## Sets the list of choices to alphabetical order
## END class Category()


## BEGIN class
class Tag(models.Model):
    tag = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50, unique=True, null=False, editable=False
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    ## @override
    def get_absolute_url(self):
        return reverse('jokes:tag', args=[self.slug])
    

    ## @override
    def save(self, *args, **kwargs):
        if (not self.slug):
            value = str(self)
            self.slug = create_unique_url_slug(value, type(self))
        super().save(*args, **kwargs)


    ## @override
    def __str__(self):
        return self.tag
    

    #### subclass
    class Meta():
        ordering = ['tag']
## END class Tag()


## BEGIN class -- Custom Intermediary or JOIN class to create a JOIN tbl w/ more fields/cols than just what 
# you would get w/ a models.ManyToManyField() [i.e.: table1Obj_id, table2Obj_id]  call to create a JOIN tbl
class JokeVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jokevotes')
    joke = models.ForeignKey(Joke, on_delete=models.CASCADE, related_name='jokevotes')
    vote = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    ## subclass
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'joke'], name='one_vote_per_user_per_joke'),
        ]
## END class JokeVote()