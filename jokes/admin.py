from common.admin import DjangoJokesAdmin
from django.contrib import admin
from .models import Category, Joke, JokeVote, Tag


# Register your models in the db here.
## BEGIN class
@admin.register(Category)
class CategoryAdmin(DjangoJokesAdmin):
    ## Using custom admin settings, set in the common app, instead of:
    # class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['category', 'created', 'updated']


    ## @override
    def get_readonly_fields(self, request, obj=None):
        ## Don't call its super here b/c overriding the entire super method. 
        if(obj): ## If editing an existing object:
            return ('slug', 'created', 'updated')
        return () ## Else rtn an empty tple   
## END class CategoryAdmin()


## BEGIN class
@admin.register(Joke)
class JokeAdmin(DjangoJokesAdmin):
    ## Using custom admin settings, set in the common app, instead of:
    # class JokeAdmin(admin.ModelAdmin):  
    model = Joke
    ## Admin fields
    date_hierarchy = 'updated'
    list_display = ['question', 'created', 'updated', 'category'] ## These can't be many:many fields
    list_filter = ['updated', 'category', 'tags']
    ordering = ['-updated'] ## Default to ordering by updated DESC
    search_fields = ['question', 'answer']


    ## @override
    def get_readonly_fields(self, request, obj=None):
        if(obj): 
            return ('slug', 'created', 'updated')
        return ()    
## END class JokeAdmin()


## BEGIN class
@admin.register(JokeVote)
class JokeVoteAdmin(DjangoJokesAdmin):
    # class JokeVoteAdmin(admin.ModelAdmin):
    model = JokeVote
    list_display = ['joke', 'user', 'vote']

    def get_readonly_fields(self, request, obj=None):
        if (obj): # editing an existing object
            return ('created', 'updated')
        return ()
## END class JokeVote()


## BEGIN class
@admin.register(Tag)
class TagAdmin(DjangoJokesAdmin):
    # class TagAdmin(admin.ModelAdmin):
    model = Joke
    list_display = ['tag', 'created', 'updated']


    ## @override
    def get_readonly_fields(self, request, obj=None):
        if(obj): 
            return ('slug', 'created', 'updated')
        return ()    
## END class JokeAdmin()
