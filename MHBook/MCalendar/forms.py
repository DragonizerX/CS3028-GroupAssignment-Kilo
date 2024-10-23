from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms

from MCalendar.models import Users, Event

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
#forms.py



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['bookingName', 'supervisorName', 'bookingDate', 'startTime', 'allotedTime', 'comments', 'equipment']

        widgets = {
            'bookingName': forms.TextInput(attrs={'class': 'form-control'}),
            'supervisorName':forms.TextInput(attrs={'class': 'form-control'}),
            'bookingDate': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'start_time':forms.TimeInput(attrs={'class':'form-control','type':'time'}),
            'alloted_time': forms.TimeInput(attrs={'class':'form-control','type':'time'}),
            'comments':forms.Textarea(attrs={'class':'form-contorl','rows':3}),
            'equipment': forms.Select(attrs={'class': 'form-control'})

        }



