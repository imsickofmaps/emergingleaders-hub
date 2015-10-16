# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
import uuid
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('venue_name', models.CharField(null=True, blank=True, max_length=200)),
                ('address', models.CharField(null=True, blank=True, max_length=255)),
                ('extras', django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True, editable=False)),
                ('name', models.CharField(max_length=200)),
                ('msisdn', models.CharField(max_length=20)),
                ('email', models.EmailField(null=True, blank=True, max_length=254)),
                ('extras', django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
