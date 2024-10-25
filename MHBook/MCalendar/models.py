from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import UserManager, PermissionsMixin, AbstractBaseUser


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

""" --- Redundant, delete later
class AccountRequest(models.Model):
    fullname = models.CharField(max_length=64, blank=False, null=False)
    phone = models.IntegerField(blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    supervisor = models.CharField(max_length=64, default='N/A')
    organisation = models.CharField(max_length=128, blank=False, null=False)
    isAccepted = models.BooleanField(default=False)
"""

class Event(models.Model):
    bookingName = models.CharField(max_length=80)
    supervisorName = models.CharField(max_length=80)
    bookingDate = models.DateField()
    startTime = models.TimeField()
    allotedTime = models.TimeField()
    comments = models.TextField(max_length = 1000)
    equipment = models.CharField(max_length=100, default='Not specified')


class Equipment(models.Model):
    equipmentID_auto = models.AutoField(primary_key=True)
    equipmentName = models.CharField(max_length=100)
    hourlyRate = models.FloatField(default=0.0)