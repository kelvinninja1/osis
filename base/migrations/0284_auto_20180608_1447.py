# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-08 12:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0283_learningunityear_existing_proposal_in_epc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learningcomponentyear',
            name='title',
        ),
        migrations.RemoveField(
            model_name='learningunitcomponent',
            name='duration',
        ),
    ]
