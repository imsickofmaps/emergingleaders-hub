# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0003_auto_20151023_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='participant',
            field=models.ForeignKey(to='operations.Participant', related_name='attendees'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='participant',
            field=models.ForeignKey(to='operations.Participant', related_name='feedback'),
        ),
    ]
