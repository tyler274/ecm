# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ecm.apps.scheduler.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GarbageCollector',
            fields=[
                ('model', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('min_entries_threshold', models.BigIntegerField(default=10000)),
                ('max_age_threshold', models.BigIntegerField()),
                ('age_units', models.BigIntegerField(default=18144000, choices=[(86400, 'days'), (604800, 'weeks'), (18144000, 'months')])),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('function', models.CharField(max_length=256, validators=[ecm.apps.scheduler.validators.FunctionValidator()])),
                ('args', models.CharField(default=b'{}', max_length=256, validators=[ecm.apps.scheduler.validators.ArgsValidator()])),
                ('priority', models.IntegerField(default=0)),
                ('next_execution', models.DateTimeField(auto_now_add=True)),
                ('last_execution', models.DateTimeField(null=True, blank=True)),
                ('frequency', models.IntegerField()),
                ('frequency_units', models.IntegerField(default=3600, choices=[(1, 'seconds'), (60, 'minutes'), (3600, 'hours'), (86400, 'days'), (604800, 'weeks')])),
                ('is_active', models.BooleanField(default=True)),
                ('is_scheduled', models.BooleanField(default=False)),
                ('is_running', models.BooleanField(default=False)),
                ('is_one_shot', models.BooleanField(default=False)),
                ('is_last_exec_success', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'scheduled task',
                'verbose_name_plural': 'scheduled tasks',
            },
        ),
    ]
