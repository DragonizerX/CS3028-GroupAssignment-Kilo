from django.db import models

class Bookings(models.Model):
    fullname = models.CharField(max_length=64, blank=False, null=False)
    phone = models.IntegerField(blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    supervisor = models.CharField(max_length=64, default='N/A')
    organisation = models.CharField(max_length=128, default='N/A')
    date = models.DateField(blank=False, null=False)
    start = models.TimeField(blank=False, null=False)
    finish = models.TimeField(blank=False, null=False)
    room = models.CharField(max_length=16, blank=False, null=False)
    equipment = models.CharField(max_length=64, blank=False, null=False)
    equipmentid = models.CharField(max_length=32, default='N/A')

class AccountRequest(models.Model):
    fullname = models.CharField(max_length=64, blank=False, null=False)
    phone = models.IntegerField(blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    supervisor = models.CharField(max_length=64, default='N/A')
    organisation = models.CharField(max_length=128, blank=False, null=False)
    isAccepted = models.BooleanField(default=False)
