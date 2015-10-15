import json

from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import Trainer, Location


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


class TestOperationsApi(AuthenticatedAPITestCase):

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

    # Trainer Api Testing
    def test_api_get_trainer(self):
        # Setup
        trainer_data = {
            "name": "Test User 1 Simple",
            "msisdn": "+27820010001"
        }
        trainer = Trainer.objects.create(**trainer_data)

        # Execute
        response = self.client.get(
            '/api/v1/trainers/%s/' % trainer.id,
            content_type='application/json')

        # Check
        self.assertEqual(response.data["name"], "Test User 1 Simple")

    def test_api_create_trainer_simple(self):
        # Setup
        post_data = {
            "name": "Test User 1 Simple",
            "msisdn": "+27820010001"
        }

        # Execute
        response = self.client.post('/api/v1/trainers/',
                                    json.dumps(post_data),
                                    content_type='application/json')

        # Check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        d = Trainer.objects.last()
        self.assertEqual(d.name, "Test User 1 Simple")
        self.assertEqual(d.msisdn, "+27820010001")
        self.assertEqual(d.email, None)
        self.assertEqual(d.extras, None)

    def test_api_create_trainer_detailed(self):
        # Setup
        post_data = {
            "name": "Test User 2 Detailed",
            "msisdn": "+27820020002",
            "email": "user2@operations.com",
            "extras": {
                "id": "1234561111222",
                "coffee": "black"
            }
        }

        # Execute
        response = self.client.post('/api/v1/trainers/',
                                    json.dumps(post_data),
                                    content_type='application/json')

        # Check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        d = Trainer.objects.last()
        self.assertEqual(d.name, "Test User 2 Detailed")
        self.assertEqual(d.msisdn, "+27820020002")
        self.assertEqual(d.email, "user2@operations.com")
        self.assertEqual(d.extras, {"id": "1234561111222", "coffee": "black"})

    # Location Api Testing
    def test_api_get_location(self):
        # Setup
        location_data = {
            "point": Point(18.0000000, -33.0000000)
        }
        location = Location.objects.create(**location_data)

        # Execute
        response = self.client.get(
            '/api/v1/locations/%s/' % location.id,
            content_type='application/json')

        # Check
        self.assertEqual(response.data["point"],
                         str(Point(18.0000000, -33.0000000, srid=4326)))
