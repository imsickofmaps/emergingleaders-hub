import uuid

from django.contrib.postgres.fields import HStoreField
from django.contrib.gis.db import models


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
        return "%s" % self.name


class Location(models.Model):

    """
    Training session point of location
    :param point point:
        GeoDjango point for x/y co-ordinates
    """
    point = models.PointField()
    venue_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    extras = HStoreField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # GeoDjango-specific overriding the default manager with a
    # GeoManager instance.
    objects = models.GeoManager()

    def __str__(self):
        return "%s" % (self.point)
