from django.contrib import admin

from .models import Event, Attendee, Feedback


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'trainer', 'location', 'scheduled_at', 'created_at',
                    'updated_at')
    list_filter = ['id', 'trainer', 'location', 'scheduled_at', 'created_at',
                   'updated_at']


class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event', 'survey_sent', 'created_at',
                    'updated_at')
    list_filter = ['participant', 'event', 'survey_sent', 'created_at',
                   'updated_at']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('event', 'participant', 'question_id', 'question_text',
                    'answer_text', 'answer_value', 'created_at',
                    'updated_at')
    list_filter = ['event', 'participant', 'question_id', 'question_text',
                   'answer_text', 'answer_value', 'created_at',
                   'updated_at']
    search_fields = ['question_text', 'answer_text', 'answer_value']

admin.site.register(Event, EventAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Feedback, FeedbackAdmin)
