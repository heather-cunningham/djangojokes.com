from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.db import models
from django.urls import reverse


## helper fcns
def validate_avatar(img):
    width, height = get_image_dimensions(img)
    if(width > 200 or height > 200):
        raise ValidationError("Avatar/profile pic may be no larger than 200 x 200 pixels.")
    return


## BEGIN 
class CustomUser(AbstractUser):
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, 
                               help_text="Must be a jpg, jpeg, jfif, or png no larger than 200 x 200px.", 
                               validators=[validate_avatar])
    

    def get_absolute_url(self):
        return reverse('my-account')
## END class/model