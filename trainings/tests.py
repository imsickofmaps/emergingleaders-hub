import json
import datetime
import pytz

from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from operations.models import Trainer, Location, Participant
from .models import Event, Attendee


class APITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()


class AuthenticatedAPITestCase(APITestCase):

    def setUp(self):
        super(AuthenticatedAPITestCase, self).setUp()
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(self.username,
                                             'testuser@example.com',
                                             self.password)
        token = Token.objects.create(user=self.user)
        self.token = token.key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)


class TestEventsApi(AuthenticatedAPITestCase):

    # Event Api Testing
    def test_api_get_event(self):
        # Setup
        # create a trainer
        trainer_data = {
            "name": "Test Trainer 1 Simple",
            "msisdn": "+27820010001"
        }
        trainer = Trainer.objects.create(**trainer_data)
        # create a location
        location_data = {
            "point": Point(18.0000000, -33.0000000)
        }
        location = Location.objects.create(**location_data)
        # create an event
        event_data = {
            "trainer": trainer,
            "location": location,
            "scheduled_at": "2015-11-01 11:00:00"
        }
        event = Event.objects.create(**event_data)

        # Execute
        response = self.client.get(
            '/api/v1/events/%s/' % event.id,
            content_type='application/json')

        # Check
        self.assertEqual(response.data["scheduled_at"], "2015-11-01T11:00:00Z")

    def test_api_create_event(self):
        # Setup
        # create a trainer
        trainer_data = {
            "name": "Test Trainer 1 Simple",
            "msisdn": "+27820010001"
        }
        trainer = Trainer.objects.create(**trainer_data)
        # create a location
        location_data = {
            "point": Point(18.0000000, -33.0000000)
        }
        location = Location.objects.create(**location_data)
        # prepare event data
        post_data = {
            "trainer": "/api/v1/trainers/%s/" % trainer.id,
            "location": "/api/v1/locations/%s/" % location.id,
            "scheduled_at": "2015-11-01T11:00:00Z"
        }
        print(post_data)
        # Execute
        response = self.client.post('/api/v1/events/',
                                    json.dumps(post_data),
                                    content_type='application/json')

        # Check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        d = Event.objects.last()
        self.assertEqual(d.scheduled_at, datetime.datetime(
            2015, 11, 1, 11, 0, tzinfo=pytz.utc))


class TestAttendeesApi(AuthenticatedAPITestCase):

    # Attendee Api Testing
    def test_api_get_attendee(self):
        # Setup
        # create a trainer
        trainer_data = {
            "name": "Test Trainer 1 Simple",
            "msisdn": "+27820010001"
        }
        trainer = Trainer.objects.create(**trainer_data)
        # create a location
        location_data = {
            "point": Point(18.0000000, -33.0000000)
        }
        location = Location.objects.create(**location_data)
        # create an event
        event_data = {
            "trainer": trainer,
            "location": location,
            "scheduled_at": "2015-11-01 11:00:00"
        }
        event = Event.objects.create(**event_data)
        # create a participant
        participant_data = {
            "msisdn": "+27820010001"
        }
        participant = Participant.objects.create(**participant_data)
        # create an attendee
        attendee_data = {
            "event": event,
            "participant": participant
        }
        attendee = Attendee.objects.create(**attendee_data)
        # Execute
        response = self.client.get(
            '/api/v1/attendees/%s/' % attendee.id,
            content_type='application/json')
        # Check
        self.assertEqual(response.data["survey_sent"], False)
