from .models import Event, Attendee, Feedback
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('url', 'id', 'trainer', 'location', 'scheduled_at')


class AttendeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendee
        fields = ('url', 'id', 'event', 'participant', 'survey_sent')


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feedback
        fields = ('url', 'id', 'event', 'participant', 'question_id',
                  'question_text', 'answer_text', 'answer_value')
