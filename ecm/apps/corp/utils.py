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
# EVE Corporation Management. If not, see <>.

__author__ = 'Ajurna'
__date__ = "2013 8 08"

import logging

from ecm.apps.common import api
from ecm.apps.corp.models import Corporation, Alliance
from ecm.apps.corp.tasks.corp import fix_description

LOG = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
def get_corp(corporationID):
    """
     corporationID: int
     :Corporation Object
    """
    try:
        return Corporation.objects.get(corporationID=corporationID)
    except Corporation.DoesNotExist:
        # conn = api.eveapi.EVEAPIConnection()
        connection = api.evelink.api.API()
        # api_corp = conn.corp.CorporationSheet(corporationID=corporationID)
        api_corp = connection.corp.Corp(api=connection).corporation_sheet(corp_id=corporationID).result
        LOG.info("Adding new Corporation: " + str(api_corp['name']))

        corp = Corporation(corporationID   = api_corp['id'],
                           corporationName = str(api_corp['name']),
                           ticker          = api_corp['ticker'],
                           ceoID           = api_corp['ceo']['id'],
                           ceoName         = api_corp['ceo']['name'],
                           stationID       = api_corp['hq']['id'],
                           stationName     = api_corp['hq']['name'],
                           description     = fix_description(api_corp['description']),
                           taxRate         = api_corp['tax_percent'],
                           )
        if api_corp['alliance']['id']:
            corp.alliance = get_alliance(api_corp['alliance']['id'])
        corp.save()
        return corp


# ------------------------------------------------------------------------------
def get_alliance(allianceID):
    """
     allianceID: int
    : Alliance object pulled from alliance list if needed
    """
    try:
        alliance = Alliance.objects.get(allianceID=allianceID)
    except Alliance.DoesNotExist:
        # api_conn = api.eveapi.EVEAPIConnection()
        connection = api.evelink.api.API()
        alliancesApi = api.evelink.eve.EVE(api=connection).alliances().result
        alliance = Alliance()
        alliance.allianceID = allianceID
        for id, alliance in alliancesApi:
            if alliance['id'] == allianceID:
                alliance.shortName = alliance['ticker']
                alliance.name = alliance['name']
                LOG.info("Adding new Alliance: "+ alliance['name'])
                alliance.save()
                break
    return alliance


# ------------------------------------------------------------------------------
def get_corp_or_alliance(entityID):
    """
     entityID:
    : Corp object if possible, alliance object if not.
    """
    if Corporation.objects.filter(corporationID=entityID):
        return Corporation.objects.get(corporationID=entityID)
    if Alliance.objects.filter(allianceID=entityID):
        return Alliance.objects.get(allianceID=entityID)
    
    try:
        return get_corp(entityID)
    except RuntimeError:
        # This is because at time of coding the api is broken and the only
        # way to catch this is by catching the eveapi runtime error
        # TODO: fix when ccp get their shit together.
        return get_alliance(entityID)