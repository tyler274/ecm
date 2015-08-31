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

__date__ = "2010-02-08"
__author__ = "diabeteman"


import re
import logging
from datetime import datetime

from django.utils import timezone
from django.conf import settings
from django.db import transaction

from ecm.utils import cryptoECM
from ecm.apps.common.models import UpdateDate
from ecm.apps.corp.models import Corporation, Hangar, Wallet, CorpHangar, CorpWallet, Alliance
from ecm.apps.common import api

LOG = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
def update():
    """
    Fetch a /corp/CorporationSheet.xml.aspx api response, parse it and store it to
    the database.
    """
    LOG.info("fetching /corp/CorporationSheet.xml.aspx...")
    # connect to eve API
    api_conn = api.connect()
    # retrieve /corp/CorporationSheet.xml.aspx
    # corpApi = api_conn.corp.CorporationSheet(characterID=api.get_charID())
    corpApi = api.evelink.corp.Corp(api=api_conn).corporation_sheet().result
    # api.check_version(corpApi._meta.version)

    # currentTime = timezone.make_aware(corpApi._meta.currentTime, timezone.utc)
    currentTime = timezone.make_aware(datetime.utcnow(), timezone.utc)

    LOG.debug("parsing api response...")
    corp = update_corp_info(corpApi, currentTime)

    LOG.debug("name: %s [%s]", corp.corporationName, corp.ticker)
    if corp.alliance:
        LOG.debug("alliance: %s <%s>", corp.alliance.name, corp.alliance.shortName)
    else:
        LOG.debug("alliance: None")
    LOG.debug("CEO: %s", corp.ceoName)
    LOG.debug("tax rate: %d%%", corp.taxRate)
    LOG.debug("member limit: %d", corp.memberLimit)

    update_hangar_divisions(corpApi, currentTime)
    update_wallet_divisions(corpApi, currentTime)
    
    LOG.info("corp info updated")

# ------------------------------------------------------------------------------
@transaction.atomic()
def update_corp_info(corpApi, currentTime):
    try:
        try:
            try:
                alliance = Alliance.objects.get(allianceID=corpApi.get('alliance').get('id'))
            except Alliance.DoesNotExist:
                LOG.info("Adding new Alliance: "+ corpApi.get('alliance').get('name'))
                alliance = Alliance()
                alliance.allianceID = corpApi.get('alliance').get('id')
                alliance.name = corpApi.get('alliance').get('name')
                alliancesApi = api.evelink.EVE(api=api.connect()).alliances().result
                for key, a in alliancesApi.iteritems():
                    if a.get() == corpApi.get('alliance').get('id'):
                        alliance.shortName = a.get('ticker')
                        alliance.save()
                        break
        except api.Error:
            LOG.exception("Failed to fetch AllianceList.xml.aspx from EVE API server")
            corp = Corporation.objects.mine()
            alliance = None
    except:
        alliance = None

    description = fix_description(corpApi.get('description'))

    # reset all other corps
    Corporation.objects.exclude(corporationID=corpApi.get('id')).update(is_my_corp=False)

    try:
        # try to retrieve the db stored corp info
        corp = Corporation.objects.get(corporationID=corpApi.get('id'))
        corp.is_my_corp      = True
        corp.corporationID   = corpApi.get('id')
        corp.corporationName = corpApi.get('name')
        corp.ticker          = corpApi.get('ticker')
        corp.ceoID           = corpApi.get('ceo').get('id')
        corp.ceoName         = corpApi.get('ceo').get('name')
        corp.stationID       = corpApi.get('hq').get('id')
        corp.stationName     = corpApi.get('hq').get('name')
        corp.alliance        = alliance
        corp.description     = description
        corp.taxRate         = corpApi.get('tax_percent')
        corp.memberLimit     = corpApi.get('members').get('limit')
    except Corporation.DoesNotExist:
        LOG.debug('First scan, creating corp...')
        # no corp parsed yet
        corp = Corporation(is_my_corp      = True,
                           corporationID   = corpApi.get('id'),
                           corporationName = corpApi.get('name'),
                           ticker          = corpApi.get('ticker'),
                           ceoID           = corpApi.get('ceo').get('id'),
                           ceoName         = corpApi.get('ceo').get('name'),
                           stationID       = corpApi.get('hq').get('id'),
                           stationName     = corpApi.get('hq').get('name'),
                           description     = description,
                           alliance        = alliance,
                           taxRate         = corpApi.get('tax_percent'),
                           memberLimit     = corpApi.get('members').get('limit')
                           )
    
    if settings.USE_HTTPS:
        corp.ecm_url = 'https://' + settings.EXTERNAL_HOST_NAME
    else:
        corp.ecm_url = 'http://' + settings.EXTERNAL_HOST_NAME
    
    if not (corp.private_key and corp.public_key and corp.key_fingerprint):
        # as this is the first time, we must generate the RSA keypair of our own corp
        LOG.debug('Generating RSA key pair...')
        corp.private_key = cryptoECM.generate_rsa_keypair()
        corp.public_key = cryptoECM.extract_public_key(corp.private_key)
        corp.key_fingerprint = cryptoECM.key_fingerprint(corp.public_key)
        LOG.info('Generated RSA key pair for corporation ID %d.' % corpApi.get('id'))

    corp.save()
    # we store the update time of the table
    UpdateDate.mark_updated(model=Corporation, date=currentTime)

    return corp


# ------------------------------------------------------------------------------
@transaction.atomic()
def update_hangar_divisions(corpApi, currentTime):
    LOG.debug("HANGAR DIVISIONS:")
    my_corp = Corporation.objects.mine()
    corp_hangars = CorpHangar.objects.filter(corp=my_corp)
    for key, hangarDiv in corpApi.get('hangars').iteritems():
        corp_hangar_id = key
        corp_hangar_name = hangarDiv
        try:
            h = corp_hangars.get(hangar_id=corp_hangar_id)
            h.name = corp_hangar_name
        except CorpHangar.DoesNotExist:
            try:
                Hangar.objects.get(hangarID=corp_hangar_id)
            except Hangar.DoesNotExist:
                new_hangar = Hangar(hangarID=corp_hangar_id)
                new_hangar.save()

            h = CorpHangar(corp=my_corp, hangar_id=corp_hangar_id, name=corp_hangar_name)
        LOG.debug("  %s [%s]", h.name, h.hangar_id)
        h.save()
    # we store the update time of the table
    UpdateDate.mark_updated(model=Hangar, date=currentTime)


# ------------------------------------------------------------------------------
@transaction.atomic()
def update_wallet_divisions(corpApi, currentTime):
    LOG.debug("WALLET DIVISIONS:")
    my_corp = Corporation.objects.mine()
    wallets = CorpWallet.objects.filter(corp=my_corp)
    for key, walletDiv in corpApi.get('wallets').iteritems():
        corp_wallet_id = key
        corp_wallet_name = walletDiv
        try:
            w = wallets.get(wallet_id=corp_wallet_id)
            w.name = corp_wallet_name
        except CorpWallet.DoesNotExist:
            try:
                Wallet.objects.get(walletID=corp_wallet_id)
            except Wallet.DoesNotExist:
                new_wallet = Wallet(walletID=corp_wallet_id)
                new_wallet.save()

            w = CorpWallet(corp=my_corp, wallet_id=corp_wallet_id, name=corp_wallet_name)
        LOG.debug("  %s [%s]", w.name, w.wallet_id)
        w.save()
    # we store the update time of the table
    UpdateDate.mark_updated(model=Wallet, date=currentTime)

#------------------------------------------------------------------------------
FONT_TAG_REGEXP = re.compile('</?font.*?>', re.DOTALL)
SPAN_TAG_REGEXP = re.compile('</?span.*?>', re.DOTALL)
def fix_description(description):
    # an empty corp description string ('<description />' )will throw a TypeError
    # so let's catch it
    try:
        desc, _ = FONT_TAG_REGEXP.subn("", description)
        desc, _ = SPAN_TAG_REGEXP.subn("", desc)
        return desc.strip()
    except TypeError:
        return '-'

