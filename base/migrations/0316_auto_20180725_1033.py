# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-07-25 08:33
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('reference', '0017_language_changed'),
        ('base', '0315_auto_20180724_0823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='educationgroupyear',
            name='domains',
        ),
        migrations.AddField(
            model_name='educationgroupyear',
            name='main_domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='reference.Domain', verbose_name='main domain'),
        ),
        migrations.AddField(
            model_name='educationgroupyear',
            name='secondary_domains',
            field=models.ManyToManyField(related_name='education_group_years', through='base.EducationGroupYearDomain',
                                         to='reference.Domain'),
        ),
    ]
