from django.contrib import admin

## Django Admin custom changes
#### These can be changed in any app’s admin.py file, but it makes sense to put them in the
#### common app.  
admin.site.index_title = "Home" # index.html / Homepage
admin.site.site_title = "Django Jokes Admin"
admin.site.site_header = "Django Jokes Admin"
