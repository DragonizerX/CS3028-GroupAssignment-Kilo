from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone, dateformat

from reportlab.pdfgen import canvas # type: ignore
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator

import uuid, io
from .models import Users, Event, Equipment, Billing, Supervisor, CancelledBooking

from .forms import CreateUserForm, UpdateUserForm, ChangePasswordForm, AddEquipmentForm

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


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
            if form.is_valid(): 
                form.save()
                changePasswordText = ("Your password was successfully changed at  %s. You can now log in to HistoTrack with your new password." % str(dateformat.format((timezone.now()), 'Y-m-d H:i:s')))
                send_mail(
                    "Your Password Has Changed!",
                    changePasswordText,
                    "histotrackltd@gmail.com",
                    [request.user.email],
                    fail_silently=False,
                )
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
        myBookings = Event.objects.filter(bookingDate__gte=timezone.now().date())
        template = loader.get_template('myBookings.html')
        hasBooking = myBookings.exists()

        # Paginator yaya
        paginator = Paginator(myBookings, 10)
        pageNumber = request.GET.get('page')
        pageObj = paginator.get_page(pageNumber)
        #print(myBookings)

        context = {
            'myBookings': myBookings,
            'hasBooking': hasBooking,
            'pageObj': pageObj,
        }
        return HttpResponse(template.render(context, request))
    
    if request.user.is_authenticated:
        current_user = request.user.email
        myBookings = Event.objects.filter(email=current_user, bookingDate__gte=timezone.now().date())
        template = loader.get_template('myBookings.html')
        hasBooking = myBookings.exists()

        # Paginator
        paginator = Paginator(myBookings, 10)
        pageNumber = request.GET.get('page')
        pageObj = paginator.get_page(pageNumber)

        context = {
            'myBookings': myBookings,
            'hasBooking': hasBooking,
            'pageObj': pageObj,
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

        # Paginator
        paginator = Paginator(requests, 12) # For some reason it displays 2 less than what this value is ?? Currently it will display 10
        pageNumber = request.GET.get('page')
        pageObj = paginator.get_page(pageNumber)

        context = {
            'requests': requests,
            'hasRequest': hasRequest,
            'pageObj': pageObj,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")



def cancelBooking(request, id):
    if id is None:
        return redirect('myBookings')
    booking = get_object_or_404(Event, id=id)
    if booking.bookingDate == timezone.now().date(): #check for same day cancelation
        CancelledBooking.objects.create(
            booking_name=booking.bookingName,
            cancelled_by=request.user,  # assumes the user is authenticated
            cancellation_date=timezone.now()
        )
    booking.delete()
    return redirect('myBookings')


def clear_cancelled_bookings(request):
    CancelledBooking.objects.all().delete()
    return redirect('CalendarPageAdmin') 


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
        supervisors = Supervisor.objects.all().order_by('first_name')
        
        if request.method == 'POST':
            new_date = request.POST.get('bookingDate')
            new_start = request.POST.get('startTime')
            new_finish = request.POST.get('finishTime')
            new_equipment = request.POST.get('equipment')

            # Check for overlapping bookings
            overlapping_bookings = Event.objects.filter(
                equipment=new_equipment,
                bookingDate=new_date,
                startTime__lt=new_finish,
                finishTime__gt=new_start
            ).exclude(id=id)  # Exclude current booking from check
            
            if overlapping_bookings.exists():
                context = {
                    'editBooking': [booking],
                    'equipmentList': equipmentList,
                    'supervisors': supervisors,
                    'error_message': "This time slot is already booked for this equipment."
                }
                return render(request, 'editBooking.html', context)

            """bookingName = request.POST.get('bookingName')
            if bookingName:
                booking.bookingName = bookingName"""

            supervisorName = request.POST.get('supervisorName')
            if supervisorName:
                supervisor = Supervisor.objects.get(id=supervisorName)
                supervisor_full_name = f"{supervisor.first_name} {supervisor.last_name}"
                booking.supervisorName = supervisor_full_name

            bookingDate = request.POST.get('bookingDate')
            if bookingDate:
                booking.bookingDate = bookingDate

            startTime = request.POST.get('startTime')
            if startTime:
                booking.startTime = startTime

            finishTime = request.POST.get('finishTime')
            if finishTime:
                booking.finishTime = finishTime

            notes = request.POST.get('notes')
            if notes:
                booking.notes = notes

            equipment = request.POST.get('equipment')
            if equipment:
                booking.equipment = equipment

            booking.save()
            return redirect('myBookings')

        template = loader.get_template('editBooking.html')
        context = {
            'editBooking': [booking],
            'equipmentList': equipmentList,
            'supervisors': supervisors
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.success(request, "Please log in before entering that page!")
        return redirect("loginPage")


@ensure_csrf_cookie
def calendar_view(request):
    return render(request, 'CalendarPage.html')


@ensure_csrf_cookie
@login_required
def create_event(request):
    if request.method == 'POST':
        try:
            
            booking_Name = f"{request.user.first_name} {request.user.last_name}"
            supervisor_Name = request.POST.get('supervisorName')
            email_ = request.user.email
            booking_Date = request.POST.get('bookingDate')
            start_Time = request.POST.get('startTime')
            finish_Time = request.POST.get('finishTime')
            notes = request.POST.get('notes')
            equipment_id = request.POST.get('equipment')
            equipment = Equipment.objects.get(equipmentID_auto=equipment_id)
            hourly_rate = equipment.hourlyRate

            supervisor = Supervisor.objects.get(id=supervisor_Name)
            supervisor_full_name = f"{supervisor.first_name} {supervisor.last_name}"

            email_ = request.POST.get('user_email') or request.user.email if request.user.is_superuser else request.user.email

            overlapping_bookings = Event.objects.filter(
                equipment=equipment.equipmentName,
                bookingDate=booking_Date,
                # Check if any existing booking overlaps with the new booking time range
                startTime__lt=finish_Time,   # Existing booking starts before the new booking ends
                finishTime__gt=start_Time    # Existing booking ends after the new booking starts
            ).exclude(email=email_)  # Exclude the same user's bookings if they are editing
            
            if overlapping_bookings.exists():
                return JsonResponse({
                    'status': 'error',
                    'message': f"This equipment is already booked by another user during the selected time slot."
                }, status=400)

            custom_price = request.POST.get('customPrice')
            if request.user.is_superuser and custom_price:
                try:
                    hourly_rate = float(custom_price)
                except ValueError:
                    # Handle case where custom price is not a valid number
                    hourly_rate = equipment.hourlyRate
        
            event = Event(
                bookingName=booking_Name,
                supervisorName=supervisor_full_name,
                email=email_,
                bookingDate=booking_Date,
                startTime=start_Time,
                finishTime = finish_Time,
                notes=notes,
                equipment=equipment.equipmentName,
                hourlyRate=hourly_rate,
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

@login_required
def get_events(request):
    try:
        equipment_id = request.GET.get('equipment', '')
        
        if equipment_id:
            equipment = Equipment.objects.get(equipmentID_auto=equipment_id)
            events = Event.objects.filter(equipment=equipment.equipmentName)
        else:
            events = Event.objects.none()
            
        event_list = []
        for event in events:
            event_data = {
                'title': f"{event.bookingName} - {event.equipment}",
                'start': f"{event.bookingDate}T{event.startTime}",
                'end': f"{event.bookingDate}T{event.finishTime}",
                'supervisorName': event.supervisorName,
                'notes': event.notes,
                'totalTime': event.totalTime,
                'hourlyRate': event.hourlyRate
            }
            event_list.append(event_data)
            
        #return redirect('/MCalendar/CalendarPage/')
        return JsonResponse(event_list, safe=False)
    except Exception as e:
        if request.user.is_superuser:
            return redirect('/MCalendar/CalendarPageAdmin/')
        else:
            return redirect('/MCalendar/CalendarPage/')

@login_required
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
    

@login_required
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

@login_required
def CalendarPage(request):
    if request.user.is_authenticated:
        equipment_list = Equipment.objects.all()
        supervisors = Supervisor.objects.all().order_by('first_name')
        context = {'equipmentList': equipment_list, #Combine both Equipment and Supervisor Dictionaries into context
                    'supervisors': supervisors
                    }
        return render(request, 'CalendarPage.html', context)
    else:
        messages.success(request, "Please log in before entering that page!")
        return redirect("loginPage")

@login_required
def AdminCalendarView(request):
    if request.user.is_superuser:
        equipment_list = Equipment.objects.all()
        supervisors = Supervisor.objects.all().order_by('first_name')

        today = timezone.now().date() #Filter Cancelation from today
        short_notice_cancellations = CancelledBooking.objects.filter(cancellation_date__date=today)
        short_notice_count = short_notice_cancellations.count()

        context = {'equipmentList': equipment_list, #Combine Equipment, Supervisor, Short_notice dictionaries into context
                    'supervisors': supervisors,
                    'short_notice_count': short_notice_count,
                    'short_notice_cancellations': short_notice_cancellations
                    }
        return render(request, 'CalendarPageAdmin.html', context)
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")
    
@login_required
def archivePage(request):
    if request.user.is_superuser:
        eventList = Event.objects.all()
        equipmentList = Equipment.objects.all()

        bookingName = request.GET.get('bookingName')
        supervisorName = request.GET.get('supervisorName')
        notes = request.GET.get('notes')
        dateMin = request.GET.get('dateMin')
        dateMax = request.GET.get('dateMax')
        equipment = request.GET.get('equipment')
        #print(bookingName, supervisorName)

        if archiveValidQuery(bookingName):
            eventList = eventList.filter(bookingName__icontains=bookingName)

        if archiveValidQuery(supervisorName):
            eventList = eventList.filter(supervisorName__icontains=supervisorName)

        if archiveValidQuery(notes):
            eventList = eventList.filter(notes__icontains=notes)

        if archiveValidQuery(dateMin):
            eventList = eventList.filter(bookingDate__gte=dateMin)

        if archiveValidQuery(dateMax):
            eventList = eventList.filter(bookingDate__lte=dateMax)

        if archiveValidQuery(equipment) and equipment != 'Select...':
            eventList = eventList.filter(equipment__contains=equipment)


        totalHours = 0
        for x in eventList:
            totalHours += x.totalTime
        #print(totalHours)

        # Paginator
        paginator = Paginator(eventList, 10)
        pageNumber = request.GET.get('page')
        pageObj = paginator.get_page(pageNumber)

        context = {
            'eventList': eventList,
            'equipmentList': equipmentList,
            'totalHours': totalHours,
            'pageObj': pageObj,
        }

        return render(request, 'archive.html', context)
    
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")

def archiveValidQuery(param): # createBilling is using this aswell to sort through filters. Thanks!
    return param != '' and param is not None


# Create Billing functions
def generateInvoiceRef():
    # Generates a universal unique id (uuid)
    return str(uuid.uuid4())[:10]

@login_required
def createBilling(request):

    if request.user.is_superuser:
        eventList = Event.objects.all()
        equipmentList = Equipment.objects.all()
        equipment = Equipment.objects.all()

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
            equipmentList = Equipment.objects.all()

            supervisors = selectedEventObjects.values_list('supervisorName', flat=True).distinct()

            if supervisors.count() > 1:
                messages.error(request, "Can only create billings for one Supervisor at most.")
                return render(request, 'createBilling.html', context)

            billing = Billing()
            billing.invoiceRef = generateInvoiceRef()
            for event in selectedEventObjects:
                event.invoiceRef = billing.invoiceRef
                event.save()
            billing.supervisor = supervisors.first()
            billing.save()

            billing.events.set(selectedEventObjects)

            #print(selectedEventObjects)
            equipment_names = selectedEventObjects.values_list('equipment', flat=True).distinct()
            for e in equipmentList:
                print(e)
                if e.equipmentName == equipment_names:
                    print(e.equipmentID_auto+1)
                    billing.equipment.set(e.equipmentID_auto+1)
                    billing.save()

            cost = 0
            for event in selectedEventObjects:
                for eq in equipment:
                    if event.equipment == eq.equipmentName:
                        print("Here")
                        cost += event.totalTime * eq.hourlyRate
            billing.totalCost = cost
            print(cost)
            billing.save()

            return redirect('billings')

        return render(request, 'createBilling.html', context)
    
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")


# For deleting whole billings
@login_required
def deleteBilling(request, id):
    if request.user.is_superuser:
        billing = get_object_or_404(Billing, id=id)

        Event.objects.filter(invoiceRef=billing.invoiceRef).update(invoiceRef='None')

        billing.delete()

        return redirect('billings')
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")


# DOESN'T DELETE EVENT, just removes event from billing
@login_required
def deleteEvent(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            # Get a list of selected event IDs
            selectedEvent = request.POST.getlist('selected_events')

            if selectedEvent:
                for id in selectedEvent:
                    event = Event.objects.get(id=id)
                    billing = Billing.objects.filter(events=event).first()
                    billingInvoiceRef = event.invoiceRef
                    event.invoiceRef = 'None'
                    billing.events.remove(event)
                    billing.totalCost -= (float(event.totalTime) * float(event.hourlyRate))
                    event.save()
                    billing.save()


                    if not Event.objects.filter(invoiceRef=billingInvoiceRef).exists():
                        Billing.objects.filter(invoiceRef=billingInvoiceRef).delete()

        return redirect('billings')
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")
    
@login_required
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
    
@login_required
def generatePDF(request, id):

    if request.user.is_superuser:
        billing = get_object_or_404(Billing, id=id)
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setTitle(f"Invoice_{billing.invoiceRef}")

        # Info for client
        p.setFont("Helvetica", 8)
        y_position = 800
        p.drawString(50, y_position, "If you have any queries, feel free to get in touch.")
        y_position -= 10
        p.drawString(50, y_position, "University of Aberdeen, Institute of Medical Sciences, Foresthill, Aberdeen, AB25 2ZD")
        y_position -= 10
        p.drawString(50, y_position, "Gillian Milne, gillian.milne@abdn.ac.uk")

        # Head
        y_position -= 10
        p.line(50, y_position, 550, y_position)
        y_position -= 20
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y_position, "Microscopy and Histology Invoice")
        y_position -= 10
        p.line(50, y_position, 550, y_position)

        # Important Info
        p.setFont("Helvetica-Bold", 12)
        y_position -= 30
        p.drawString(50, y_position, "Supervisor: ")

        width = p.stringWidth("Supervisor: ", "Helvetica-Bold", 12)
        p.setFont("Helvetica", 12)
        p.drawString(50 + width, y_position, f"{billing.supervisor}")

        p.setFont("Helvetica-Bold", 12)
        y_position -= 20
        p.drawString(50, y_position, "Invoice Reference code: ")

        width = p.stringWidth("Invoice Reference code: ", "Helvetica-Bold", 12)
        p.setFont("Helvetica", 12)
        p.drawString(50 + width, y_position, f"{billing.invoiceRef}")

        p.setFont("Helvetica-Bold", 12)
        y_position -= 21
        p.drawString(50, y_position, "Total Cost: ")

        width = p.stringWidth("Total Cost: ", "Helvetica-Bold", 12)
        p.setFont("Helvetica", 12)
        p.drawString(50 + width, y_position, f"£{billing.totalCost:.2f}")

        p.setFont("Helvetica-Bold", 12)
        y_position -= 20
        p.drawString(50, y_position, "Issue Date: ")

        width = p.stringWidth("Issue Date: ", "Helvetica-Bold", 12)
        p.setFont("Helvetica", 12)
        p.drawString(50 + width, y_position, f"{billing.issueDate}")

        y_position -= 20
        p.line(50, y_position, 550, y_position)

        # Events listing
        y_position -= 20
        p.setFont("Helvetica-Bold", 13)
        p.drawString(50, y_position, "Events:")
        y_position -= 10
        p.setFont("Helvetica", 12)
        p.line(50, y_position, 550, y_position)
        y_position -= 20

        for event in billing.events.all():
            # Checks for space & creates new page
            if y_position <= 50:
                p.showPage()
                y_position = 800
                p.line(100, y_position, 550, y_position)
                y_position -= 20

            # name
            p.setFont("Helvetica-Bold", 10)
            p.drawString(100, y_position, "Booking Name: ")

            width = p.stringWidth("Booking Name: ", "Helvetica-Bold", 10)
            p.setFont("Helvetica", 10)
            p.drawString(100 + width, y_position, f"{event.bookingName}")

            # id
            p.setFont("Helvetica-Bold", 10)
            p.drawString(300, y_position, "Booking ID: ")

            width = p.stringWidth("Booking ID: ", "Helvetica-Bold", 10)
            p.setFont("Helvetica", 10)
            p.drawString(300 + width, y_position, f"{event.id}")

            # date
            p.setFont("Helvetica-Bold", 10)
            p.drawString(425, y_position, "Booking Date: ")

            width = p.stringWidth("Booking Date: ", "Helvetica-Bold", 10)
            p.setFont("Helvetica", 10)
            p.drawString(425 + width, y_position, f"{event.bookingDate}")

            # equipment
            y_position -= 8
            p.line(300, y_position, 550, y_position)
            y_position -= 15
            p.setFont("Helvetica-Bold", 10)
            p.drawString(300, y_position, "Hour(s)")
            p.drawString(400, y_position, "Rate/hr")
            p.drawString(500, y_position, "Cost")

            y_position -= 20
            p.drawString(100, y_position, f"{event.equipment}")

            p.setFont("Helvetica", 10)
            p.drawString(300, y_position, f"{event.totalTime}")
            p.drawString(400, y_position, f"{event.hourlyRate}")
            cost = event.hourlyRate * event.totalTime
            p.drawString(500, y_position, f"£{cost:.2f}")
            
            # end
            y_position -= 20
            p.line(100, y_position, 550, y_position)
            y_position -= 20
        
        p.setFont("Helvetica-Bold", 12)
        y_position -= 5
        p.drawString(350, y_position, "Invoice Total Cost: ")

        width = p.stringWidth("Invoice Total Cost: ", "Helvetica-Bold", 12)
        p.setFont("Helvetica", 12)
        p.drawString(350 + width, y_position, f"£{billing.totalCost:.2f}")
        y_position -= 15
        p.line(50, y_position, 550, y_position)
        
        # DOne
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"Invoice_{billing.invoiceRef}.pdf")
    else:
        messages.success(request, "Please log in before entering that page! Admin access only.")
        logout(request)
        return redirect("loginPage")

@login_required(login_url='/MCalendar/login/')
def add_supervisor(request): #function for adding new supervisors
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')

        #Input validation for all fields
        if not first_name or not last_name or not email or not telephone:
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

        #Ensures unique email
        if Supervisor.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Supervisor with this email already exists.'})
        
        #Add new supervisor to table
        supervisor = Supervisor(first_name=first_name, last_name=last_name, email=email, telephone=telephone)
        supervisor.save()

        #Response to let users know it was a success
        return JsonResponse({'status': 'success', 'message': 'Supervisor added successfully.'})   
        

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})    


def custom_404_view(request, exception):
    # Redirect to the login page
    return redirect('/MCalendar/login/')