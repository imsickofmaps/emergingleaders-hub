# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields.hstore
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.UUIDField(serialize=False, editable=False, primary_key=True, default=uuid.uuid4)),
                ('name', models.CharField(max_length=200)),
                ('msisdn', models.CharField(max_length=20)),
                ('email', models.EmailField(null=True, blank=True, max_length=254)),
                ('extras', django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
