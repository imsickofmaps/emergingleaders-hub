from django.contrib.auth.models import User, Group
from .models import Trainer, Participant, Location
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class TrainerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trainer
        fields = ('url', 'id', 'name', 'msisdn', 'email', 'extras')


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Participant
        fields = ('url', 'id', 'msisdn', 'lang', 'full_name', 'gender',
                  'id_type', 'id_no', 'dob', 'passport_origin')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('url', 'id', 'point', 'venue_name', 'address', 'extras')
