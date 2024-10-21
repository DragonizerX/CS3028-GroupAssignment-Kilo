from django.shortcuts import render, redirect
from .models import Event
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def create_event(request):
    if request.method == 'POST':
        booking_Name = request.POST.get('bookingName')
        supervisor_Name = request.POST.get('supervisorName')
        booking_Date = request.POST.get('bookingDate')
        start_Time = request.POST.get('startTime')
        alloted_Time = request.POST.get('allottedTime')
        comments_ = request.POST.get('comments')
        equipment_ = request.POST.get('equipment')
    
        event = Event(
            bookingName = booking_Name,
            supervisorName = supervisor_Name,
            bookingDate = booking_Date,
            startTime = start_Time,
            allotedTime = alloted_Time,
            comments = comments_,
            equipment = equipment_
        )
        event.save()

        return JsonResponse({
            'status': 'success',
            'event': {
                'title': f"{event.bookingName} - {event.equipment}",
                'start': f"{event.bookingDate}T{event.startTime}",
                'end': f"{event.bookingDate}T{event.allotedTime}",
            }
        })

        return HttpResponse("Booking created!")
    return HttpResponse(request='CalendarPage.html')

def get_events(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'title': f"{event.bookingName} - {event.equipment}",
            'start': f"{event.bookingDate}T{event.startTime}",
            'end': f"{event.bookingDate}T{event.allotedTime}",
        })
    return JsonResponse(event_list, safe=False)

def home(request):
    return render(request,"CalendarPage.html")

@staff_member_required
def AdminCalendarView(request):
    return render(request, 'CalendarPageAdmin.html')