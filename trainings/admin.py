from django.contrib import admin

from .models import Event, Attendee, Feedback

admin.site.register(Event)
admin.site.register(Attendee)
admin.site.register(Feedback)
