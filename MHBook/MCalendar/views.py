from django.shortcuts import render
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
    editBooking = Bookings.objects.get(id=id)
    template = loader.get_template('editBooking.html')
    context = {
        'editBooking': editBooking,
    }
    return HttpResponse(template.render(context, request))