from django.contrib.postgres.fields import HStoreField
from django.contrib.gis.db import models


class Trainer(models.Model):

    """
    People who run training events
    """
    name = models.CharField(max_length=200)
    msisdn = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    extras = HStoreField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % self.name


class Participant(models.Model):

    """
    People who have participated in training events
    """
    LANG_CHOICES = (
        ('zu', 'isiZulu'),
        ('xh', 'isiXhosa'),
        ('af', 'Afrikaans'),
        ('en', 'English'),
        ('nso', 'Sesotho sa Leboa'),
        ('tn', 'Setswana'),
        ('st', 'Sesotho'),
        ('ts', 'Xitsonga'),
        ('ss', 'siSwati'),
        ('ve', 'Tshivenda'),
        ('nr', 'isiNdebele'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    ID_TYPE_CHOICES = (
        ('sa_id', 'SA ID'),
        ('passport', 'Passport'),
        ('none', 'None'),
    )
    msisdn = models.CharField(max_length=20)
    lang = models.CharField(max_length=3, null=True, blank=True,
                            choices=LANG_CHOICES)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=6, null=True, blank=True,
                              choices=GENDER_CHOICES)
    id_type = models.CharField(max_length=8, null=True, blank=True,
                               choices=ID_TYPE_CHOICES)
    id_no = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    passport_origin = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Participant %s" % self.msisdn


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
