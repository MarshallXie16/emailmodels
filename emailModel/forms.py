from django import forms
from .models import User

class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        widgets = {
            "first_name" : forms.TextInput(attrs={'placeholder': 'First Name'}),
            "last_name" : forms.TextInput(attrs={'placeholder': 'Last Name'}),
            "email" : forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            "password" : forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)