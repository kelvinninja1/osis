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
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, get_object_or_404, render
from waffle.decorators import waffle_flag

from base.forms.learning_unit_proposal import CreationProposalBaseForm
from base.models.academic_year import AcademicYear, current_academic_year
from base.models.person import Person
from base.views.learning_units.common import show_success_proposal_learning_unit_year_creation_message


@waffle_flag('learning_unit_proposal_create')
@login_required
@permission_required('base.can_propose_learningunit', raise_exception=True)
def get_proposal_learning_unit_creation_form(request, academic_year):
    person = get_object_or_404(Person, user=request.user)

    proposal_form = CreationProposalBaseForm(request.POST or None,
                                             person,
                                             _get_academic_year(academic_year, person, request))

    if proposal_form.is_valid():
        proposal = proposal_form.save()
        show_success_proposal_learning_unit_year_creation_message(request, proposal.learning_unit_year)
        return redirect('learning_unit', learning_unit_year_id=proposal.learning_unit_year.pk)

    return render(request, "learning_unit/proposal/creation.html", proposal_form.get_context())


def _get_academic_year(academic_year, person, request):
    if person.is_faculty_manager and request.POST.get('academic_year'):
        return get_object_or_404(AcademicYear, pk=request.POST.get('academic_year'))
    return get_object_or_404(AcademicYear, pk=academic_year)
