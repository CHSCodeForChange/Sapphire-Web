# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-15 20:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0007_slot_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slots',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utility.Slot'),
        ),
    ]
