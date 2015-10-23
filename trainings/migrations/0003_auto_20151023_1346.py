# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
        ('trainings', '0002_attendee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('question_id', models.IntegerField()),
                ('question_text', models.CharField(max_length=255)),
                ('answer_text', models.CharField(max_length=255)),
                ('answer_value', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(to='trainings.Event', related_name='feedback')),
                ('participant', models.OneToOneField(related_name='feedback', to='operations.Participant')),
            ],
        ),
        migrations.AlterField(
            model_name='attendee',
            name='participant',
            field=models.OneToOneField(related_name='attendees', to='operations.Participant'),
        ),
    ]
