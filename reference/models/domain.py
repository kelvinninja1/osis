##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2018 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.core import serializers
from django.db import models

from osis_common.models.serializable_model import SerializableModel, SerializableModelAdmin
from reference.models.enums import domain_type


class DomainAdmin(SerializableModelAdmin):
    list_display = ('code', 'name', 'parent', 'decree', 'type', )
    fieldsets = ((None, {'fields': ('code', 'name', 'parent', 'decree', 'type')}),)
    list_filter = ('type', 'national', 'adhoc')
    search_fields = ['code', 'name']


class Domain(SerializableModel):
    external_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    changed = models.DateTimeField(null=True, auto_now=True)

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True)
    decree = models.ForeignKey('Decree', null=True, blank=True)
    type = models.CharField(max_length=50, choices=domain_type.TYPES, default=domain_type.UNKNOWN)
    adhoc = models.BooleanField(default=True) # If False == Official/validated, if True == Not Official/not validated
    national = models.BooleanField(default=False) # True if is Belgian else False

    def __str__(self):
        full_domain_name = ""
        if self.decree:
            full_domain_name += "{}: ".format(self.decree.name)
        if self.code:
            full_domain_name += "{} ".format(self.code)
        full_domain_name += "{}".format(self.name)
        return full_domain_name

    class Meta:
        ordering = ('-decree__name', 'code', 'name')


def find_all_for_sync():
    """
    :return: All records in the 'Domain' model (table). Used to synchronize date from Osis to Osis-portal.
    """
    print("Retrieving data from " + str(Domain) + "...")
    # Necessary fields for Osis-portal
    fields = ['id', 'external_id', 'name', 'parent_id']
    # list() to force the evaluation of the queryset
    return list(Domain.objects.values(*fields).order_by('name'))


def serialize_list(list_domains):
    """
    Serialize a list of "Domain" objects using the json format.
    Use to send data to osis-portal.
    :param list_domains: a list of "Domain" objects
    :return: the serialized list (a json)
    """
    fields = ('id', 'external_id', 'name', 'parent')
    return serializers.serialize("json", list_domains, fields=fields)
