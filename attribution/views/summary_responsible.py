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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from attribution import models as mdl_attr
from attribution.business.attribution import get_attributions_list, _set_summary_responsible_to_true
from attribution.business.entity_manager import _append_entity_version
from base import models as mdl_base
from base.models.entity_manager import is_entity_manager, find_entities_with_descendants_from_entity_managers
from base.views import layout


@login_required
@user_passes_test(is_entity_manager)
def search(request):
    entities_manager = mdl_base.entity_manager.find_by_user(request.user)
    academic_year = mdl_base.academic_year.current_academic_year()
    _append_entity_version(entities_manager, academic_year)
    if request.GET:
        entities_with_descendants = find_entities_with_descendants_from_entity_managers(entities_manager)
        attributions = list(mdl_attr.attribution.search_summary_responsible(
            learning_unit_title=request.GET.get('learning_unit_title'),
            course_code=request.GET.get('course_code'),
            entities=entities_with_descendants,
            tutor=request.GET.get('tutor'),
            responsible=request.GET.get('summary_responsible')
        ))
        dict_attribution = get_attributions_list(attributions, "-summary_responsible")
        return layout.render(request, 'summary_responsible.html',
                             {"entities_manager": entities_manager,
                              "academic_year": academic_year,
                              "dict_attribution": dict_attribution,
                              "learning_unit_title": request.GET.get('learning_unit_title'),
                              "course_code": request.GET.get('course_code'),
                              "tutor": request.GET.get('tutor'),
                              "summary_responsible": request.GET.get('summary_responsible'),
                              "init": "1"})
    else:
        return layout.render(request, 'summary_responsible.html',
                             {"entities_manager": entities_manager,
                              "academic_year": academic_year,
                              "init": "0"})


@login_required
@user_passes_test(is_entity_manager)
def edit(request):
    entities_manager = mdl_base.entity_manager.find_by_user(request.user)
    entities_with_descendants = find_entities_with_descendants_from_entity_managers(entities_manager)
    learning_unit_year_id = request.GET.get('learning_unit_year').strip('learning_unit_year_')
    a_learning_unit_year = mdl_base.learning_unit_year.get_by_id(learning_unit_year_id)
    if a_learning_unit_year.allocation_entity in entities_with_descendants:
        attributions = mdl_attr.attribution.find_all_responsible_by_learning_unit_year(a_learning_unit_year)
        academic_year = mdl_base.academic_year.current_academic_year()
        return layout.render(request, 'summary_responsible_edit.html',
                             {'learning_unit_year': a_learning_unit_year,
                              'attributions': attributions,
                              "academic_year": academic_year,
                              'course_code': request.GET.get('course_code'),
                              'learning_unit_title': request.GET.get('learning_unit_title'),
                              'tutor': request.GET.get('tutor'),
                              'summary_responsible': request.GET.get('summary_responsible')})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


@login_required
@user_passes_test(is_entity_manager)
def update(request, pk):
    if request.POST.get('action') == "add":
        mdl_attr.attribution.clear_summary_responsible_by_learning_unit_year(pk)
        if request.POST.get('attribution'):
            attribution_id = request.POST.get('attribution').strip('attribution_')
            attribution = mdl_attr.attribution.find_by_id(attribution_id)
            attributions = mdl_attr.attribution.search(tutor=attribution.tutor,
                                                       learning_unit_year=attribution.learning_unit_year)
            _set_summary_responsible_to_true(attributions)
    url = reverse('summary_responsible')
    return HttpResponseRedirect(url + "?course_code=%s&learning_unit_title=%s&tutor=%s&scores_responsible=%s"
                                % (request.POST.get('course_code'),
                                   request.POST.get('learning_unit_title'),
                                   request.POST.get('tutor'),
                                   request.POST.get('summary_responsible')))
