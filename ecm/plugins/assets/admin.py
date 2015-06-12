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

__date__ = "2010-05-14"
__author__ = "diabeteman"


from django.contrib import admin
from ecm.plugins.assets.models import Asset, AssetDiff

class AssetAdmin(admin.ModelAdmin):
    list_display = ['itemID', 'solarSystemID', 'stationID', 'hangarID', 'container1', 'container2', 
                    'eve_type', 'quantity', 'flag', 'singleton', 'hasContents']

class AssetDiffAdmin(admin.ModelAdmin):
    list_display = ['solarSystemID', 'stationID', 'hangarID', 'eve_type', 'quantity', 'date', 'new']



admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetDiff, AssetDiffAdmin)
