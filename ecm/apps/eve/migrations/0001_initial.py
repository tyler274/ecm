# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ecm.lib.bigint


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlueprintReq',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('activityID', models.SmallIntegerField(default=1, choices=[(1, b'Manufacturing'), (3, b'Time Efficiency Research'), (4, b'Material Efficiency Research'), (5, b'Copying'), (6, b'Duplicating'), (7, b'Reverse Engineering'), (8, b'Invention')])),
                ('quantity', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['blueprint', 'activityID', 'required_type'],
            },
        ),
        migrations.CreateModel(
            name='BlueprintType',
            fields=[
                ('blueprintTypeID', models.IntegerField(serialize=False, primary_key=True)),
                ('productionTime', models.IntegerField(null=True, blank=True)),
                ('researchProductivityTime', models.IntegerField(null=True, blank=True)),
                ('researchMaterialTime', models.IntegerField(null=True, blank=True)),
                ('researchCopyTime', models.IntegerField(null=True, blank=True)),
                ('inventionTime', models.IntegerField(null=True, blank=True)),
                ('maxProductionLimit', models.IntegerField(null=True, blank=True)),
                ('inventionBaseChance', models.FloatField(null=True, blank=True)),
                ('parent_blueprint', models.ForeignKey(related_name='children_blueprints', db_column=b'parentBlueprintTypeID', blank=True, to='eve.BlueprintType', null=True)),
            ],
            options={
                'ordering': ['blueprintTypeID'],
                'get_latest_by': 'blueprintTypeID',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('categoryID', models.IntegerField(serialize=False, primary_key=True)),
                ('categoryName', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('iconID', models.IntegerField(null=True, blank=True)),
                ('published', models.SmallIntegerField(db_index=True, null=True, blank=True)),
            ],
            options={
                'ordering': ['categoryID'],
                'get_latest_by': 'categoryID',
            },
        ),
        migrations.CreateModel(
            name='CelestialObject',
            fields=[
                ('itemID', models.IntegerField(serialize=False, primary_key=True)),
                ('solarSystemID', models.IntegerField(db_index=True, null=True, blank=True)),
                ('regionID', models.IntegerField(db_index=True, null=True, blank=True)),
                ('itemName', models.CharField(max_length=100, null=True, blank=True)),
                ('security', models.FloatField(null=True, blank=True)),
                ('x', models.FloatField(null=True, blank=True)),
                ('y', models.FloatField(null=True, blank=True)),
                ('z', models.FloatField(null=True, blank=True)),
            ],
            options={
                'ordering': ['itemID'],
                'get_latest_by': 'itemID',
            },
        ),
        migrations.CreateModel(
            name='ControlTowerResource',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('purpose', models.SmallIntegerField()),
                ('quantity', models.SmallIntegerField()),
                ('minSecurityLevel', models.FloatField(null=True, blank=True)),
                ('factionID', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['control_tower', 'resource'],
                'get_latest_by': 'control_tower',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('groupID', models.IntegerField(serialize=False, primary_key=True)),
                ('groupName', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('iconID', models.IntegerField(null=True, blank=True)),
                ('useBasePrice', models.SmallIntegerField(null=True, blank=True)),
                ('allowManufacture', models.SmallIntegerField(null=True, blank=True)),
                ('allowRecycler', models.SmallIntegerField(null=True, blank=True)),
                ('anchored', models.SmallIntegerField(null=True, blank=True)),
                ('anchorable', models.SmallIntegerField(null=True, blank=True)),
                ('fittableNonSingleton', models.SmallIntegerField(null=True, blank=True)),
                ('published', models.SmallIntegerField(null=True, blank=True)),
                ('category', models.ForeignKey(related_name='groups', db_column=b'categoryID', to='eve.Category')),
            ],
            options={
                'ordering': ['groupID'],
                'get_latest_by': 'groupID',
            },
        ),
        migrations.CreateModel(
            name='MarketGroup',
            fields=[
                ('marketGroupID', models.IntegerField(serialize=False, primary_key=True)),
                ('marketGroupName', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('iconID', models.IntegerField(null=True, blank=True)),
                ('hasTypes', models.SmallIntegerField(null=True, blank=True)),
                ('parent_group', models.ForeignKey(related_name='children_groups', db_column=b'parentGroupID', blank=True, to='eve.MarketGroup', null=True)),
            ],
            options={
                'ordering': ['marketGroupID'],
                'get_latest_by': 'marketGroupID',
            },
        ),
        migrations.CreateModel(
            name='SkillReq',
            fields=[
                ('id', ecm.lib.bigint.BigAutoField(serialize=False, primary_key=True)),
                ('required_level', models.SmallIntegerField()),
            ],
            options={
                'ordering': ['item', 'skill'],
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('typeID', models.IntegerField(serialize=False, primary_key=True)),
                ('typeName', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('volume', models.FloatField(null=True, blank=True)),
                ('portionSize', models.IntegerField(null=True, blank=True)),
                ('raceID', models.SmallIntegerField(null=True, blank=True)),
                ('basePrice', models.FloatField(null=True, blank=True)),
                ('metaGroupID', models.SmallIntegerField(null=True, blank=True)),
                ('published', models.SmallIntegerField(db_index=True, null=True, blank=True)),
                ('blueprint', models.OneToOneField(null=True, db_column=b'blueprintTypeID', blank=True, to='eve.BlueprintType')),
                ('category', models.ForeignKey(related_name='types', db_column=b'categoryID', to='eve.Category')),
                ('group', models.ForeignKey(related_name='types', db_column=b'groupID', to='eve.Group')),
                ('market_group', models.ForeignKey(related_name='items', db_column=b'marketGroupID', blank=True, to='eve.MarketGroup', null=True)),
            ],
            options={
                'ordering': ['typeID'],
                'get_latest_by': 'typeID',
            },
        ),
        migrations.AddField(
            model_name='skillreq',
            name='item',
            field=models.ForeignKey(related_name='skill_reqs', to='eve.Type'),
        ),
        migrations.AddField(
            model_name='skillreq',
            name='skill',
            field=models.ForeignKey(related_name='+', to='eve.Type'),
        ),
        migrations.AddField(
            model_name='controltowerresource',
            name='control_tower',
            field=models.ForeignKey(related_name='tower_resources_t', db_column=b'controlTowerTypeID', to='eve.Type'),
        ),
        migrations.AddField(
            model_name='controltowerresource',
            name='resource',
            field=models.ForeignKey(related_name='tower_resources_r', db_column=b'resourceTypeID', to='eve.Type'),
        ),
        migrations.AddField(
            model_name='celestialobject',
            name='group',
            field=models.ForeignKey(db_column=b'groupID', blank=True, to='eve.Group', null=True),
        ),
        migrations.AddField(
            model_name='celestialobject',
            name='type',
            field=models.ForeignKey(to='eve.Type', db_column=b'typeID'),
        ),
        migrations.AddField(
            model_name='blueprinttype',
            name='product',
            field=models.OneToOneField(null=True, db_column=b'productTypeID', blank=True, to='eve.Type'),
        ),
        migrations.AddField(
            model_name='blueprintreq',
            name='blueprint',
            field=models.ForeignKey(related_name='requirements', db_column=b'blueprintTypeID', to='eve.BlueprintType'),
        ),
        migrations.AddField(
            model_name='blueprintreq',
            name='required_type',
            field=models.ForeignKey(to='eve.Type', db_column=b'requiredTypeID'),
        ),
        migrations.AlterUniqueTogether(
            name='controltowerresource',
            unique_together=set([('control_tower', 'resource')]),
        ),
    ]
