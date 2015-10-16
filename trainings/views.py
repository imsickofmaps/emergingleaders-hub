from django.contrib.auth.models import User, Group
from .models import Event
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (UserSerializer, GroupSerializer, EventSerializer)


class UserViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class EventViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows Events to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
