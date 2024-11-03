from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import UserManager, PermissionsMixin, AbstractBaseUser
from dateutil.relativedelta import relativedelta # type: ignore
from django.utils import timezone


class CustomUserManager(UserManager):
    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})
    
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    
    first_name = models.CharField(max_length=15, unique=True, blank=True)
    last_name = models.CharField(max_length=15, unique=True, blank=True)
    email = models.EmailField(unique=True, blank=True)
    password = models.CharField(max_length=128, null=True)  # Initially allow null
    telephone = models.CharField(max_length=11, blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Supervisor(models.Model):
    first_name = models.CharField(max_length=15, unique=True, blank=True)
    last_name = models.CharField(max_length=15, unique=True, blank=True)
    email = models.EmailField(unique=True, blank=True)
    password = models.CharField(max_length=128, null=True)  # Initially allow null
    telephone = models.CharField(max_length=15, blank=True)


class Event(models.Model):
    bookingName = models.CharField(max_length=80)
    supervisorName = models.CharField(max_length=80)
    email = models.EmailField()
    bookingDate = models.DateField()
    startTime = models.TimeField()
    finishTime = models.TimeField()
    #allotedTime = models.TimeField()
    comments = models.TextField(max_length = 1000)
    equipment = models.CharField(max_length=100, default='Not specified')
    totalTime = models.IntegerField(default=0)

    def __str__(self):
        return self.bookingName
    
    @property
    def calctotalTime(self):
        if isinstance(self.bookingDate, str):
            booking_date = datetime.strptime(self.bookingDate, '%Y-%m-%d').date()
        else:
            booking_date = self.bookingDate

        if isinstance(self.startTime, str):
            start_time = datetime.strptime(self.startTime, '%H:%M').time()
        else:
            start_time = self.startTime

        if isinstance(self.finishTime, str):
            finish_time = datetime.strptime(self.finishTime, '%H:%M').time()
        else:
            finish_time = self.finishTime

        startTime = datetime.combine(booking_date, start_time)
        finishTime = datetime.combine(booking_date, finish_time)  
    
        if finishTime < startTime:
            finishTime += timedelta(days=1)

        duration = finishTime - startTime
        return int(duration.total_seconds()//3600) 
    
    def save(self, *args, **kwargs):
        self.totalTime = self.calctotalTime
        super(Event,self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.bookingName} - {self.totalTime} hours"

    #@property
    #def totalTime(self):
    #    pass    


class Equipment(models.Model):
    equipmentID_auto = models.AutoField(primary_key=True)
    equipmentName = models.CharField(max_length=100)
    hourlyRate = models.FloatField(default=0.0)

    def __str__(self):
        return self.equipmentName
    
class Billing(models.Model): 
    invoiceRef = models.CharField(max_length=10, blank=False, null=False)
    supervisor = models.ManyToManyField(Supervisor) # includes first and last name, can be changed in billing.html
    user = models.ManyToManyField(Users) # includes first and last name, can be changed in billing.html
    events = models.ManyToManyField(Event) # includes booking reference no which for now is the booking id, and takes the start and finish time parameters to calculate the differnce in minutes to display time used
    issueDate = models.DateField(default=timezone.now)
    startDate = models.DateField(default=(timezone.now().date() - relativedelta(months=3))) # Default is 3 months difference but we need to be able to change this and finish date
    finishDate = models.DateField(default=timezone.now)
    equipment = models.ManyToManyField(Equipment) # includes the equipment id, name and its hourly rate
    totalCost = models.FloatField(default=0.0)
