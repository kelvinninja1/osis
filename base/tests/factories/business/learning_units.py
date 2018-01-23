##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2017 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from base.models.enums import entity_container_year_link_type
from base.tests.factories.entity_container_year import EntityContainerYearFactory
from base.tests.factories.learning_container_year import LearningContainerYearFactory
from base.tests.factories.learning_unit_year import LearningUnitYearFactory


def create_learning_unit_with_context(academic_year, structure, entity, acronym):
    learning_container_year = LearningContainerYearFactory(academic_year=academic_year, acronym=acronym)
    learning_unit_year = LearningUnitYearFactory(structure=structure,
                                                 acronym=acronym,
                                                 learning_container_year=learning_container_year,
                                                 academic_year=academic_year)

    EntityContainerYearFactory(type=entity_container_year_link_type.ALLOCATION_ENTITY,
                               learning_container_year=learning_container_year,
                               entity=entity)

    return learning_unit_year