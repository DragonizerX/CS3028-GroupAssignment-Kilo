from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms

from MCalendar.models import Users, Event, Equipment

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
    user_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="User's Email"
    )

    class Meta:
        model = Event
        fields = ['bookingName', 'supervisorName', 'bookingDate', 'startTime', 'finishTime', 'notes', 'equipment', 'hourlyRate']

        widgets = {
            'bookingName': forms.TextInput(attrs={'class': 'form-control'}),
            'supervisorName':forms.TextInput(attrs={'class': 'form-control'}),
            'bookingDate': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'start_time':forms.TimeInput(attrs={'class':'form-control','type':'time'}),
            'finish_time': forms.TimeInput(attrs={'class':'form-control','type':'time'}),
            'notes':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'hourlyRate': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True})
            
        }


class AddEquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['equipmentName', 'hourlyRate']

        widgets = {
            'equipmentName': forms.TextInput(attrs={'class': 'form-control'}),
            'hourlyRate':forms.TextInput(attrs={'class': 'form-control'}),

        }