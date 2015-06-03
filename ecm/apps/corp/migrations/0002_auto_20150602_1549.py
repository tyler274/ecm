# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, connection
from django.core.management import call_command


# def mysql_quotes(sql):
#     if 'mysql' == connection.vendor:
#         return sql.replace('"', '`')
#     else:
#         return sql

def load_corp_data(apps, schema_editor):
    call_command("loaddata", "0009_mercenary_wallet_data.json")

    # cursor = connection.cursor()
    #
    # cursor.execute(mysql_quotes('SELECT "hangarID", "name", "accessLvl" FROM "corp_hangar";'))
    # hangar_rows = cursor.fetchall()
    #
    # cursor.execute(mysql_quotes('SELECT "walletID", "name", "accessLvl" FROM "corp_wallet";'))
    # wallet_rows = cursor.fetchall()
    #
    # Corporation = apps.get_model("corp", "Corporation")
    # Hangar = apps.get_model("corp", "Hangar")
    # CorpHangar = apps.get_model("corp", "CorpHangar")
    # CorpWallet = apps.get_model("corp", "CorpWallet")
    # Wallet = apps.get_model("corp", "Wallet")
    #
    # try:
    #     my_corp = Corporation.objects.get(is_my_corp=True)
    #
    #     for hangarID, name, access_lvl in hangar_rows:
    #         hangar = Hangar.objects.get(hangarID=hangarID)
    #         CorpHangar.objects.create(corp=my_corp, hangar=hangar, name=name, access_lvl=access_lvl)
    #
    #     for walletID, name, access_lvl in wallet_rows:
    #         wallet = Wallet.objects.get(walletID=walletID)
    #         CorpWallet.objects.create(corp=my_corp, wallet=wallet, name=name, access_lvl=access_lvl)
    # except Corporation.DoesNotExist:
    #     pass


class Migration(migrations.Migration):

    dependencies = [
        ('corp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_corp_data),
    ]
