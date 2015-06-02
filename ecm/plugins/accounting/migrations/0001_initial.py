# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contractID', models.BigIntegerField(serialize=False, primary_key=True)),
                ('issuerID', models.BigIntegerField()),
                ('issuerCorpID', models.BigIntegerField()),
                ('assigneeID', models.BigIntegerField()),
                ('acceptorID', models.BigIntegerField()),
                ('startStationID', models.BigIntegerField()),
                ('endStationID', models.BigIntegerField()),
                ('type', models.SmallIntegerField(choices=[(1, 'ItemExchange'), (2, 'Courier'), (3, 'Loan'), (4, 'Auction'), (-1, 'Unkown')])),
                ('status', models.SmallIntegerField(choices=[(1, 'Outstanding'), (2, 'Deleted'), (3, 'Completed'), (4, 'Failed'), (5, 'CompletedByIssuer'), (6, 'CompletedByContractor'), (7, 'Cancelled'), (8, 'Rejected'), (9, 'Reversed'), (10, 'InProgress'), (-1, 'Unknown')])),
                ('title', models.CharField(max_length=255)),
                ('forCorp', models.BooleanField()),
                ('availability', models.SmallIntegerField(choices=[(0, 'Private'), (1, 'Public'), (-1, 'Unknown')])),
                ('dateIssued', models.DateTimeField(null=True, blank=True)),
                ('dateExpired', models.DateTimeField(null=True, blank=True)),
                ('dateAccepted', models.DateTimeField(null=True, blank=True)),
                ('dateCompleted', models.DateTimeField(null=True, blank=True)),
                ('numDays', models.SmallIntegerField()),
                ('price', models.FloatField()),
                ('reward', models.FloatField()),
                ('collateral', models.FloatField()),
                ('buyout', models.FloatField()),
                ('volume', models.FloatField()),
            ],
            options={
                'ordering': ['dateIssued'],
                'verbose_name': 'Contract',
            },
        ),
        migrations.CreateModel(
            name='ContractItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recordID', models.BigIntegerField()),
                ('typeID', models.IntegerField()),
                ('quantity', models.BigIntegerField()),
                ('rawQuantity', models.BigIntegerField()),
                ('singleton', models.SmallIntegerField()),
                ('included', models.SmallIntegerField()),
                ('contract', models.ForeignKey(related_name='items', to='accounting.Contract')),
            ],
            options={
                'verbose_name': 'Contract Item',
            },
        ),
        migrations.CreateModel(
            name='EntryType',
            fields=[
                ('refTypeID', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('refTypeName', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('refID', models.BigIntegerField()),
                ('date', models.DateTimeField()),
                ('ownerName1', models.CharField(max_length=128)),
                ('ownerID1', models.BigIntegerField()),
                ('ownerName2', models.CharField(max_length=128)),
                ('ownerID2', models.BigIntegerField()),
                ('argName1', models.CharField(max_length=128)),
                ('argID1', models.BigIntegerField()),
                ('amount', models.FloatField()),
                ('balance', models.FloatField()),
                ('reason', models.CharField(max_length=512)),
                ('type', models.ForeignKey(to='accounting.EntryType')),
                ('wallet', models.ForeignKey(to='corp.Wallet')),
            ],
            options={
                'get_latest_by': 'refID',
                'verbose_name': 'Journal Entry',
                'verbose_name_plural': 'Journal Entries',
            },
        ),
        migrations.CreateModel(
            name='MarketOrder',
            fields=[
                ('orderID', models.BigIntegerField(serialize=False, primary_key=True)),
                ('charID', models.BigIntegerField()),
                ('stationID', models.BigIntegerField()),
                ('volEntered', models.BigIntegerField()),
                ('volRemaining', models.BigIntegerField()),
                ('minVolume', models.BigIntegerField()),
                ('orderState', models.SmallIntegerField(choices=[(0, b'Open/Active'), (1, b'Closed'), (2, b'Expired (or Fulfilled)'), (3, b'Cancelled'), (4, b'Pending'), (5, b'Character Deleted')])),
                ('typeID', models.IntegerField()),
                ('range', models.SmallIntegerField()),
                ('duration', models.SmallIntegerField()),
                ('escrow', models.FloatField()),
                ('price', models.FloatField()),
                ('bid', models.BooleanField(default=False)),
                ('issued', models.DateTimeField()),
                ('accountKey', models.ForeignKey(related_name='market_orders', to='corp.Wallet')),
            ],
            options={
                'ordering': ['orderID'],
                'verbose_name': 'Market Order',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('default_period', models.IntegerField(null=True, blank=True)),
                ('default_step', models.IntegerField(null=True, blank=True)),
                ('entry_types', models.ManyToManyField(to='accounting.EntryType')),
            ],
            options={
                'verbose_name': 'Report',
            },
        ),
        migrations.CreateModel(
            name='TransactionEntry',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('date', models.DateTimeField()),
                ('quantity', models.BigIntegerField(default=0)),
                ('typeID', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0.0)),
                ('clientID', models.BigIntegerField(default=0)),
                ('clientName', models.CharField(max_length=128)),
                ('stationID', models.BigIntegerField(default=0)),
                ('transactionType', models.SmallIntegerField(default=0, choices=[(0, b'Buy'), (1, b'Sell')])),
                ('transactionFor', models.SmallIntegerField(default=0, choices=[(0, b'Personal'), (1, b'Corporation')])),
                ('journal', models.ForeignKey(related_name='JournalEntry', to='accounting.JournalEntry')),
                ('wallet', models.ForeignKey(to='corp.Wallet')),
            ],
            options={
                'ordering': ['date'],
                'get_latest_by': 'date',
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
    ]
