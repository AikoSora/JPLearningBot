# Generated by Django 4.1.1 on 2022-10-06 08:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_account_kana_test_count_account_kana_test_right_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='reg_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 11, 27, 55, 164611)),
        ),
    ]
