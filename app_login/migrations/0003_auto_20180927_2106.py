# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-27 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_login', '0002_auto_20180926_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]