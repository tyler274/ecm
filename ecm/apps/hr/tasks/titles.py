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

__date__ = "2010-01-24"
__author__ = "diabeteman"

from django.contrib.auth.models import Group
from django.conf import settings
from django import db
from django.db import transaction
from django.utils import timezone
from django.utils.html import strip_tags
from django.db.models import Max

from ecm.apps.corp.models import Corporation
from ecm.apps.common.models import UpdateDate
from ecm.apps.hr.models import TitleComposition, Title, Role, TitleCompoDiff, RoleType
from ecm.apps.common import api

import logging
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
@transaction.atomic()
def update():
    """
    Retrieve all corp titles, their names and their role composition.
    If there are changes in the composition of the titles,
    the changes are also stored in the database.

    If there's an error, nothing is written in the database
    """
    logger.info("fetching /corp/Titles.xml.aspx...")
    # connect to eve API
    api_conn = api.connect()
    # retrieve /corp/Titles.xml.aspx
    # titlesApi = api_conn.corp.Titles(characterID=api.get_charID())
    titlesApi = api.evelink.corp.Corp(api=api_conn).titles().result

    # api.check_version(titlesApi._meta.version)
    # TODO: implement this for evelink

    currentTime = timezone.make_aware(titlesApi._meta.currentTime, timezone.utc)
    cachedUntil = timezone.make_aware(titlesApi._meta.cachedUntil, timezone.utc)
    logger.debug("current time : %s", str(currentTime))
    logger.debug("cached util : %s", str(cachedUntil))

    logger.debug("parsing api response...")
    
    my_corp = Corporation.objects.mine()
    
    newList = []
    # we get all the old TitleComposition from the database
    oldList = list(TitleComposition.objects.all())

    for id, title in titlesApi.iteritems():
        newList.extend(parse_one_title(title, my_corp))

    diffs = []
    if len(oldList) != 0 :
        diffs = getDiffs(newList, oldList, currentTime)
        if diffs :
            for d in diffs: d.save()
            # we store the update time of the table
            UpdateDate.mark_updated(model=TitleCompoDiff, date=currentTime)

            TitleComposition.objects.all().delete()
            for c in newList: c.save()
            # we store the update time of the table
            UpdateDate.mark_updated(model=TitleComposition, date=currentTime)
        # if no diff, we do nothing
    else:
        # 1st import
        for c in newList: c.save()
        # we store the update time of the table
        UpdateDate.mark_updated(model=TitleComposition, date=currentTime)

    # update titles access levels
    for t in Title.objects.all():
        t.accessLvl = t.get_access_lvl()
        t.save()

    logger.info("%d roles in titles parsed, %d changes since last scan", len(newList), len(diffs))

#------------------------------------------------------------------------------
def parse_one_title(titleApi, my_corp):
    '''
    Parse all the role for a given title

    @param titleApi: one IndexRowset instance from the eveapi module
    @return: a list of TitleComposition objects
    '''
    roleList = []

    titleID = title['id']

    name = unicode(titleApi['name'])
    if name.strip() == '':
        name = 'Title #%d' % titleID

    try:
        # retrieval of the title from the database
        title = my_corp.titles.get(titleID=titleID)
        if not title.titleName == name:
            # if the titleName has changed, we update it
            logger.info('Changing title name "%s" to "%s"...' % (title.titleName, name))
            title.titleName = name
            title.save()
    except Title.DoesNotExist:
        # the title doesn't exist yet, we create it
        logger.info('Title "%s" does not exist. Creating...' % name)
        title = Title.objects.create(corp=my_corp, titleID=titleID, titleName=strip_tags(name))
    try:
        # retrieval of the group corresponding to the title from de DB
        group = Group.objects.get(id=titleID)
        if not group.name == name:
            # if the titleName has changed, we update the group
            logger.info('Changing group name "%s" to "%s"...' % (group.name, name))
            group.name = name
            group.save()
    except Group.DoesNotExist:
        # the group doesn't exist yet, we create it
        logger.info('Group "%s" does not exist. Creating...' % name)
        Group.objects.create(id=titleID, name=name)
        
        # Bugfix for postgres. 
        # When inserting entries in a table which has a auto-incrementing serial,
        # if the id is forced manually, the serial is not automatically updated by the db
        # This leads to bug somewhere else in the application so we force the serial
        # to max_id + 1 here.
        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            maxid = Group.objects.all().aggregate(Max('id'))['id__max']
            
            cursor = db.connection.cursor()
            # reference: http://stackoverflow.com/questions/5342440/reset-auto-increment-counter-in-postgres
            cursor.execute('ALTER SEQUENCE auth_group_id_seq RESTART WITH %s;', [maxid + 1])

    '''
    Evelink does not follow the same naming pattern as eveapi, however the later names are enshrined in the db so
    we have to bridge
    '''
    role_type_conversion = {
        'roles' : ['global', ''],
        'rolesAtOther' : ['at_other', ''],
        'rolesAtBase' : ['at_base', ''],
        'rolesAtHQ': ['at_hq', ''],
        'grantableRoles' : ['can_grant', 'global'],
        'grantableRolesAtHQ' : ['can_grant', 'at_hq'],
        'grantableRolesAtBase' : ['can_grant', 'at_base'],
        'grantableRolesAtOther' : ['can_grant', 'at_other'],
    }
    for roleType in RoleType.objects.all():
        # for each role category, we extend the role composition list for the current title
        if not role_type_conversion[roleType.typeName][1]:
            roleList.extend(parseRoleType(title=title,
                                          roleType=roleType,
                                           # roles    = titleApi[roleType.typeName] ))
                                          roles=titleApi['roles'][role_type_conversion[roleType.typeName]]
                                          ))
        else:
            roleList.extend(parseRoleType(title=title,
                                          roleType=roleType,
                                           # roles    = titleApi[roleType.typeName] ))
                                          roles=titleApi['roles'][role_type_conversion[roleType.typeName][0]][role_type_conversion[roleType.typeName][1]]
                                          ))

    return roleList

#------------------------------------------------------------------------------
def parseRoleType(title, roleType, roles):
    '''
    Parse all the roles from a category for a given title

    @param title:    the current title
    @param roleType: the role category
    @param roles:    all the roles from that category for the given title
    @return: a list of TitleComposition objects
    '''

    subList = []

    for r in roles:
        r_id = r["roleID"]

        try:
            # we get the concerned role
            role = Role.objects.get(roleID=r_id, roleType=roleType.id)
        except Role.DoesNotExist:
            msg = 'roleID %s not found in category %s. Database corrupted or new role?'
            raise Role.DoesNotExist(msg % (r_id, roleType))

        # we create a new TitleComposition for the current title
        subList.append(TitleComposition(title=title, role=role))

    return subList

#------------------------------------------------------------------------------
def getDiffs(newList, oldList, date):
    removed  = [ r for r in oldList if r not in newList ]
    added    = [ a for a in newList if a not in oldList ]
    diffs    = []

    logger.debug("REMOVED ROLES TO TITLES:")
    if not removed : logger.debug("(none)")
    for oldcompo in removed:
        logger.debug("- %s", unicode(oldcompo))
        diffs.append(TitleCompoDiff(title = oldcompo.title,
                                    role  = oldcompo.role,
                                    new=False, date=date))
    logger.debug("ADDED ROLES TO TITLES:")
    if not removed : logger.debug("(none)")
    for newcompo in added:
        logger.debug("+ %s", unicode(newcompo))
        diffs.append(TitleCompoDiff(title = newcompo.title,
                                    role  = newcompo.role,
                                    new=True, date=date))

    return diffs

