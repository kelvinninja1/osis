# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-11-07 09:52
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0383_organizationaddress_is_main'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='person',
            managers=[
                ('employees', django.db.models.manager.Manager()),
            ],
        ),
    ]
