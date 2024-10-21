#forms.py

from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['bookingName', 'supervisorName', 'bookingDate', 'startTime', 'allotedTime', 'comments']

        widgets = {
            'bookingName': forms.TextInput(attrs={'class': 'form-control'}),
            'supervisorName':forms.TextInput(attrs={'class': 'form-control'}),
            'bookingDate': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'start_time':forms.TimeInput(attrs={'class':'form-control','type':'time'}),
            'alloted_time': forms.TimeInput(attrs={'class':'form-control','type':'time'}),
            'comments':forms.Textarea(attrs={'class':'form-contorl','rows':3})
        }



