# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-16 09:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0218_auto_20180116_1052'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entitycomponentyear',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='entitycontaineryear',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='examenrollment',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='groupelementyear',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='learningclassyear',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='learningcontainer',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='learningcontaineryear',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='learningunit',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='learningunitcomponent',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='learningunitcomponentclass',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='learningunitenrollment',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='learningunityear',
            old_name='deleted_new',
            new_name='deleted',
        ),
        migrations.RenameField(
            model_name='learningcomponentyear',
            old_name='deleted_new',
            new_name='deleted'
        ),
    ]
