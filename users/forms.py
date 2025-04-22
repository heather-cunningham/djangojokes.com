from django import forms
from allauth.account.forms import SignupForm


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
## END class