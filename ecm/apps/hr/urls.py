# Copyright (c) 2010-2012 Robin Jarry
#
# This file is part of EVE Corporation Management.
#
# EVE Corporation Management is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# EVE Corporation Management is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# EVE Corporation Management. If not, see <http://www.gnu.org/licenses/>.

__date__ = "2011 10 23"
__author__ = "diabeteman"

from django.conf.urls.defaults import patterns

urlpatterns = patterns('ecm.apps.hr.views',
    (r'^$',                                     'dashboard.dashboard'),


    (r'^players/$',                             'players.player_list'),
    (r'^players/data/$',                        'players.player_list_data'),
    (r'^players/(\d+)/$',                       'players.player_details'),
    (r'^players/(\d+)/data/$',                  'players.player_details_data'),
)

urlpatterns += patterns('ecm.apps.hr.views.members',
    ###########################################################################
    # MEMBERS VIEWS
    (r'^members/$',                             'list.members'),
    (r'^members/data/$',                        'list.members_data'),
    (r'^members/history/$',                     'history.history'),
    (r'^members/history/data/$',                'history.history_data'),
    (r'^members/unassociated/$',                'list.unassociated'),
    (r'^members/unassociated/data/$',           'list.unassociated_data'),
    (r'^members/unassociated/clip/$',           'list.unassociated_clip'),
    (r'^members/accesschanges/$',               'access.access_changes'),
    (r'^members/accesschanges/data/$',          'access.access_changes_data'),
    (r'^members/(\d+)/$',                       'details.details'),
    (r'^members/(\d+)/accesschanges/data/$',    'details.access_changes_member_data'),
    (r'^members/(\d+)/updatenotes/$',           'details.update_member_notes'),
)

urlpatterns += patterns('ecm.apps.hr.views.titles',
    ###########################################################################
    # TITLES VIEWS
    (r'^titles/$',                              'list.titles'),
    (r'^titles/data/$',                         'list.titles_data'),
    (r'^titles/changes/$',                      'changes.changes'),
    (r'^titles/changes/data/$',                 'changes.changes_data'),
    (r'^titles/(\d+)/$',                        'details.details'),
    (r'^titles/(\d+)/composition/data/$',       'details.composition_data'),
    (r'^titles/(\d+)/compodiff/data/$',         'details.compo_diff_data'),
    (r'^titles/(\d+)/members/$',                'members.members'),
    (r'^titles/(\d+)/members/data/$',           'members.members_data'),
)

urlpatterns += patterns('ecm.apps.hr.views.roles',
    ###########################################################################
    # ROLES VIEWS
    (r'^roles/$',                               'list.roles'),
    (r'^roles/data/$',                          'list.roles_data'),
    (r'^roles/update/$',                        'list.update_access_level'),
    (r'^roles/(\d+)/$',                         'details.role'),
    (r'^roles/(\d+)/data/$',                    'details.role_data'),
)