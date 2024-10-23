from django.contrib import admin

# Register your models here.

from .models import Users, Supervisor, Event

admin.site.register(Users)
admin.site.register(Supervisor)
admin.site.register(Event)