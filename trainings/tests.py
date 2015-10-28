import json
import datetime
import pytz
import responses

from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase
from django.db.models.signals import post_save
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from operations.models import Trainer, Location, Participant
from .models import Event, Attendee, Feedback, send_feedback_sms


class APITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()


class AuthenticatedAPITestCase(APITestCase):

    def _replace_post_save_hooks(self):
        has_listeners = lambda: post_save.has_listeners(Attendee)
        assert has_listeners(), (
            "Attendee model has no post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")
        post_save.disconnect(send_feedback_sms, sender=Attendee)
        assert not has_listeners(), (
            "Attendee model still has post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")

    def _restore_post_save_hooks(self):
        has_listeners = lambda: post_save.has_listeners(Attendee)
        assert not has_listeners(), (
            "Attendee model still has post_save listeners. Make sure"
            " helpers removed them properly in earlier tests.")
        post_save.connect(send_feedback_sms, sender=Attendee)

    def setUp(self):
        super(AuthenticatedAPITestCase, self).setUp()
        self._replace_post_save_hooks()
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(self.username,
                                             'testuser@example.com',
                                             self.password)
        token = Token.objects.create(user=self.user)
        self.token = token.key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def tearDown(self):
        self._restore_post_save_hooks()

    DEFAULT_TRAINER = {
        "name": "Test Trainer",
        "msisdn": "+27820010001"
    }

    def create_trainer(self, data=DEFAULT_TRAINER):
        trainer = Trainer.objects.create(**data)
        return trainer

    DEFAULT_LOCATION = {
        "point": Point(18.0000000, -33.0000000)
    }

    def create_location(self, data=DEFAULT_LOCATION):
        location = Location.objects.create(**data)
        return location

    def create_event(self, data={}):
        if data == {}:
            data = {
                "trainer": self.create_trainer(),
                "location": self.create_location(),
                "scheduled_at": "2015-11-01 11:00:00"
            }
        event = Event.objects.create(**data)
        return event

    DEFAULT_PARTICIPANT = {
        "msisdn": "+27820010001"
    }

    def create_participant(self, data=DEFAULT_PARTICIPANT):
        participant = Participant.objects.create(**data)
        return participant

    def create_attendee(self, data={}):
        if data == {}:
            data = {
                "event": self.create_event(),
                "participant": self.create_participant()
            }
        attendee = Attendee.objects.create(**data)
        return attendee

    def create_feedback(self, data={}):
        if data == {}:
            data = {
                "event": self.create_event(),
                "participant": self.create_participant(),
                "question_id": 1,
                "question_text": "Rate the venue",
                "answer_text": "Mediocre",
                "answer_value": "3"
            }
        feedback = Feedback.objects.create(**data)
        return feedback


class TestEventsApi(AuthenticatedAPITestCase):

    # Event Api Testing
    def test_api_get_event(self):
        # Setup
        event = self.create_event()
        # Execute
        response = self.client.get(
            '/api/v1/events/%s/' % event.id,
            content_type='application/json')
        # Check
        self.assertEqual(response.data["scheduled_at"], "2015-11-01T11:00:00Z")
        self.assertEqual(
            response.data["trainer"],
            "http://testserver/api/v1/trainers/%s/" % event.trainer.id)
        self.assertEqual(
            response.data["location"],
            "http://testserver/api/v1/locations/%s/" % event.location.id)

    def test_api_create_event(self):
        # Setup
        trainer = self.create_trainer()
        location = self.create_location()
        # prepare event data
        post_data = {
            "trainer": "/api/v1/trainers/%s/" % trainer.id,
            "location": "/api/v1/locations/%s/" % location.id,
            "scheduled_at": "2015-11-01T11:00:00Z"
        }
        # Execute
        response = self.client.post('/api/v1/events/',
                                    json.dumps(post_data),
                                    content_type='application/json')

        # Check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        d = Event.objects.last()
        self.assertEqual(d.scheduled_at, datetime.datetime(
            2015, 11, 1, 11, 0, tzinfo=pytz.utc))
        self.assertEqual(d.trainer.id, trainer.id)
        self.assertEqual(d.location.id, location.id)


class TestAttendeesApi(AuthenticatedAPITestCase):

    # Attendee Api Testing
    def test_api_get_attendee(self):
        # Setup
        attendee = self.create_attendee()
        # Execute
        response = self.client.get(
            '/api/v1/attendees/%s/' % attendee.id,
            content_type='application/json')
        # Check
        self.assertEqual(response.data["survey_sent"], False)
        self.assertEqual(
            response.data["event"],
            "http://testserver/api/v1/events/%s/" % attendee.event.id)
        self.assertEqual(
            response.data["participant"],
            "http://testserver/api/v1/participants/%s/" % (
                attendee.participant.id))

    @responses.activate
    def test_api_create_attendee(self):
        # Setup
        # restore post_save hook for this test
        post_save.connect(send_feedback_sms, sender=Attendee)
        event = self.create_event()
        participant = self.create_participant()
        # prepare event data
        post_data = {
            "event": "/api/v1/events/%s/" % event.id,
            "participant": "/api/v1/participants/%s/" % participant.id
        }
        # add response
        responses.add(responses.PUT,
                      "https://go.vumi.org/api/v1/go/http_api_nostream/conv-key/messages.json",  # flake8: noqa
                      body=json.dumps(post_data), status=201,
                      content_type='application/json')
        # Execute
        response = self.client.post('/api/v1/attendees/',
                                    json.dumps(post_data),
                                    content_type='application/json')
        # Check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        d = Attendee.objects.last()
        self.assertEqual(d.survey_sent, False)
        self.assertEqual(d.event.id, event.id)
        self.assertEqual(d.participant.id, participant.id)
        self.assertEqual(len(responses.calls), 1)
        # disconnect post_save hook again
        post_save.disconnect(send_feedback_sms, sender=Attendee)


class TestFeedbackApi(AuthenticatedAPITestCase):

    # Feedback Api Testing
    def test_api_get_feedback(self):
        # Setup
        feedback = self.create_feedback()

        # Execute
        response = self.client.get(
            '/api/v1/feedback/%s/' % feedback.id,
            content_type='application/json')
        # Check
        self.assertEqual(response.data["question_id"], 1)
        self.assertEqual(response.data["question_text"], "Rate the venue")
        self.assertEqual(response.data["answer_text"], "Mediocre")
        self.assertEqual(response.data["answer_value"], "3")
        self.assertEqual(
            response.data["event"],
            "http://testserver/api/v1/events/%s/" % feedback.event.id)
        self.assertEqual(
            response.data["participant"],
            "http://testserver/api/v1/participants/%s/" % (
                feedback.participant.id))

    def test_api_create_feedback(self):
        # Setup
        event = self.create_event()
        participant = self.create_participant()
        # prepare feedback data
        post_data = {
            "event": "/api/v1/events/%s/" % event.id,
            "participant": "/api/v1/participants/%s/" % participant.id,
            "question_id": 1,
            "question_text": "Rate the venue",
            "answer_text": "Mediocre",
            "answer_value": "3"
        }
        # Execute
        response = self.client.post('/api/v1/feedback/',
                                    json.dumps(post_data),
                                    content_type='application/json')
        # Check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        d = Feedback.objects.last()
        self.assertEqual(d.question_id, 1)
        self.assertEqual(d.question_text, "Rate the venue")
        self.assertEqual(d.answer_text, "Mediocre")
        self.assertEqual(d.answer_value, "3")
        self.assertEqual(d.event.id, event.id)
        self.assertEqual(d.participant.id, participant.id)
