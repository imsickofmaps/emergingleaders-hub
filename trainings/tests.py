import json
import datetime

from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from operations.models import Trainer, Location
from .models import Event


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

    def test_login(self):
        # Setup

        # Execute
        request = self.client.post(
            '/api/v1/token-auth/',
            {"username": "testuser", "password": "testpass"})

        # Check
        token = request.data.get('token', None)
        self.assertIsNotNone(
            token, "Could not receive authentication token on login post.")
        self.assertEqual(request.status_code, 200,
                         "Status code on /auth/login was %s (should be 200)."
                         % request.status_code)

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
        # d = Trainer.objects.last()
        # self.assertEqual(d.name, "Test User 1 Simple")
        # self.assertEqual(d.msisdn, "+27820010001")
        # self.assertEqual(d.email, None)
        # self.assertEqual(d.extras, None)

    # def test_api_create_trainer_detailed(self):
    #     # Setup
    #     post_data = {
    #         "name": "Test User 2 Detailed",
    #         "msisdn": "+27820020002",
    #         "email": "user2@operations.com",
    #         "extras": {
    #             "id": "1234561111222",
    #             "coffee": "black"
    #         }
    #     }

    #     # Execute
    #     response = self.client.post('/api/v1/trainers/',
    #                                 json.dumps(post_data),
    #                                 content_type='application/json')

    #     # Check
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     d = Trainer.objects.last()
    #     self.assertEqual(d.name, "Test User 2 Detailed")
    #     self.assertEqual(d.msisdn, "+27820020002")
    #     self.assertEqual(d.email, "user2@operations.com")
    #     self.assertEqual(d.extras, {"id": "1234561111222", "coffee": "black"})
