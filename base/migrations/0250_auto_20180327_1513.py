# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-27 13:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0249_auto_20180327_1458'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='learningunityear',
            unique_together=set([('learning_unit', 'academic_year')]),
        ),
        migrations.AlterUniqueTogether(
            name='entitycomponentyear',
            unique_together=set([('entity_container_year', 'learning_component_year')]),
        ),
        migrations.AlterUniqueTogether(
            name='entitycontaineryear',
            unique_together=set([('entity', 'learning_container_year', 'type')]),
        ),
        migrations.AlterUniqueTogether(
            name='learningcontaineryear',
            unique_together=set([('learning_container', 'academic_year')]),
        ),
        migrations.RemoveField(
            model_name='examenrollment',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='groupelementyear',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='learningclassyear',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='learningcomponentyear',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='learningcontainer',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='learningunit',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='learningunitcomponent',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='learningunitcomponentclass',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='learningunitenrollment',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='entitycomponentyear',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='entitycontaineryear',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='learningcontaineryear',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='learningunityear',
            name='deleted',
        ),
    ]