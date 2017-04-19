# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('calarie', models.FloatField()),
                ('serving', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('fat', models.FloatField()),
                ('protein', models.FloatField()),
                ('carbohydrates', models.FloatField()),
                ('m1', models.IntegerField()),
                ('m2', models.IntegerField()),
                ('m3', models.IntegerField()),
                ('m4', models.IntegerField()),
                ('m5_loss', models.IntegerField()),
                ('m5_gain', models.IntegerField()),
                ('m5_stable', models.IntegerField()),
                ('fruit', models.IntegerField()),
                ('drink', models.IntegerField()),
                ('dairy', models.IntegerField()),
                ('snaks', models.IntegerField()),
                ('vegetable', models.IntegerField()),
                ('cereal_grains', models.IntegerField()),
                ('salad', models.IntegerField()),
                ('yogurt', models.IntegerField()),
                ('dessert', models.IntegerField()),
                ('pulses', models.IntegerField()),
                ('for_loss', models.IntegerField()),
                ('cuisine', models.CharField(max_length=255)),
                ('nuts', models.IntegerField()),
                ('squared_diff', models.FloatField(default=0)),
                ('squared_diff_weight_loss', models.FloatField(default=0)),
            ],
        ),
    ]
