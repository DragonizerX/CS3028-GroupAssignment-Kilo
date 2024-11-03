from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie


from django.contrib.admin.views.decorators import staff_member_required

import uuid
from .models import Users, Event, Equipment, Billing, Event
from .forms import CreateUserForm, UpdateUserForm, ChangePasswordForm, AddEquipmentForm

from django.core.mail import send_mail
from django.conf import settings
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
                    return redirect('CalendarPage')
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
    if request.user.is_superuser:
        myBookings = Event.objects.all().values()
        template = loader.get_template('myBookings.html')
        context = {
            'myBookings': myBookings,
        }
        return HttpResponse(template.render(context, request))
    if request.user.is_authenticated: ####
        current_user = request.user.email
        myBookings = Event.objects.filter(email=current_user)
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
        hasRequest = requests.filter(verified=False).exists()
        context = {
            'requests': requests,
            'hasRequest': hasRequest
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")

def cancelBooking(request, id):
    booking = get_object_or_404(Event, id=id)
    booking.delete()
    return redirect('myBookings')

def confirmAccept(request, id):
    requests = get_object_or_404(Users, id=id)
    requests.verified = True
    send_mail(
        "Your Account Is Verified!",
        "Congratulations!\n\nYour account has been verified and is in our HistoTrack system. You may now log in.",
        "histotrackltd@gmail.com",
        [requests.email],
        fail_silently=False,
    )
    requests.save()
    return redirect('requests')

def confirmReject(request, id):
    requests = get_object_or_404(Users, id=id)
    requests.delete()
    return redirect('requests')

def editBooking(request, id):
    if request.user.is_authenticated:
        booking = get_object_or_404(Event, id=id)
        equipmentList = Equipment.objects.all()
        
        if request.method == 'POST':
            """bookingName = request.POST.get('bookingName')
            if bookingName:
                booking.bookingName = bookingName"""

            supervisorName = request.POST.get('supervisorName')
            if supervisorName:
                booking.supervisorName = supervisorName

            bookingDate = request.POST.get('bookingDate')
            if bookingDate:
                booking.bookingDate = bookingDate

            startTime = request.POST.get('startTime')
            if startTime:
                booking.startTime = startTime

            finishTime = request.POST.get('finishTime')
            if finishTime:
                booking.finishTime = finishTime

            comments = request.POST.get('comments')
            if comments:
                booking.comments = comments

            equipment = request.POST.get('equipment')
            if equipment:
                booking.equipment = equipment

            booking.save()
            return redirect('myBookings')

        template = loader.get_template('editBooking.html')
        context = {
            'editBooking': [booking],
            'equipmentList': equipmentList
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.success(request, "Please log in before entering that page!")
        return redirect("loginPage")

@ensure_csrf_cookie
def calendar_view(request):
    return render(request, 'CalendarPage.html')

@ensure_csrf_cookie
def create_event(request):
    if request.method == 'POST':
        try:
            
            booking_Name = f"{request.user.first_name} {request.user.last_name}"
            supervisor_Name = request.POST.get('supervisorName')
            email_ = request.user.email
            booking_Date = request.POST.get('bookingDate')
            start_Time = request.POST.get('startTime')
            finish_Time = request.POST.get('finishTime')
            comments_ = request.POST.get('comments')
            equipment_ = request.POST.get('equipment')
            
        
            event = Event(
                bookingName=booking_Name,
                supervisorName=supervisor_Name,
                email=email_,
                bookingDate=booking_Date,
                startTime=start_Time,
                finishTime = finish_Time,
                comments=comments_,
                equipment=equipment_,
            )
            event.save()

            return JsonResponse({
                'status': 'success',
                'event': {
                    'title': f"{event.bookingName} - {event.equipment}",
                    'start': f"{event.bookingDate}T{event.startTime}",
                    'end': f"{event.bookingDate}T{event.finishTime}",
                }
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def get_events(request):
    try:
        equipment = request.GET.get('equipment', '')
        
        if equipment:
            events = Event.objects.filter(equipment=equipment)
        else:
            events = Event.objects.none()
            
        event_list = []
        for event in events:
            event_data = {
                'title': f"{event.bookingName} - {event.equipment}",
                'start': f"{event.bookingDate}T{event.startTime}",
                'end': f"{event.bookingDate}T{event.finishTime}",
                'supervisorName': event.supervisorName,
                'comments': event.comments,
                'totalTime': event.totalTime
            }
            event_list.append(event_data)
            
        return JsonResponse(event_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def add_equipment(request):
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('CalendarPageAdmin')  # Redirect to a success page or another view
            else:
                return redirect('CalendarPage')
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = AddEquipmentForm()
    
    # Render the form in case of GET request or invalid POST
    if request.user.is_superuser:
        return render(request, 'CalendarPageAdmin.html', {'form': form})
    else:
        return render(request, 'CalendarPage.html', {'form': form})
    
def delete_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('delete_equipment')
        try:
            equipment = Equipment.objects.get(equipmentID_auto=equipment_id)
            equipment.delete()
            return redirect('CalendarPageAdmin')  # Redirect after deletion
        except Equipment.DoesNotExist:
            return HttpResponse("Equipment not found.", status=404)
    
    # If it's a GET request, render the deletion form with the dropdown
    equipment_list = Equipment.objects.all()
    return render(request, 'CalendarPageAdmin.html', {'equipmentList': equipment_list})

def CalendarPage(request):
    if request.user.is_authenticated:
        equipment_list = Equipment.objects.all()
        return render(request, 'CalendarPage.html', {'equipmentList': equipment_list})
    else:
        messages.success(request, "Please log in before entering that page!")
        return redirect("loginPage")


def AdminCalendarView(request):
    if request.user.is_superuser:
        equipment_list = Equipment.objects.all()
        return render(request, 'CalendarPageAdmin.html', {'equipmentList': equipment_list})
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")
    

def archivePage(request):
    if request.user.is_superuser:
        eventList = Event.objects.all()
        equipmentList = Equipment.objects.all()

        bookingName = request.GET.get('bookingName')
        supervisorName = request.GET.get('supervisorName')
        dateMin = request.GET.get('dateMin')
        dateMax = request.GET.get('dateMax')
        equipment = request.GET.get('equipment')
        #print(bookingName, supervisorName)

        if archiveValidQuery(bookingName):
            eventList = eventList.filter(bookingName__icontains=bookingName)

        if archiveValidQuery(supervisorName):
            eventList = eventList.filter(supervisorName__icontains=supervisorName)

        if archiveValidQuery(dateMin):
            eventList = eventList.filter(bookingDate__gte=dateMin)

        if archiveValidQuery(dateMax):
            eventList = eventList.filter(bookingDate__lte=dateMax)

        if archiveValidQuery(equipment) and equipment != 'Select...':
            eventList = eventList.filter(equipment__name=equipment)


        context = {
            'eventList': eventList,
            'equipmentList': equipmentList
        }

        return render(request, 'archive.html', context)
    
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")


def archiveValidQuery(param): # createBilling is using this aswell to sort through filters. Thanks!
    return param != '' and param is not None

# createBilling functions
def generateInvoiceRef():
    return str(uuid.uuid4())[:10]

def createBilling(request):

    if request.user.is_superuser:
        eventList = Event.objects.all()
        equipmentList = Equipment.objects.all()

        supervisorName = request.GET.get('supervisorName')
        dateMin = request.GET.get('dateMin')
        dateMax = request.GET.get('dateMax')

        if archiveValidQuery(supervisorName):
            eventList = eventList.filter(supervisorName__icontains=supervisorName)

        if archiveValidQuery(dateMin):
            eventList = eventList.filter(bookingDate__gte=dateMin)

        if archiveValidQuery(dateMax):
            eventList = eventList.filter(bookingDate__lte=dateMax)

        context = {
        'eventList': eventList,
        'equipmentList': equipmentList,
        }

        if request.method == "POST":
            selectedEvents = request.POST.getlist('selectEvent')
            selectedEventObjects = Event.objects.filter(id__in=selectedEvents)

            supervisors = selectedEventObjects.values_list('supervisorName').distinct()

            if supervisors.count() > 1:
                messages.error(request, "Can only create billings for one Supervisor at most.")
                return render(request, 'createBilling.html', context)

            billing = Billing()
            billing.invoiceRef = generateInvoiceRef()          
            billing.supervisor = supervisors.first()
            billing.save()

            billing.events.set(selectedEventObjects)

            equipment_names = selectedEventObjects.values_list('equipment', flat=True).distinct()
            billing.equipment.set(equipment_names)

            billing.save()

            messages.success(request, "Billing created")

        return render(request, 'createBilling.html', context)
    
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")
    
def billings(request):

    if request.user.is_superuser:
        billingsList = Billing.objects.all()
        equipmentList = Equipment.objects.all()
        events = Event.objects.all()

        supervisorName = request.GET.get('supervisorName')
        dateMin = request.GET.get('dateMin')
        dateMax = request.GET.get('dateMax')

        if archiveValidQuery(supervisorName):
            billingsList = billingsList.filter(supervisor__icontains=supervisorName)

        if archiveValidQuery(dateMin):
            billingsList = billingsList.filter(issueDate__gte=dateMin)

        if archiveValidQuery(dateMax):
            billingsList = billingsList.filter(issueDate__lte=dateMax)

        context = {
        'billingsList': billingsList,
        'equipmentList': equipmentList,
        'events': events
        }

        return render(request, 'billings.html', context)
    
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")
    
