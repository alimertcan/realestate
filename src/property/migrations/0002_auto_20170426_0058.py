# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-25 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='vote',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
