##############################################################################
#
# OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2016 Université catholique de Louvain (http://www.uclouvain.be)
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
from django.db import models
from base.models import offer
import datetime


class OfferProposition(models.Model):
    acronym = models.CharField(max_length=200)
    offer = models.ForeignKey(offer.Offer)

    ####################
    # READERS PARAMETERS
    ####################

    # Do the students manage their readers ?
    # True = students can manage their readers
    # False = students cannot manage their readers, only the managers can
    student_can_manage_readers = models.BooleanField(default=True)

    # Can students always see readers ?
    # True = Yes
    # False = No, only when the date is ok
    readers_visibility_date_for_students = models.BooleanField(default=False)

    # Can advisers suggest readers when creating proposition_dissertation ?
    adviser_can_suggest_reader = models.BooleanField(default=False)

    ##################
    # STEPS PARAMETERS
    ##################
    # Is there a first year evaluation ?
    evaluation_first_year = models.BooleanField(default=False)

    # Is there a validation commission ?
    validation_commission_exists = models.BooleanField(default=False)

    #################
    # DATE PARAMETERS
    #################
    #   Start of visibility of proposition_dissertation
    month_start_visibility_proposition = models.IntegerField(default=9)
    day_of_month_start_visibility_proposition = models.IntegerField(default=1)

    #   End of visibility of proposition_dissertation
    month_end_visibility_proposition = models.IntegerField(default=8)
    day_of_month_end_visibility_proposition = models.IntegerField(default=31)

    #   Start of opening dissertation
    month_start_visibility_dissertation = models.IntegerField(default=9)
    day_of_month_start_visibility_dissertation = models.IntegerField(default=1)

    #   End of oppening dissertation
    month_end_visibility_dissertation = models.IntegerField(default=8)
    day_of_month_end_visibility_dissertation = models.IntegerField(default=31)

    @property
    def in_periode_visibility_proposition(self):
        c = datetime.date.today()
        a = datetime.date(c.year, self.month_start_visibility_proposition,
                          self.day_of_month_start_visibility_proposition)
        b = datetime.date(c.year, self.month_end_visibility_proposition, self.day_of_month_end_visibility_proposition)
        if a > b:
            if c >= a or c <= b:
                return True
            else:
                return False
        if a <= b:
            if c >= a and c <= b:
                return True
            else:
                return False

    @property
    def in_periode_visibility_dissertation(self):
        c = datetime.date.today()
        a = datetime.date(c.year, self.month_start_visibility_dissertation,
                          self.day_of_month_start_visibility_dissertation)
        b = datetime.date(c.year, self.month_end_visibility_dissertation, self.day_of_month_end_visibility_dissertation)
        if a > b:
            if c >= a or c <= b:
                return True
            else:
                return False
        if a <= b:
            if c >= a and c <= bl:
                return True
            else:
                return False

    def __str__(self):
        return self.acronym


def __day_month_check(day, month):
    if (month == 1) or (month == 3) or (month == 5) or (month == 7) or (month == 8) or (month == 10) or (month == 12):
        if day < 0 or day > 31:

            print('day start visibility proposition is not correct ')
        else:
            return True
    elif (month == 4) or (month == 6) or (month == 9) or (month == 11):
        if day < 0 or day > 30:

            print('day start visibility proposition is not correct ')
        else:
            return True
    elif month == 2:
        if day < 0 or day > 28:

            print('day start visibility proposition is not correct ')
        else:
            return True
