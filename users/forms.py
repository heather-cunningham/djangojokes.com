from datetime import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from allauth.account.forms import SignupForm


## BEGIN class
class MySignupForm(SignupForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    # password1 = forms.CharField(label="Password",
    #     widget=forms.PasswordInput(attrs={"class": "form-control", "label": "Password",
    #                                       "placeholder": "Enter a password",}))
    # password2 = forms.CharField(label="Confirm Password",
    #     widget=forms.PasswordInput(attrs={"class": "form-control", "label": "Confirm Password",
    #                 "placeholder": "Confirm password",}))


    def signup(self, request, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        # user.password1 = self.cleaned_data["password1"]
        # user.password2 = self.cleaned_data["password2"]
        user.save()


    # def clean_password2(self):
    #     if self.cleaned_data.get("password1") != self.cleaned_data.get("password2"):
    #         raise forms.ValidationError("Passwords must match.")
    #     return self.cleaned_data["password2"]
## END class MySignupForm()


## BEGIN class
class CustomUserChangeForm(UserChangeForm):
    password = None
    

    ## subclass
    class Meta:
        BIRTH_YEAR_CHOICES = range((datetime.now().year - 111), datetime.now().year + 1)
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'dob')
        widgets = {
            'dob': forms.SelectDateWidget(
                attrs={'style': 'width: 31%; display: inline-block; margin: 0 1%;'},
                years = BIRTH_YEAR_CHOICES
            )
        }
    ## END subclass
## END class CustomUserChangeForm()
