from django.contrib import admin

# Register your models here.

from .models import Users, Supervisor, Event,Equipment

admin.site.register(Users)
admin.site.register(Supervisor)
admin.site.register(Event)
admin.site.register(Equipment)