# Generated by Django 2.0 on 2018-05-02 11:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epilogue', '0029_auto_20180409_0844'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerFoodItemsPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.IntegerField(db_index=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epilogue.Customer')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epilogue.Food')),
            ],
        ),
        migrations.AlterModelOptions(
            name='customerlevellog',
            options={'managed': False},
        ),
        migrations.AddField(
            model_name='logincustomer',
            name='email_confirm',
            field=models.CharField(default='0', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activitylevellog',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 2, 16, 55, 54, 993969)),
        ),
        migrations.AlterField(
            model_name='activitylevellog',
            name='week',
            field=models.IntegerField(default=18),
        ),
        migrations.AlterField(
            model_name='generateddietplanfooddetails',
            name='day',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterUniqueTogether(
            name='customerfooditemspreference',
            unique_together={('customer', 'food')},
        ),
        migrations.AlterIndexTogether(
            name='customerfooditemspreference',
            index_together={('customer', 'food')},
        ),
    ]
