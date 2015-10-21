from .models import Event, Attendee
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('url', 'id', 'trainer', 'location', 'scheduled_at')


class AttendeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendee
        fields = ('url', 'id', 'event', 'participant', 'survey_sent')
