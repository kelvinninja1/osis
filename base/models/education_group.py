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
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _, ngettext
from reversion.admin import VersionAdmin

from base.business.education_groups import shorten
from base.models.enums import education_group_categories
from osis_common.models.serializable_model import SerializableModelAdmin, SerializableModel, SerializableModelManager


class EducationGroupAdmin(VersionAdmin, SerializableModelAdmin):
    list_display = ('most_recent_acronym', 'start_year', 'end_year', 'changed')
    search_fields = ('educationgroupyear__acronym', 'educationgroupyear__partial_acronym')

    actions = [
        'apply_education_group_year_postponement'
    ]

    def apply_education_group_year_postponement(self, request, queryset):
        # Potential circular imports
        from base.business.education_groups.automatic_postponement import EducationGroupAutomaticPostponement
        from base.views.common import display_success_messages, display_error_messages

        result, errors = EducationGroupAutomaticPostponement(queryset).postpone()
        count = len(result)
        display_success_messages(
            request, ngettext(
                "%(count)d education group has been postponed with success.",
                "%(count)d education groups have been postponed with success.", count
            ) % {'count': count}
        )
        if errors:
            display_error_messages(request, "{} : {}".format(
                _("The following education groups ended with error"),
                ", ".join([str(error) for error in errors])
            ))

    apply_education_group_year_postponement.short_description = _("Apply postponement on education group year")


class EducationGroupManager(SerializableModelManager):
    def having_related_training(self, **kwargs):
        # .distinct() is necessary if there is more than one training egy related to an education_group
        return self.filter(
            educationgroupyear__education_group_type__category=education_group_categories.TRAINING,
            **kwargs
        ).distinct()


class EducationGroup(SerializableModel):
    objects = EducationGroupManager()
    external_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    changed = models.DateTimeField(null=True, auto_now=True)

    start_year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Start')
    )

    end_year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('end')
    )

    @property
    def most_recent_acronym(self):
        most_recent_education_group = self.educationgroupyear_set.filter(education_group_id=self.id)\
                                                                 .latest('academic_year__year')
        return most_recent_education_group.acronym

    def __str__(self):
        return "{}".format(self.id)

    class Meta:
        permissions = (
            ("can_access_education_group", "Can access education_group"),
            ("change_commonpedagogyinformation", "Can change common pedagogy information"),
            ("change_pedagogyinformation", "Can change pedagogy information"),
        )

    def clean(self):
        # Check end_year should be greater of equals to start_year
        if self.start_year and self.end_year:
            if self.start_year > self.end_year:
                raise ValidationError({
                    'end_year': _("%(max)s must be greater or equals than %(min)s") % {
                        "max": _("end").title(),
                        "min": _("Start"),
                    }
                })
        # Check if end_year could be set according to protected data
        if self.end_year:
            shorten.check_education_group_end_date(self, self.end_year)
