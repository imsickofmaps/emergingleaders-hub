from django.contrib import admin

from .models import Trainer, Participant, Location


class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'msisdn', 'email', 'extras', 'created_at',
                    'updated_at')
    list_filter = ['name', 'msisdn', 'email', 'extras', 'created_at',
                   'updated_at']
    search_fields = ['name', 'msisdn', 'email']


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('msisdn', 'lang', 'full_name', 'gender', 'id_type',
                    'id_no', 'dob', 'passport_origin', 'created_at',
                    'updated_at')
    list_filter = ['msisdn', 'lang', 'full_name', 'gender', 'id_type',
                   'id_no', 'dob', 'passport_origin', 'created_at',
                   'updated_at']
    search_fields = ['msisdn', 'full_name']


class LocationAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'point', 'address', 'extras', 'created_at',
                    'updated_at')
    list_filter = ['venue_name', 'point', 'address', 'extras', 'created_at',
                   'updated_at']
    search_fields = ['venue_name', 'address']

admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Location, LocationAdmin)
