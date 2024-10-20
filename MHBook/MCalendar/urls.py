from django.urls import path

from . import views

app_name = "MCalendar"

urlpatterns = [

    # Accessable via http://127.0.0.1:8000/MCalendar/example/
    path("example/", views.examplePage, name="example"),
    # Accessable via http://127.0.0.1:8000/MCalendar/myBookings/
    path("myBookings/", views.myBookings, name="myBookings"),
    # Accessable via http://127.0.0.1:8000/MCalendar/myBookings/editBooking/1
    path("myBookings/editBooking/<int:id>", views.editBooking, name="editBooking"),
    # Accessable via http://127.0.0.1:8000/MCalendar/requests/
    path("requests/", views.requests, name="requests"),
    
]