# Generated by Django 4.1.1 on 2022-10-09 10:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_account_kana_average_json_array_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='kana_rating_right',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='numbers_rating_right',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='reg_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 9, 13, 25, 10, 427670)),
        ),
    ]