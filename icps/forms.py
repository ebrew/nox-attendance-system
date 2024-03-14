from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.widgets import NumberInput
from .models import *

User = get_user_model()


class LoginForm(forms.ModelForm):
    email = forms.EmailField(initial='you@example.com')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']


class RegisterForm(UserCreationForm):
    options = [('standard', 'Standard User'), ('admin', 'Administrator')]
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=20, required=True, help_text='First and other names')
    last_name = forms.CharField(max_length=20, required=True, help_text='Surname')
    access = forms.ChoiceField(choices=options)
    # phone_number = forms.CharField(required=True, max_length=13, help_text='Include country code')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'access', 'password1', 'password2')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']



