# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-28 12:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('epilogue', '0007_auto_20170812_0930'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerGoogleClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visited', models.DateTimeField(auto_now_add=True)),
                ('clientId', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gaclientids', to='epilogue.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(db_index=True)),
                ('clientId', models.CharField(max_length=255)),
                ('visited', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='customergoogleclient',
            index=models.Index(fields=['customer'], name='analytics_c_custome_d753dc_idx'),
        ),
        migrations.AddIndex(
            model_name='customergoogleclient',
            index=models.Index(fields=['clientId'], name='analytics_c_clientI_549452_idx'),
        ),
        migrations.AddIndex(
            model_name='customergoogleclient',
            index=models.Index(fields=['customer', 'clientId'], name='analytics_c_custome_3273bc_idx'),
        ),
    ]
