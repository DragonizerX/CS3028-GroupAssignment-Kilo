from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms

from MCalendar.models import Users

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):

    password = None

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'telephone']


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = Users
        fields = ['new_password1', 'new_password2']