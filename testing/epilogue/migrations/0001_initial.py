# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-21 18:05
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
                ('name', models.TextField()),
                ('quantity', models.IntegerField()),
                ('calarie', models.FloatField()),
                ('serving', models.TextField()),
                ('weight', models.FloatField()),
                ('fat', models.FloatField()),
                ('protein', models.FloatField()),
                ('carbohydrates', models.TextField()),
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
                ('cuisine', models.TextField()),
                ('nuts', models.IntegerField()),
            ],
            options={
                'db_table': 'business_diet_list',
            },
        ),
    ]
