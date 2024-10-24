from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader


from django.contrib.admin.views.decorators import staff_member_required

from .models import Bookings, Users, Event
from .forms import CreateUserForm, UpdateUserForm, ChangePasswordForm
# Create your views here.b

def loginPage(request):
    if request.method == "POST":
        email = request.POST.get('email') #pulls email and password from login page
        password = request.POST.get('password')
        print('email: ', email, 'password', password)
        user = authenticate(email=email, password=password) #authenticates users
        #print(user)
        if user is not None: #if user exists in database
            if user.verified == True:
                #print(user.is_superuser)
                if user.is_superuser:
                    #print("A")
                    login(request, user)
                    return redirect('CalendarPageAdmin')
                else:
                    #print("B")
                    login(request, user)
                    return redirect('home')
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


#@login_required(login_url='loginPage') #Method 1 for making sure user in logged in to access this page.
def accountPage(request):
    if request.user.is_authenticated:
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
    else:
        messages.success(request, "Please log in before entering that page!")
        return redirect("loginPage")

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
    

def myBookings(request):
    if request.user.is_authenticated:
        myBookings = Bookings.objects.all().values()
        template = loader.get_template('myBookings.html')
        context = {
            'myBookings': myBookings,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.success(request, "Please log in before entering that page!")
        return redirect("loginPage")

def requests(request):
    if request.user.is_superuser:
        requests = Users.objects.all().values()
        template = loader.get_template('requests.html')
        context = {
            'requests': requests,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")

def cancelBooking(request, id):
    booking = get_object_or_404(Bookings, id=id)
    booking.delete()
    return redirect('myBookings')

def confirmAccept(request, id):
    requests = get_object_or_404(Users, id=id)
    requests.verified = True
    requests.save()
    return redirect('requests')

def confirmReject(request, id):
    requests = get_object_or_404(Users, id=id)
    requests.delete()
    return redirect('requests')

def editBooking(request, id):
    if request.user.is_authenticated:
        booking = get_object_or_404(Bookings, id=id)
        
        if request.method == 'POST':
            fullname = request.POST.get('fullname')
            if fullname:
                booking.fullname = fullname

            phone = request.POST.get('phone')
            if phone:
                booking.phone = int(phone)

            email = request.POST.get('email')
            if email:
                booking.email = email

            supervisor = request.POST.get('supervisor')
            if supervisor:
                booking.supervisor = supervisor

            organisation = request.POST.get('organisation')
            if organisation:
                booking.organisation = organisation

            date = request.POST.get('date')
            if date:
                booking.date = date

            start = request.POST.get('start')
            if start:
                booking.start = start

            finish = request.POST.get('finish')
            if finish:
                booking.finish = finish

            room = request.POST.get('room')
            if room:
                booking.room = room

            equipment = request.POST.get('equipment')
            if equipment:
                booking.equipment = equipment

            equipmentid = request.POST.get('equipmentid')
            if equipmentid:
                booking.equipmentid = equipmentid

            booking.save()
            return redirect('MCalendar:myBookings')

        template = loader.get_template('editBooking.html')
        context = {
            'editBooking': [booking],
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.success(request, "Please log in before entering that page!")
        return redirect("loginPage")

def create_event(request):
    if request.method == 'POST':
        booking_Name = request.POST.get('bookingName')
        supervisor_Name = request.POST.get('supervisorName')
        booking_Date = request.POST.get('bookingDate')
        start_Time = request.POST.get('startTime')
        alloted_Time = request.POST.get('allottedTime')
        comments_ = request.POST.get('comments')
        equipment_ = request.POST.get('equipment')
    
        event = Event(
            bookingName = booking_Name,
            supervisorName = supervisor_Name,
            bookingDate = booking_Date,
            startTime = start_Time,
            allotedTime = alloted_Time,
            comments = comments_,
            equipment = equipment_
        )
        event.save()

        return JsonResponse({
            'status': 'success',
            'event': {
                'title': f"{event.bookingName} - {event.equipment}",
                'start': f"{event.bookingDate}T{event.startTime}",
                'end': f"{event.bookingDate}T{event.allotedTime}",
            }
        })

        return HttpResponse("Booking created!")
    return HttpResponse(request='CalendarPage.html')

def get_events(request):
    events = Event.objects.all()
    #print(events)
    event_list = []
    for event in events:
        event_list.append({
            'title': f"{event.bookingName} - {event.equipment}",
            'start': f"{event.bookingDate}T{event.startTime}",
            'end': f"{event.bookingDate}T{event.allotedTime}",
        })
    return JsonResponse(event_list, safe=False)

def home(request):
    if request.user.is_authenticated:
        return render(request,"CalendarPage.html")
    else:
        messages.success(request, "Please log in before entering that page!")
        return redirect("loginPage")


def AdminCalendarView(request):
    if request.user.is_superuser:
        return render(request, 'CalendarPageAdmin.html')
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")