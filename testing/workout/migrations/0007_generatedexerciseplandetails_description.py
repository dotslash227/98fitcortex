# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-06 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0006_auto_20171206_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatedexerciseplandetails',
            name='description',
            field=models.CharField(default='', max_length=225),
        ),
    ]