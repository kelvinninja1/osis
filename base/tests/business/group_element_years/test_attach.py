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
from django.test import TestCase

from base.business.group_element_years.attach import AttachEducationGroupYearStrategy
from base.models.enums.education_group_types import TrainingType, GroupType, MiniTrainingType
from base.tests.factories.education_group_year import TrainingFactory, GroupFactory, MiniTrainingFactory
from base.tests.factories.group_element_year import GroupElementYearFactory


class TestAttachEducationGroupYearStrategy(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.master_120 = TrainingFactory(education_group_type__name=TrainingType.PGRM_MASTER_120.name)

        cls.option_in_parent = MiniTrainingFactory(education_group_type__name=MiniTrainingType.OPTION.name)
        GroupElementYearFactory(parent=cls.master_120, child_branch=cls.option_in_parent)

        # Create finality and attach some options
        cls.finality_group = GroupFactory(education_group_type__name=GroupType.FINALITY_120_LIST_CHOICE.name)
        GroupElementYearFactory(parent=cls.master_120, child_branch=cls.finality_group)

        cls.master_120_specialized = GroupFactory(education_group_type__name=TrainingType.MASTER_MS_120.name)
        GroupElementYearFactory(parent=cls.finality_group, child_branch=cls.master_120_specialized)

    def test_is_valid_case_attach_option_which_are_within_master_120(self):
        """
        In this test, we ensure that we can add an option at specialized finality because
        it is present in root master 2m level
        """
        strategy = AttachEducationGroupYearStrategy(
            parent=self.master_120_specialized,
            child=self.option_in_parent
        )
        self.assertTrue(strategy.is_valid())

    def test_is_valid_case_attach_groups_which_contains_options_which_are_within_master_120(self):
        """
        In this test, we ensure that we can add a groups which contains options at specialized finality because
        this options are present in root master 2m level
        """
        subgroup = GroupFactory(education_group_type__name=GroupType.SUB_GROUP.name)
        GroupElementYearFactory(parent=subgroup, child_branch=self.option_in_parent)

        strategy = AttachEducationGroupYearStrategy(
            parent=self.master_120_specialized,
            child=subgroup
        )
        self.assertTrue(strategy.is_valid())

    def test_is_not_valid_case_attach_option_which_are_not_within_master_120(self):
        """
        In this test, we ensure that we CANNOT add an option at specialized finality because
        it is not present in root master 2m level
        """
        option_which_are_not_in_2m = MiniTrainingFactory(education_group_type__name=MiniTrainingType.OPTION.name)
        strategy = AttachEducationGroupYearStrategy(
            parent=self.master_120_specialized,
            child=option_which_are_not_in_2m
        )

        with self.assertRaises(ValidationError):
            strategy.is_valid()

    def test_is_not_valid_case_attach_group_which_contains_option_which_are_not_within_master_120(self):
        """
        In this test, we ensure that we CANNOT add a groups which contains options at specialized finality because
        this options are not present in root master 2m level
        """
        subgroup = GroupFactory(education_group_type__name=GroupType.SUB_GROUP.name)
        option_which_are_not_in_2m = MiniTrainingFactory(education_group_type__name=MiniTrainingType.OPTION.name)
        # Error case
        GroupElementYearFactory(parent=subgroup, child_branch=option_which_are_not_in_2m)
        # Good case (present in 2M)
        GroupElementYearFactory(parent=subgroup, child_branch=self.option_in_parent)

        strategy = AttachEducationGroupYearStrategy(
            parent=self.master_120_specialized,
            child=subgroup
        )
        with self.assertRaises(ValidationError):
            strategy.is_valid()
