from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from MCalendar.models import Users

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

