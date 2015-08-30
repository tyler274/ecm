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

__date__ = '2012 5 15'
__author__ = 'diabeteman'

import re

from django.core.exceptions import ValidationError
from django.conf import settings

if settings.EVEAPI_STUB_ENABLED:
    from ecm.utils import eveapi_stub as eveapi
else:
    import eveapi

from ecm.apps.common.models import Setting, APICall
from ecm.apps.corp.models import Corporation
import evelink


class Error(StandardError):
    def __init__(self, code, message):
        self.code = code
        self.args = (message.rstrip("."),)

    def __unicode__(self):
        return u'%s [code=%s]' % (self.args[0], self.code)


class RequestError(Error):
    pass


class AuthenticationError(Error):
    pass


class ServerError(Error):
    pass


# ------------------------------------------------------------------------------
EVE_API_VERSION = '2'
def check_version(version):
    if version != EVE_API_VERSION:
        raise DeprecationWarning("Wrong EVE API version. "
                "Expected '%s', got '%s'." % (EVE_API_VERSION, version))


# ------------------------------------------------------------------------------
def get_api():
    keyID = Setting.get(name='common_api_keyID')
    vCode = Setting.get(name='common_api_vCode')
    if not keyID or not vCode:
        raise Setting.DoesNotExist('the settings "common_api_keyID" or "common_api_vCode" are empty')
    else:
        return keyID, vCode


# ------------------------------------------------------------------------------
def get_charID():
    characterID = Setting.get(name='common_api_characterID')
    if not characterID:
        raise Setting.DoesNotExist('the setting "common_api_characterID" is empty')
    else:
        return characterID


# ------------------------------------------------------------------------------
def set_api(keyID, vCode, characterID):
    Setting.objects.filter(name='common_api_keyID').update(value=repr(keyID))
    Setting.objects.filter(name='common_api_vCode').update(value=repr(vCode))
    Setting.objects.filter(name='common_api_characterID').update(value=repr(characterID))


# ------------------------------------------------------------------------------
def connect(base_url=settings.BASE_API_URL):
    """
    Creates a connection to the web API with director credentials
    """
    keyID, vCode = get_api()
    conn = evelink.api.API(base_url, api_key=(keyID, vCode))
    return conn


# ------------------------------------------------------------------------------
def connect_user(user_api, base_url=settings.BASE_API_URL):
    """
    Creates a connection to the web API with a user's credentials
    """
    connection = evelink.api.API(base_url, api_key=(user_api.keyID, user_api.vCode))
    return connection


# ------------------------------------------------------------------------------
def required_access_mask(character=True):
    accessMask = 0
    key_type = character and APICall.CHARACTER or APICall.CORPORATION
    for call in APICall.objects.filter(type=key_type, required=True):
        accessMask |= call.mask
    return accessMask


# ------------------------------------------------------------------------------
def check_access_mask(accessMask, character):
    missing = []
    key_type = character and APICall.CHARACTER or APICall.CORPORATION
    for call in APICall.objects.filter(type=key_type, required=True):
        if not accessMask & call.mask:
            missing.append(call)
    if missing:
        raise AuthenticationError(0, "This API Key misses mandatory accesses: "
                                  + ', '.join([ call.name for call in missing ]))


# ------------------------------------------------------------------------------
def validate_director_api_key(keyID, vCode):
    try:
        connection = evelink.api.API(api_key=(keyID, vCode))
        # connection = eveapi.EVEAPIConnection().auth(keyID=keyID, vCode=vCode)
        # response = connection.account.APIKeyInfo()
        response = evelink.account.Account(api=connection).key_info()
        if response.result['type'].lower() != 'corp':
            raise ValidationError(
                "Wrong API Key type '%s'. Please provide a Corporation API Key." % response.result['type']
            )
        check_access_mask(response.result['access_mask'], character=False)
    except AuthenticationError, e:
        raise ValidationError(str(e))

    keyCharIDs = [ char['id'] for char in response.result['characters'] ]
    return keyCharIDs[0]


# ------------------------------------------------------------------------------
class Character:
    name = ""
    characterID = 0
    corporationID = 0
    corporationName = "No Corporation"
    is_corped = False

def get_account_characters(user_api):
    connection = connect_user(user_api)
    response = evelink.account.Account(api=connection).key_info()
    corp = Corporation.objects.mine()
    characters = []
    if response.result['type'].lower() != "account":
        raise AuthenticationError(0, "Wrong API Key type '" + response.result['type'] + "'. " +
                                         "Please provide an API Key working for all characters of your account.")

    check_access_mask(response.key.accessMask, character=True)

    for id, char in response.result['characters'].iteritems():
        c = Character()
        c.name = char['name']
        c.characterID = char['id']
        c.corporationID = char['corp']['id']
        c.corporationName = char['corp']['name']
        c.is_corped = (char['corp']['id'] == corp.corporationID)
        characters.append(c)
    return characters

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
