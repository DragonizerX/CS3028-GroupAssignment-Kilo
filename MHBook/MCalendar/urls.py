from django.urls import path
from . import views
from django.shortcuts import render
from django.conf.urls import handler404
from .views import custom_404_view

handler404 = custom_404_view

#app_name = "MCalendar"

urlpatterns = [
    # Accessable via http://127.0.0.1:8000/MCalendar/
    path('register/', views.registrationPage, name = 'registrationPage'),
    path('login/', views.loginPage, name="loginPage"),
    path('logout/', views.logoutUser, name='logout'),
    path('account/', views.accountPage, name='accountPage'),
    path('changePassword/', views.changePasswordPage, name = 'changePassword'),
    path('add_supervisor/', views.add_supervisor, name='add_supervisor'),
    path('clear_cancelled_bookings/', views.clear_cancelled_bookings, name='clear_cancelled_bookings'),
    path("myBookings/", views.myBookings, name="myBookings"),
    path("myBookings/editBooking/<int:id>", views.editBooking, name="editBooking"),
    path("requests/", views.requests, name="requests"),
    path('cancelBooking/<int:id>/', views.cancelBooking, name='cancelBooking'),
    path("confirmAccept/<int:id>/", views.confirmAccept, name="confirmAccept"),
    path("confirmReject/<int:id>/", views.confirmReject, name="confirmReject"),
    path("archive/", views.archivePage, name="archivePage"),
    path("CalendarPage/", views.CalendarPage, name="CalendarPage"),
    path('CalendarPage/add_equipment/', views.add_equipment, name='add_equipment'),
    path('CalendarPage/delete_equipment/', views.delete_equipment, name='delete_equipment'),
    path('CalendarPage/create-event/', views.create_event, name='create_event'),
    path('CalendarPage/get_events/', views.get_events, name='get_events'),
    path('CalendarPageAdmin/get_events/', views.get_events, name='get_events'),
    path("CalendarPageAdmin/", views.AdminCalendarView, name='CalendarPageAdmin'),
    path("createBilling/", views.createBilling, name="createBilling"),
    path("billings/", views.billings, name="billings"),
    path('generatePDF/<int:id>/', views.generatePDF, name='generatePDF'),
    path('deleteBilling/<int:id>/', views.deleteBilling, name='deleteBilling'),
    path('deleteEvent/', views.deleteEvent, name='deleteEvent'),
]
