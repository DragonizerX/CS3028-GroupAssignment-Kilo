from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse



from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username') #pulls email and password from login page
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password) #authenticates users
        if user is not None: #if user exists in database
            login(request, user)
            return redirect('accountPage')
        else:
            messages.info(request, 'username OR password is incorrect')
            
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

def registrationPage(request):
    form = CreateUserForm() #grabs form structure from forms.py
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid(): #if form completed successfully save form
            form.save()
            user = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for ' + user) #flash message to user that form created successfuly 
            return redirect("loginPage")
        
                    
    context = {'form': form}
    return render(request, 'register.html', context)

@login_required(login_url='loginPage')
def accountPage(request):
    return render(request, 'account.html')