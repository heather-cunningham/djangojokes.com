from common.admin import DjangoJokesAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


# Register your models here.
CustomUser = get_user_model()


## BEGIN model Class
@admin.register(CustomUser)
class CustomUserAdmin(DjangoJokesAdmin, UserAdmin):
    model = CustomUser

    ## When inheriting from a class, like this one does from `UserAdmin`,  
    # you may append to the superclass’s class attributes. 
    # BUT to do so correctly, you must know whether the
    #  superclass defined those attributes as lists or tuples.
    #
    ## For ex: The UserAdmin class defines list_display with a TUPLE like this:
    ##### list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    #
    ## As it is defined as a tuple, to add a field (e.g., 'is_superuser'),
    #  you must append a tuple:
    ##### list_display = UserAdmin.list_display + ('is_superuser',)
    #
    ## If you try to append a list, you will get a TypeError:
    #### TypeError: can only concatenate tuple (not "list") to tuple
    # 
    # For JokeAdmin class': autocomplete_fields = ['tags', 'user']:
    ## YOu do not need to add here:
    ##### `search_fields = ["user"]`
    ## ... Because this class, here, the class it inherits from (django.contrib.auth.admin.UserAdmin), 
    # which already defines search_fields as:
    #### `search_fields = ('username', 'first_name', 'last_name', 'email')`
    ## So, you don't have to add it again.        


    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Optional Fields',
            {
                'classes': ('wide',),
                'fields': ('email', 'first_name', 'last_name'),
            }
        ),## end inner tple
    )## end outer tple
## END CustomUser model Class
