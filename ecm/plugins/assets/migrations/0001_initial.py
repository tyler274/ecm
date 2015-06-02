# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ecm.lib.bigint
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eve', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('itemID', ecm.lib.bigint.BigAutoField(serialize=False, primary_key=True)),
                ('solarSystemID', models.BigIntegerField()),
                ('stationID', models.BigIntegerField()),
                ('hangarID', models.PositiveIntegerField()),
                ('container1', models.BigIntegerField(null=True, blank=True)),
                ('container2', models.BigIntegerField(null=True, blank=True)),
                ('quantity', models.BigIntegerField(default=0)),
                ('flag', models.BigIntegerField()),
                ('singleton', models.BooleanField(default=False)),
                ('hasContents', models.BooleanField(default=False)),
                ('volume', models.FloatField(default=0.0)),
                ('closest_object_id', models.BigIntegerField(default=0)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('is_bpc', models.NullBooleanField(default=None)),
                ('eve_type', models.ForeignKey(to='eve.Type', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
            options={
                'get_latest_by': 'itemID',
            },
        ),
        migrations.CreateModel(
            name='AssetDiff',
            fields=[
                ('id', ecm.lib.bigint.BigAutoField(serialize=False, primary_key=True)),
                ('solarSystemID', models.BigIntegerField()),
                ('stationID', models.BigIntegerField()),
                ('hangarID', models.PositiveIntegerField()),
                ('quantity', models.IntegerField(default=0)),
                ('date', models.DateTimeField(db_index=True)),
                ('new', models.BooleanField()),
                ('flag', models.BigIntegerField()),
                ('volume', models.BigIntegerField(default=0)),
                ('eve_type', models.ForeignKey(to='eve.Type', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
    ]
