# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alliance',
            fields=[
                ('allianceID', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('shortName', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CorpGroup',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='CorpHangar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('access_lvl', models.PositiveIntegerField(default=1000)),
            ],
            options={
                'ordering': ('corp', 'hangar'),
            },
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('ecm_url', models.CharField(max_length=200, null=True, blank=True)),
                ('is_my_corp', models.BooleanField(default=False)),
                ('is_trusted', models.BooleanField(default=False)),
                ('corporationID', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('corporationName', models.CharField(max_length=256, null=True, blank=True)),
                ('ticker', models.CharField(max_length=8, null=True, blank=True)),
                ('ceoID', models.BigIntegerField(null=True, blank=True)),
                ('ceoName', models.CharField(max_length=256, null=True, blank=True)),
                ('stationID', models.BigIntegerField(null=True, blank=True)),
                ('stationName', models.CharField(max_length=256, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('taxRate', models.IntegerField(null=True, blank=True)),
                ('memberLimit', models.IntegerField(null=True, blank=True)),
                ('private_key', models.TextField(null=True, blank=True)),
                ('public_key', models.TextField(null=True, blank=True)),
                ('key_fingerprint', models.CharField(max_length=255, null=True, blank=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('alliance', models.ForeignKey(related_name='corporations', blank=True, to='corp.Alliance', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CorpWallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('access_lvl', models.PositiveIntegerField(default=1000)),
                ('corp', models.ForeignKey(related_name='wallets', to='corp.Corporation')),
            ],
            options={
                'ordering': ('corp', 'wallet'),
            },
        ),
        migrations.CreateModel(
            name='Hangar',
            fields=[
                ('hangarID', models.PositiveIntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'ordering': ['hangarID'],
            },
        ),
        migrations.CreateModel(
            name='SharedData',
            fields=[
                ('url', models.CharField(max_length=255, serialize=False, editable=False, primary_key=True)),
                ('handler', models.CharField(max_length=255, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Standing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contactID', models.BigIntegerField(default=0)),
                ('contactName', models.CharField(max_length=255)),
                ('is_corp_contact', models.BooleanField(default=True)),
                ('value', models.IntegerField(default=0)),
                ('corp', models.ForeignKey(related_name='standings', to='corp.Corporation')),
            ],
            options={
                'ordering': ('-value', 'contactName'),
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('walletID', models.PositiveIntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'ordering': ['walletID'],
            },
        ),
        migrations.AddField(
            model_name='corpwallet',
            name='wallet',
            field=models.ForeignKey(related_name='corp_wallets', to='corp.Wallet'),
        ),
        migrations.AddField(
            model_name='corphangar',
            name='corp',
            field=models.ForeignKey(related_name='hangars', to='corp.Corporation'),
        ),
        migrations.AddField(
            model_name='corphangar',
            name='hangar',
            field=models.ForeignKey(related_name='corp_hangars', to='corp.Hangar'),
        ),
        migrations.AddField(
            model_name='corpgroup',
            name='allowed_shares',
            field=models.ManyToManyField(related_name='shared_datas', to='corp.SharedData'),
        ),
        migrations.AddField(
            model_name='corpgroup',
            name='corporations',
            field=models.ManyToManyField(related_name='corp_groups', to='corp.Corporation'),
        ),
        migrations.AlterUniqueTogether(
            name='corpwallet',
            unique_together=set([('corp', 'wallet')]),
        ),
        migrations.AlterUniqueTogether(
            name='corphangar',
            unique_together=set([('corp', 'hangar')]),
        ),
    ]
