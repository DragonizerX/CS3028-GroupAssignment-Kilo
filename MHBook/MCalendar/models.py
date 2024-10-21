from django.db import models

# Create your models here.

class Event(models.Model):
    bookingName = models.CharField(max_length=80)
    supervisorName = models.CharField(max_length=80)
    bookingDate = models.DateField()
    startTime = models.TimeField()
    allotedTime = models.TimeField()
    comments = models.TextField(max_length = 1000)
    equipment = models.CharField(max_length=100, default='Not specified')