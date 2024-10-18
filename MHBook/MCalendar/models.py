from django.db import models

class Bookings(models.Model):
    fullname = models.CharField(max_length=64)
    phone = models.IntegerField()
    email = models.EmailField()
    supervisor = models.CharField(max_length=64)
    organisation = models.CharField(max_length=128)
    date = models.DateField()
    start = models.TimeField()
    finish = models.TimeField()
    room = models.CharField(max_length=16)
    equipment = models.CharField(max_length=64)
    equipmentid = models.CharField(max_length=32)
