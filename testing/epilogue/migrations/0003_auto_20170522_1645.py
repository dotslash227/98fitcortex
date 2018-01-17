# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('epilogue', '0002_auto_20170421_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('business_owner_first_name', models.CharField(max_length=25)),
                ('business_owner_last_name', models.CharField(max_length=25)),
                ('mobile_number', models.CharField(max_length=11)),
                ('created_on', models.DateTimeField()),
                ('signup_completed', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'business_account',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('mobile', models.CharField(max_length=11)),
                ('age', models.IntegerField()),
                ('w', models.CharField(db_column='weight', max_length=11)),
                ('h', models.CharField(db_column='height', max_length=20)),
                ('ls', models.CharField(db_column='lifestyle', max_length=50)),
                ('gen', models.CharField(db_column='gender', max_length=20)),
            ],
            options={
                'db_table': 'erp_customer',
            },
        ),
        migrations.CreateModel(
            name='GeneratedDietPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user_week_id', models.IntegerField(default=1)),
                ('week_id', models.IntegerField(default=1)),
                ('company_id', models.IntegerField(default=0)),
                ('plan_type', models.CharField(default='system generated plan', max_length=50)),
                ('medi_applicable', models.CharField(default='', max_length=20)),
            ],
            options={
                'db_table': 'erp_diet_plan',
            },
        ),
        migrations.CreateModel(
            name='GeneratedDietPlanFoodDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=100)),
                ('meal_type', models.CharField(max_length=20)),
                ('day', models.IntegerField()),
                ('calorie', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'erp_diet_plan_food_details',
            },
            managers=[
                ('day1', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='GeneratedExercisePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=None)),
            ],
            options={
                'db_table': 'erp_exercise_plan',
            },
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'glo_objective',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to='epilogue.Customer', verbose_name='Customer')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
            },
        ),
    ]
