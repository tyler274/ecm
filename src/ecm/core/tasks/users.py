# The MIT License - EVE Corporation Management
# 
# Copyright (c) 2010 Robin Jarry
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from django.template.context import RequestContext
from django.http import HttpRequest

__date__ = "2011 4 18"
__author__ = "diabeteman"

import logging

from django.db import transaction
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives

from ecm.core import api
from ecm.lib import eveapi
from ecm.data.common.models import RegistrationProfile, UserAPIKey
from ecm.data.roles.models import CharacterOwnership, Title, Member

logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------
@transaction.commit_on_success
def update_all_character_associations():
    try:
        logger.info("Updating character associations with players...")
        for user in User.objects.filter(is_active=True):
            update_character_associations(user)
        logger.info("Character associations updated")
    except:
        logger.exception("update failed")
        raise

#------------------------------------------------------------------------------
def update_character_associations(user):
    logger.debug("Updating character ownerships for '%s'..." % user.username)
    # we delete all the previous ownerships
    CharacterOwnership.objects.filter(owner=user).delete()
    # get all the user's registered api credentials
    user_apis = UserAPIKey.objects.filter(user=user)
    invalid_apis = []
    for user_api in user_apis:
        try:
            ids = [ char.characterID for char in api.get_account_characters(user_api) ]
            user_api.is_valid = True
            for member in Member.objects.filter(characterID__in=ids):
                try:
                    ownership = member.ownership
                except CharacterOwnership.DoesNotExist:
                    ownership = CharacterOwnership()
                    ownership.character = member
                ownership.owner = user
                ownership.save()
        except eveapi.Error as err:
            if err.code in [202, 203, 204, 205, 210, 212]:
                # authentication failure error codes. 
                # This happens if the apiKey does not match the userID
                # TODO put these in eveapi or in the database.
                user_api.is_valid = False
                invalid_apis.append(user_api)
        user_api.save()
    if invalid_apis:
        # we notify the user by email
        ctx_dict = {'site': settings.ECM_BASE_URL,
                    'user_name': user.username,
                    'invalid_apis': invalid_apis}
        subject = render_to_string('auth/invalid_api_email_subject.txt', ctx_dict, 
                                   RequestContext(HttpRequest()))
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        txt_content = render_to_string('auth/invalid_api_email.txt', ctx_dict,
                                       RequestContext(HttpRequest()))
        html_content = render_to_string('auth/invalid_api_email.html', ctx_dict,
                                        RequestContext(HttpRequest()))
        msg = EmailMultiAlternatives(subject, body=txt_content, to=[user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info("API credentials for '%s' are invalid. User notified by email." % user.username)

#------------------------------------------------------------------------------
@transaction.commit_on_success
def cleanup_unregistered_users():
    try:
        logger.info("Deleting activation keys...")
        count = 0
        for profile in RegistrationProfile.objects.all():
            if profile.activation_key_expired():
                user = profile.user
                count += 1
                if user.is_active:
                    # user has activated his/her account. we delete the activation key
                    profile.delete()
                else:
                    logger.info("activation key has exprired for '%s', deleting user..." % user.username)
                    user.delete() # this will delete the profile along with the user
        logger.info("%d activation keys deleted" % count)
    except:
        logger.exception("cleanup failed")
        raise

#------------------------------------------------------------------------------
@transaction.commit_on_success
def update_all_users_accesses():
    try:
        logger.info("Updating user accesses from their in-game roles...")
        for user in User.objects.filter(is_active=True):
            update_user_accesses(user)
        logger.info("User accesses updated")
    except:
        logger.exception("update failed")
        raise

#------------------------------------------------------------------------------
def update_user_accesses(user):
    owned = CharacterOwnership.objects.filter(owner=user)
    titles = Title.objects.none()
    director = False
    for char in owned:
        director = char.character.is_director() or director
        titles |= char.character.titles.all()
    ids = titles.distinct().values_list("titleID", flat=True)
    user.groups.clear()
    for id in ids:
        user.groups.add(Group.objects.get(id=id))
    if director:
        user.groups.add(Group.objects.get(id=settings.DIRECTOR_GROUP_ID))