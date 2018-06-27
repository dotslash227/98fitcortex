# Generated by Django 2.0 on 2018-06-23 07:36

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('epilogue', '0035_auto_20180607_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerIsoWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('year', models.IntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epilogue.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='DietFavouriteFoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'item'), (1, 'meal'), (2, 'day')])),
                ('meal', models.IntegerField(choices=[(1, 'Breakfast'), (2, 'Mid Day Snack'), (3, 'Lunch'), (4, 'Evening Snack'), (5, 'Dinner')])),
                ('preference', models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike'), (0, 'Neutral')], default=0)),
                ('customer_calendar', models.ForeignKey(default=0, on_delete=django.db.models.fields.related.ForeignKey, related_name='favourites', to='epilogue.CustomerIsoWeek')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epilogue.Food')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='dietfavouritefoods',
            unique_together={('customer_calendar', 'type', 'meal', 'preference', 'food')},
        ),
        migrations.AddIndex(
            model_name='customerisoweek',
            index=models.Index(fields=['customer', '-week', '-year'], name='epilogue_cu_custome_1d8b99_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='customerisoweek',
            unique_together={('customer', 'week', 'year')},
        ),
    ]