from django.contrib import admin

from .models import Trainer, Participant, Location

admin.site.register(Trainer)
admin.site.register(Participant)
admin.site.register(Location)
