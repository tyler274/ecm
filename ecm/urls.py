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

from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

from ecm.views.account.forms import PasswordChangeForm, PasswordResetForm, PasswordSetForm
from ecm import views as ecm_views

admin.autodiscover()

def robots(request):
    return HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")

urlpatterns = [
    ###########################################################################
    # MISC VIEWS
    url(r'^robots\.txt$', robots),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    url('^', include('django.contrib.auth.urls')),
    ###########################################################################
    # DJANGO BUILT-IN AUTH VIEWS
    url(r'^account/login/$', auth_views.login, 
            {
                'template_name' : 'ecm/auth/login.html'
            }
        ),
    url(r'^account/logout/$', auth_views.logout, 
            {
                'next_page' : '/'
            }
        ),
    url(r'^account/passwordchange/$', auth_views.password_change,
            {
                'template_name' : 'ecm/auth/password_change.html',
                'password_change_form' : PasswordChangeForm
            }
        ),
    url(r'^account/passwordchange/done/$',  auth_views.password_change_done,
            {
                'template_name' : 'ecm/auth/password_change_done.html'
            }
        ),
    url(r'^account/passwordreset/$', auth_views.password_reset,
            {
                'template_name' : 'ecm/auth/password_reset.html',
                'email_template_name' : 'ecm/auth/password_reset_email.txt',
                'password_reset_form' : PasswordResetForm,
                'post_reset_redirect' : '/account/passwordreset/sent/'
            }
        ),
    url(r'^account/passwordreset/sent/$',   auth_views.password_reset_done,
            {
                'template_name' : 'ecm/auth/password_reset_done.html'
            }
        ),
    url(r'^account/passwordreset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,
            {
                'template_name' : 'ecm/auth/password_reset_confirm.html',
                'set_password_form' : PasswordSetForm
            }
        ),
    url(r'^account/passwordreset/complete/$', auth_views.password_reset_complete,
            {
                'template_name' : 'ecm/auth/password_reset_complete.html'
            }
        ),

]

urlpatterns += [
    ###########################################################################
    # ECM AUTH + USER PROFILE VIEWS
    url(r'^account/$', ecm_views.account.home.account),
    url(r'^account/addapi/$', ecm_views.account.home.add_api),
    url(r'^account/deleteapi/(\d+)/$', ecm_views.account.home.delete_api),
    url(r'^account/deletecharacter/(\d+)/$', ecm_views.account.home.delete_character),
    url(r'^account/editapi/(\d+)/$', ecm_views.account.home.edit_api),
    url(r'^account/binding/add/(\d+)/$', ecm_views.account.home.add_binding),
    url(r'^account/binding/delete/(\d+)/$', ecm_views.account.home.delete_binding),

    url(r'^account/create/$', ecm_views.account.signup.create_account),
    url(r'^account/activate/(\w+)/$', ecm_views.account.signup.activate_account),
]

urlpatterns += [
    ###########################################################################
    # COMMON VIEWS
    url(r'^$', ecm_views.common.home),
    url(r'^editmotd/$', ecm_views.common.edit_motd),
    url(r'^editapi/$', ecm_views.common.edit_apikey),
]

urlpatterns += [
    ###########################################################################
    # JSON API VIEWS
    url(r'^api/players/$', ecm_views.api.players),
    url(r'^api/bindings/(\w+)/users/$', ecm_views.api.user_bindings),
    url(r'^api/bindings/(\w+)/groups/$', ecm_views.api.group_bindings),
]

urlpatterns += [
    ###########################################################################
    # AJAX QUERY VIEWS
    url(r'^ajax/celestials/$', ecm_views.ajax.celestial.list),
    url(r'^ajax/solarsystems/$', ecm_views.ajax.solarsystem.list),
    url(r'^ajax/moons/$', ecm_views.ajax.moons.list),
]

import ecm.apps
CORE_APPS_URLS = []
for app in ecm.apps.LIST:
    if app.urlconf is not None:
        CORE_APPS_URLS.append( url(r'^' + app.app_prefix + '/', include(app.urlconf)) )
if CORE_APPS_URLS:
    urlpatterns += [*CORE_APPS_URLS,]


import ecm.plugins
PLUGINS_URLS = []
for plugin in ecm.plugins.LIST:
    PLUGINS_URLS.append( url(r'^' + plugin.app_prefix + '/', include(plugin.urlconf)) )
if PLUGINS_URLS:
    urlpatterns += [*PLUGINS_URLS,]
    
################################################
#custom handlers for http return codes
handler500='ecm.views.custom_handlers.server_error'
