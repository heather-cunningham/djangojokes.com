from django.contrib import admin
from .models import Applicant, Job


## BEGIN class
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display = ['title', 'created', 'updated']


    ## override
    def get_readonly_fields(self, request, obj=None):
        if (obj): 
            return ('created', 'updated')
        return ()
## END class JobAdmin()


## BEGIN class
@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    model = Applicant
    list_display = ['first_name', 'last_name', 'job', 'created', 'updated']


    ## override
    def get_readonly_fields(self, request, obj=None):
        if (obj): 
            return ('created', 'updated')
        return ()
## END class ApplicantAdmin()