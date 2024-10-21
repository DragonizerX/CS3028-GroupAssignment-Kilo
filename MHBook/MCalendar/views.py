from django.shortcuts import render, redirect
from .forms import CreateUserForm, UpdateUserForm, ChangePasswordForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Users



from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def loginPage(request):
    if request.method == "POST":
        email = request.POST.get('email') #pulls email and password from login page
        password = request.POST.get('password')
        print('email: ', email, 'password', password)
        user = authenticate(email=email, password=password) #authenticates users
        print(user)
        if user is not None: #if user exists in database
            if user.verified == True:
                login(request, user)
                return redirect('accountPage')
            else:
                messages.info(request, 'Your account has not been approved by the admins yet!')
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


@login_required(login_url='loginPage') #Method 1 for making sure user in logged in to access this page.
def accountPage(request):
    user = Users.objects.get(id=request.user.id) #Get both current user and current form.
    form = UpdateUserForm(request.POST or None, instance=user)
    if request.method == 'POST':
        form = UpdateUserForm(data=request.POST, instance=request.user)

        if form.is_valid(): #If the form's data is valid then data is saved and redirected.
            form.save()
            messages.success(request, "User has been updated!")
            return redirect("accountPage")
        
        else:
            form = UpdateUserForm(instance=request.user) #Even if not valid, will display saved data.
        
        return render(request, 'account.html', {"form" :form} )
    return render(request, 'account.html', {"form" :form})


def changePasswordPage(request):
    if request.user.is_authenticated: #Method 2 for making sure user in logged in to access this page.
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid(): #If the form's data is valid then data is
                form.save()
                messages.success(request, "Your Password Has Been Updated, Please Log In Again")
                return redirect('loginPage')

            else:
                for error in list(form.errors.values()): #Displays error messages as to why password wasn't accepted.
                    messages.error(request,error)
                    return redirect('changePassword')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'changePassword.html', {'form':form})
        
    else:
        messages.success(request, "Please log in before entering that page!")
        return redirect("loginPage")

def examplePage(request):
    return render(request, 'example.html')

