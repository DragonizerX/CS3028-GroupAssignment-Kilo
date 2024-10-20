from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from django.template import loader
from .models import Bookings

# Create your views here.

def examplePage(request):
    return render(request, 'example.html')

def myBookings(request):
    myBookings = Bookings.objects.all().values()
    template = loader.get_template('myBookings.html')
    context = {
        'myBookings': myBookings,
    }
    return HttpResponse(template.render(context, request))

def editBooking(request, id):
    booking = get_object_or_404(Bookings, id=id)
    
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        if fullname:
            booking.fullname = fullname

        phone = request.POST.get('phone')
        if phone:
            booking.phone = int(phone)

        email = request.POST.get('email')
        if email:
            booking.email = email

        supervisor = request.POST.get('supervisor')
        if supervisor:
            booking.supervisor = supervisor

        organisation = request.POST.get('organisation')
        if organisation:
            booking.organisation = organisation

        date = request.POST.get('date')
        if date:
            booking.date = date

        start = request.POST.get('start')
        if start:
            booking.start = start

        finish = request.POST.get('finish')
        if finish:
            booking.finish = finish

        room = request.POST.get('room')
        if room:
            booking.room = room

        equipment = request.POST.get('equipment')
        if equipment:
            booking.equipment = equipment

        equipmentid = request.POST.get('equipmentid')
        if equipmentid:
            booking.equipmentid = equipmentid

        booking.save()

    template = loader.get_template('editBooking.html')
    context = {
        'editBooking': [booking],
    }
    return HttpResponse(template.render(context, request))