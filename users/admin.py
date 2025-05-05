from common.admin import DjangoJokesAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from common.utils.admin import (append_fields_to_fieldset, move_fieldset_fields, 
                                remove_fields_from_fieldset)


# Register your models here.
CustomUser = get_user_model()


## BEGIN model Class
@admin.register(CustomUser)
class CustomUserAdmin(DjangoJokesAdmin, UserAdmin):
    model = CustomUser
    ## Admin fields
    #### Existing User
    #------------------
    ## Be sure to add trailing commas here, so Python/Django knows these are not just Strings:
    list_display = UserAdmin.list_display + ('is_superuser', ) 
    list_display_links = ('username', 'email', 'first_name', 'last_name', )
    ## Add User fields to "Personal Info" heading in Django Admin for editing an existing user.
    new_personal_info_fields_to_add = ('dob', 'avatar', )
    #### New Users
    #--------------
    ## Add fields to the form for adding a new user.
    new_user_fields_to_add = ('email', )
    # Add optional fields to new 'Optional Fields' fieldset.
    optional_new_user_fields = ('first_name', 'last_name', 'dob', )


    #### Existing User
    #------------------
    ## Add, move, remove Admin fields: "Personal info"
    # Add
    append_fields_to_fieldset(UserAdmin.fieldsets, "Personal info", new_personal_info_fields_to_add)
    # Move the `email` field from "Personal info" fieldset to the unlabelled (no heading) fieldset
    move_fieldset_fields(UserAdmin.fieldsets, "Personal info", None, ('email', ))
    # Remove
    # Remove password field from the (no heading) fieldset, since it takes up a lot of space
    #  and only links to the 'Reset Password' button.
    remove_fields_from_fieldset(UserAdmin.fieldsets, None, ('password', ))


    #### New Users
    #--------------
    ## Add, move, remove Admin fields: 
    # Add new fields to New User unlabelled (no heading) fieldset.
    add_fieldsets = append_fields_to_fieldset(UserAdmin.add_fieldsets, None, new_user_fields_to_add)
    # Add optional fields to new 'Optional Fields' fieldset.
    add_fieldsets = append_fields_to_fieldset(UserAdmin.add_fieldsets, 'Optional Fields', 
                                              optional_new_user_fields)


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



    ## Using imported common utils fcns to add, move, and remove fields instead:
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     (
    #         'Optional Fields',
    #         {
    #             'classes': ('wide',),
    #             'fields': ('email', 'first_name', 'last_name'),
    #         }
    #     ),## end inner tple
    # )## end outer tple
## END CustomUser model Class
