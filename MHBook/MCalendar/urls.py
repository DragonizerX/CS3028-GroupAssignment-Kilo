from django.urls import path

from . import views

app_name = "MCalendar"

urlpatterns = [

    # Accessable via http://127.0.0.1:8000/
    path("", views.home, name="home"),
    path('create-event/', views.create_event, name='create_event'),
    path('get_events/', views.get_events, name='get_events'),
    path('CalendarPageAdmin/', views.AdminCalendarView, name='CalendarPageAdmin'),
]