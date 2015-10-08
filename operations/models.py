import uuid

from django.contrib.postgres.fields import HStoreField
from django.db import models


class Trainer(models.Model):

    """
    People who run training events
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    msisdn = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    extras = HStoreField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return "Trainer: %s; ID: %s" % (self.name, str(self.id))
