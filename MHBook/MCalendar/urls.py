from django.urls import path
from . import views

#app_name = "MCalendar"

urlpatterns = [
    path('register/', views.registrationPage, name = 'registrationPage'),
    path('login/', views.loginPage, name="loginPage"),
    path('logout/', views.logoutUser, name='logout'),
    path('account/', views.accountPage, name='accountPage'),
    path('changePassword/', views.changePasswordPage, name = 'changePassword'),
    path("example/", views.examplePage, name="example"),
]
