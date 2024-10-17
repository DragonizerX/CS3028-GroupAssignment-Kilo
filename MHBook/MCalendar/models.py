from django.db import models
from django.contrib.auth.hashers import make_password, check_password
    
    
class Person(models.Model):
    first_name = models.CharField(max_length=15, unique=True, blank=True)
    last_name = models.CharField(max_length=15, unique=True, blank=True)
    email = models.EmailField(unique=True, blank=True)
    password = models.CharField(max_length=128, null=True)  # Initially allow null
    telephone = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = 'email'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    