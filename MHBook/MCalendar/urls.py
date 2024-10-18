from django.urls import path

from . import views

app_name = "MCalendar"

urlpatterns = [

    # Accessable via http://127.0.0.1:8000/MCalendar/CalendarPage/
    path("CalendarPage/", views.CalendarPage, name="CalendarPage"),
    
]