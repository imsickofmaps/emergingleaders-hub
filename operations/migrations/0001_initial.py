# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('venue_name', models.CharField(blank=True, null=True, max_length=200)),
                ('address', models.CharField(blank=True, null=True, max_length=255)),
                ('extras', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('msisdn', models.CharField(max_length=20)),
                ('lang', models.CharField(blank=True, null=True, max_length=3, choices=[('zu', 'isiZulu'), ('xh', 'isiXhosa'), ('af', 'Afrikaans'), ('en', 'English'), ('nso', 'Sesotho sa Leboa'), ('tn', 'Setswana'), ('st', 'Sesotho'), ('ts', 'Xitsonga'), ('ss', 'siSwati'), ('ve', 'Tshivenda'), ('nr', 'isiNdebele')])),
                ('full_name', models.CharField(blank=True, null=True, max_length=200)),
                ('gender', models.CharField(blank=True, null=True, max_length=6, choices=[('male', 'Male'), ('female', 'Female')])),
                ('id_type', models.CharField(blank=True, null=True, max_length=8, choices=[('sa_id', 'SA ID'), ('passport', 'Passport'), ('none', 'None')])),
                ('id_no', models.CharField(blank=True, null=True, max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('passport_origin', models.CharField(blank=True, null=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('msisdn', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, null=True, max_length=254)),
                ('extras', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
