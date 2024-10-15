from django.shortcuts import render

# Create your views here.

def loginPage(request):
    return render(request, 'login.html')

def registrationPage(request):
    return render(request, 'register.html')

def accountPage(request):
    return render(request, 'account.html')