from django.contrib.gis.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from operations.models import Trainer, Location, Participant
from trainings.tasks import send_message


class Event(models.Model):

    """
    Training events
    """
    trainer = models.ForeignKey(Trainer,
                                related_name='events',
                                null=False)
    location = models.ForeignKey(Location,
                                 related_name='events',
                                 null=False)
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return "Training event by %s on %s" % (
            self.trainer, self.scheduled_at)


class Attendee(models.Model):

    """
    Participants at specific training events
    """
    event = models.ForeignKey(Event,
                              related_name='attendees',
                              null=False)
    participant = models.ForeignKey(Participant,
                                    related_name='attendees',
                                    null=False)
    survey_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return "Attendee %s for event %s" % (self.participant, self.event)


@receiver(post_save, sender=Attendee)
def send_feedback_sms(sender, instance, created, **kwargs):

    """
    Send an Sms to the Attendee prompting them to provide feedback.
    """
    if created:
        # Send message
        delay = 60 * settings.FEEDBACK_MESSAGE_DELAY
        send_message.apply_async(
            countdown=delay,
            kwargs={"to_addr": instance.participant.msisdn,
                    "message": settings.FEEDBACK_MESSAGE})


class Feedback(models.Model):

    """
    Feedback provided by training attendees
    """
    event = models.ForeignKey(Event,
                              related_name='feedback',
                              null=False)
    participant = models.ForeignKey(Participant,
                                    related_name='feedback',
                                    null=False)
    question_id = models.IntegerField()
    question_text = models.CharField(max_length=255)
    answer_text = models.CharField(max_length=255)
    answer_value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return "Feedback for question %s for event %s" % (
            self.question_id, self.event)
