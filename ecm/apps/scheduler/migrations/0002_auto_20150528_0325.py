# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ecm.apps.scheduler.validators


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledtask',
            name='args',
            field=models.CharField(default=b'{}', max_length=256, validators=[ecm.apps.scheduler.validators.ArgsValidator()]),
        ),
        migrations.AlterField(
            model_name='scheduledtask',
            name='function',
            field=models.CharField(max_length=256, validators=[ecm.apps.scheduler.validators.FunctionValidator()]),
        ),
    ]
