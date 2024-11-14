from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registrationPage, name = 'Hregister'),
    path('login/', views.loginPage, name="HloginPage"),
    path('logout/', views.logoutUser, name='Hlogout'),
    path('account/', views.accountPage, name='HaccountPage'),
]