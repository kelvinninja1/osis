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
from django import template
from base.utils.cache import cache

register = template.Library()

CACHE_NOTIFICATIONS_TIMEOUT = 1800 # seconds -> 30 min

@register.simple_tag(takes_context=True)
def get_notifications(context):
    user = context["request"].user

    cache_key = make_cache_key(user)
    notifications_cached = cache.get(cache_key, [])

    if notifications_cached:
        return notifications_cached

    notifications = [notification.verb for notification in user.notifications.unread()]

    cache.set(cache_key, notifications, CACHE_NOTIFICATIONS_TIMEOUT)

    return notifications


def make_cache_key(user):
    return "notifications_user_{}".format(user.pk)
