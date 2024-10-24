# CS3028-GroupAssignment-Kilo
Group Kilo - Software Engineering Assignment: Microscopy and Histology Management System

# TEMPORARY MODEL CREATION ENTRY TUTORIAL
# -- py manage.py shell
# -- from MCalendar.models import Bookings -- (Or AccountRequest in this case)
# -- x = Bookings(fullname='John Doe', phone=123456, etc...) -- (Inside brackets put all variable names such as fullname, phone, supervisor)
# -- x.full_clean() -- (Ensure to type this command as it make sures that you aren't inputing blank values)
# -- x.save()
# -- Bookings.objects.all().values() (To view all entries and their values)

# MANY2MANY FIELD KONRAD TUROIAL
# Do it all in shell and make sure to import models ^^^^ step 2 -- replace Bookings with * so it import everything
# first check booking id number by doing Billing.objects.all().values()
# for example if we want to add equipment:
# -- Billing(2).equipment.add(Equipment(1))
# 
# 2 - This is the id number that you have to check, replace this with any number as long as it exists
# equipment - if you check models this is what the field is called inside Billing()
# Equipment - again if you just check models this will be inside the equipment field.
# 1 - another id number once again check if it exists. at the moment i only created two equipments with id 1 and 2, create more if you want.
#
# If for example I would like to do supervisor instead of equipment, I would look into Billing() model:
# This is what I would look for: supervisor = models.ManyToManyField(Supervisor) -- So the command would be:
# -- Billing(ID).supervisor.add(Supervisor(ID)) -- where ID is whatever as long as it exists.
# If you want to figure out how to edit and delete look it up.