# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-08-21 09:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0333_auto_20180820_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupelementyear',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='base.EducationGroupYear'),
        ),
    ]