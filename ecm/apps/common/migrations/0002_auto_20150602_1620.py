# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command


def load_common_data(apps, schema_editor):
    call_command("loaddata", "0006_apicall_data.json")
    call_command("loaddata", "0007_colorthreshold_data.json")


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_common_data),
    ]
