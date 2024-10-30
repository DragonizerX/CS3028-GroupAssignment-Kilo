from django.urls import path
from . import views

#app_name = "MCalendar"

urlpatterns = [
    path('register/', views.registrationPage, name = 'registrationPage'),
    path('login/', views.loginPage, name="loginPage"),
    path('logout/', views.logoutUser, name='logout'),
    path('account/', views.accountPage, name='accountPage'),
    path('changePassword/', views.changePasswordPage, name = 'changePassword'),
    # Accessable via http://127.0.0.1:8000/MCalendar/myBookings/
    path("myBookings/", views.myBookings, name="myBookings"),
    # Accessable via http://127.0.0.1:8000/MCalendar/myBookings/editBooking/1
    path("myBookings/editBooking/<int:id>", views.editBooking, name="editBooking"),
    # Accessable via http://127.0.0.1:8000/MCalendar/requests/
    path("requests/", views.requests, name="requests"),

    path('cancelBooking/<int:id>/', views.cancelBooking, name='cancelBooking'),

    path("confirmAccept/<int:id>/", views.confirmAccept, name="confirmAccept"),
    path("confirmReject/<int:id>/", views.confirmReject, name="confirmReject"),
    

    # Accessable via http://127.0.0.1:8000/MCalendar/home/
    path("", views.home, name="home"),
    path('create-event/', views.create_event, name='create_event'),
    path('get_events/', views.get_events, name='get_events'),
    path('CalendarPageAdmin/', views.AdminCalendarView, name='CalendarPageAdmin'),

    # Accessable via http://127.0.0.1:8000/MCalendar/billing/
    path("billing/", views.billing, name="billings"),

]
