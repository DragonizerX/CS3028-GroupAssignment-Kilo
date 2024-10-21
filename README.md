# CS3028-GroupAssignment-Kilo
Group Kilo - Software Engineering Assignment: Microscopy and Histology Management System

# MINOR BUGS WITH MYBOOKINGS
# -- Date and Time fields update when nothing gets changed in edit bookings

# TEMPORARY MODEL CREATION ENTRY TUTORIAL
# -- py manage.py shell
# -- from MCalendar.models import Bookings -- (Or AccountRequest in this case)
# -- x = Bookings(fullname='John Doe', phone=123456, etc...) -- (Inside brackets put all variable names such as fullname, phone, supervisor)
# -- x.save()
# -- Bookings.objects.all().values() (To view all entries and their values)