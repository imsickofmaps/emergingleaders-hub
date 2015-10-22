from django.contrib.auth.models import User, Group
from .models import Trainer, Participant, Location
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import (UserSerializer, GroupSerializer, TrainerSerializer,
                          ParticipantSerializer, LocationSerializer)


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


class TrainerViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows Trainers to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer


class ParticipantViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows Participants to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class ParticipantSearchList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ParticipantSerializer

    def get_queryset(self):
        """
        This view should return a list of all the participants
        for the supplied msisdn
        """
        msisdn = self.request.query_params.get("msisdn")
        participants = Participant.objects.filter(msisdn=msisdn)
        return participants


class LocationViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows Locations to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
