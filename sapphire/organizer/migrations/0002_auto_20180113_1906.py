# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-14 00:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='address',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='city',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='location_name',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='state',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.CharField(default=datetime.datetime(2018, 1, 14, 0, 4, 57, 146969, tzinfo=utc), max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.CharField(default=datetime.datetime(2018, 1, 14, 0, 5, 32, 542283, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='location_name',
            field=models.CharField(default=datetime.datetime(2018, 1, 14, 0, 5, 47, 353709, tzinfo=utc), max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='state',
            field=models.CharField(default=datetime.datetime(2018, 1, 14, 0, 5, 55, 17759, tzinfo=utc), max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='zipcode',
            field=models.CharField(default=datetime.datetime(2018, 1, 14, 0, 6, 0, 740238, tzinfo=utc), max_length=5),
            preserve_default=False,
        ),
    ]
