# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ecm.lib.bigint
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FuelLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('type_id', models.IntegerField(db_index=True)),
                ('quantity', models.IntegerField()),
                ('consumption', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['pos', 'date', 'type_id'],
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='POS',
            fields=[
                ('item_id', ecm.lib.bigint.BigAutoField(serialize=False, primary_key=True)),
                ('location_id', models.BigIntegerField(default=0)),
                ('location', models.CharField(default=b'', max_length=255)),
                ('moon_id', models.BigIntegerField(default=0)),
                ('moon', models.CharField(default=b'', max_length=255)),
                ('type_id', models.IntegerField(default=0)),
                ('type_name', models.CharField(default=b'', max_length=255)),
                ('state', models.SmallIntegerField(default=0, choices=[(0, b'Unanchorded'), (1, b'Anchored/Offline'), (2, b'Onlining'), (3, b'Reinforced'), (4, b'Online')])),
                ('state_timestamp', models.DateTimeField(auto_now_add=True)),
                ('online_timestamp', models.DateTimeField(auto_now_add=True)),
                ('cached_until', models.DateTimeField(auto_now_add=True)),
                ('usage_flags', models.SmallIntegerField(default=0)),
                ('deploy_flags', models.SmallIntegerField(default=0)),
                ('allow_corporation_members', models.BooleanField(default=False)),
                ('allow_alliance_members', models.BooleanField(default=False)),
                ('use_standings_from', models.BigIntegerField(default=0)),
                ('standings_threshold', models.FloatField(default=0.0)),
                ('security_status_threshold', models.FloatField(default=0.0)),
                ('attack_on_concord_flag', models.BooleanField(default=False)),
                ('attack_on_aggression', models.BooleanField(default=False)),
                ('attack_on_corp_war', models.BooleanField(default=False)),
                ('fuel_type_id', models.IntegerField(default=0, choices=[(4312, b'Gallente Fuel Block'), (4051, b'Caldari Fuel Block'), (4246, b'Minmatar Fuel Block'), (4247, b'Amarr Fuel Block')])),
                ('custom_name', models.CharField(max_length=255, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('has_sov', models.BooleanField(default=False)),
                ('authorized_groups', models.ManyToManyField(related_name='visible_group', to='auth.Group', blank=True)),
                ('operators', models.ManyToManyField(related_name='operated_poses', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': 'POS',
                'verbose_name_plural': 'POSes',
            },
        ),
        migrations.AddField(
            model_name='fuellevel',
            name='pos',
            field=models.ForeignKey(related_name='fuel_levels', to='pos.POS'),
        ),
    ]
