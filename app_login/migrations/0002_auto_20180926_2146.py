# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-26 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('mal', '男'), ('female', '女')], default='男', max_length=4),
        ),
    ]
