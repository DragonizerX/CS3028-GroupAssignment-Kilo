from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registrationPage),
    path('login/', views.loginPage),
    path('account/', views.accountPage)
]