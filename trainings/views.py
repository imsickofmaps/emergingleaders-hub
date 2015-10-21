from .models import Event, Attendee
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (EventSerializer, AttendeeSerializer)


class EventViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows Events to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AttendeeViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows Attendees to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
