# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-30 08:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20180130_0739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='librarian',
            name='promotion_position',
        ),
        migrations.RemoveField(
            model_name='librarian',
            name='promotion_year',
        ),
        migrations.RemoveField(
            model_name='librarian',
            name='running_position',
        ),
    ]