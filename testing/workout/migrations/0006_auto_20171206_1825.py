# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-06 12:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0005_auto_20171206_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatedexerciseplandetails',
            name='exercise_level',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='generatedexerciseplandetails',
            name='muscle_group',
            field=models.CharField(default='', max_length=20),
        ),
    ]
