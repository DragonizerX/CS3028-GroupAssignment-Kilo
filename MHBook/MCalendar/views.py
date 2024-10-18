from django.shortcuts import render
from django.views import generic

# Create your views here.

def CalendarPage(request):
    return render(request, 'CalendarPage.html')
