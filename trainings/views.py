from .models import Event
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (EventSerializer)


class EventViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows Events to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
