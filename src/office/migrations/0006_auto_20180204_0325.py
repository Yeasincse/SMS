# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-03 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0005_gallaryimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallaryimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='school/gallary/'),
        ),
    ]
