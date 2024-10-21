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

    

