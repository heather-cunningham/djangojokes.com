from django.contrib import admin
from .models import Joke


# Register your models here.
@admin.register(Joke)
class JokeAdmin(admin.ModelAdmin):
    model = Joke
    list_display = ['question', 'created', 'updated']


    def get_readonly_fields(self, request, obj=None):
        ## Don't call its super here b/c overriding the entire super method. 
        if(obj): ## If editing an existing object:
            return ('created', 'updated')
        return () ## Else rtn an empty tple
    
    
## END model class
