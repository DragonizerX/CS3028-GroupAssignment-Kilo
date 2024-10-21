from django.shortcuts import render, redirect
from .models import Event
from django.http import HttpResponse

# Create your views here.

def create_event(request):
    if request.method == 'POST':
        booking_Name = request.POST.get('bookingName')
        supervisor_Name = request.POST.get('supervisorName')
        booking_Date = request.POST.get('bookingDate')
        start_Time = request.POST.get('startTime')
        alloted_Time = request.POST.get('allottedTime')
        comments_ = request.POST.get('comments')
    
        event = Event(
            bookingName = booking_Name,
            supervisorName = supervisor_Name,
            bookingDate = booking_Date,
            startTime = start_Time,
            allotedTime = alloted_Time,
            comments = comments_
        )
        event.save()

        return HttpResponse("Booking created!")
    return render(request='CalendarPage.html')

def home(request):
    return render(request,"CalendarPage.html")