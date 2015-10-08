import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import Trainer

USER_1_SIMPLE = {
    "name": "Test User 1 Simple",
    "msisdn": "+27820010001"
}
USER_2_DETAILED = {
    "name": "Test User 2 Detailed",
    "msisdn": "+27820020002",
    "email": "user2@operations.com",
    "extras": {
        "id": "1234561111222",
        "coffee": "black"
    }
}


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

    def _make_trainer(self, post_data=USER_1_SIMPLE):
        response = self.client.post('/operations/trainer/',
                                    json.dumps(post_data),
                                    content_type='application/json')
        return response


class TestExampleAppHStore(AuthenticatedAPITestCase):

    def test_login(self):
        request = self.client.post(
            '/operations/api-token-auth/',
            {"username": "testuser", "password": "testpass"})
        token = request.data.get('token', None)
        self.assertIsNotNone(
            token, "Could not receive authentication token on login post.")
        self.assertEqual(request.status_code, 200,
                         "Status code on /auth/login was %s (should be 200)."
                         % request.status_code)

    def test_create_trainer_simple(self):
        response = self._make_trainer()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        d = Trainer.objects.last()
        self.assertEqual(d.name, "Test User 1 Simple")
        self.assertEqual(d.msisdn, "+27820010001")
        self.assertEqual(d.email, None)
        self.assertEqual(d.extras, None)

    def test_create_trainer_detailed(self):
        response = self._make_trainer(post_data=USER_2_DETAILED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        d = Trainer.objects.last()
        self.assertEqual(d.name, "Test User 2 Detailed")
        self.assertEqual(d.msisdn, "+27820020002")
        self.assertEqual(d.email, "user2@operations.com")
        self.assertEqual(d.extras, {"id": "1234561111222", "coffee": "black"})
