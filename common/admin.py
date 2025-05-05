from django.contrib import admin

## Django Admin custom changes
#### These can be changed in any app’s admin.py file, but it makes sense to put them in the
#### common app.  
admin.site.index_title = "Home" # index.html / Homepage
admin.site.site_title = "Django Jokes Admin"
admin.site.site_header = "Django Jokes Admin"


## Set all of the other ModelAdmin classes, in the other apps' admin's, 
# to inherit from this class.
#### Remember, in Django, almost everything is an app.    
class DjangoJokesAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_max_show_all = 600
    ## Replaces the `Save and Add Another` btn [in Admin] 
    # with a `Save as New` btn.
    save_as = True
