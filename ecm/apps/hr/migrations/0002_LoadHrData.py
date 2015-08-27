# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command


def load_corp_data(apps, schema_editor):
    call_command("loaddata", "initial_data.json")
    # pass

class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_corp_data),
    ]
