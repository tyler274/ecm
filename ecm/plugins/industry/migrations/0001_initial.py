# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogEntry',
            fields=[
                ('typeID', models.IntegerField(serialize=False, primary_key=True)),
                ('typeName', models.CharField(max_length=100)),
                ('fixed_price', models.FloatField(null=True, blank=True)),
                ('production_cost', models.FloatField(null=True, blank=True)),
                ('public_price', models.FloatField(null=True, blank=True)),
                ('last_update', models.DateTimeField(null=True, blank=True)),
                ('is_available', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Catalog Entry',
                'verbose_name_plural': 'Catalog Entries',
            },
        ),
        migrations.CreateModel(
            name='InventionPolicy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_group_id', models.IntegerField(default=0)),
                ('item_id', models.IntegerField(null=True, blank=True)),
                ('item_group', models.CharField(max_length=255)),
                ('encryption_skill_lvl', models.SmallIntegerField(default=5)),
                ('science1_skill_lvl', models.SmallIntegerField(default=5)),
                ('science2_skill_lvl', models.SmallIntegerField(default=5)),
                ('me_mod', models.IntegerField(blank=True, null=True, choices=[(1, b'+1'), (2, b'+2'), (3, b'+3'), (-1, b'-1'), (-2, b'-2'), (None, b'None')])),
            ],
            options={
                'verbose_name': 'Invention Policy',
                'verbose_name_plural': 'Invention Policies',
            },
        ),
        migrations.CreateModel(
            name='ItemGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('items', models.ManyToManyField(related_name='item_groups', to='industry.CatalogEntry')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.SmallIntegerField(default=0, choices=[(0, b'Pending'), (1, b'Planned'), (2, b'In Production'), (3, b'Ready')])),
                ('item_id', models.PositiveIntegerField()),
                ('runs', models.FloatField()),
                ('activity', models.SmallIntegerField(default=1, choices=[(0, b'Supply'), (1, b'Manufacturing'), (8, b'Invention')])),
                ('due_date', models.DateField(null=True, blank=True)),
                ('duration', models.BigIntegerField(default=0)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('assignee', models.ForeignKey(related_name='jobs', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.PositiveIntegerField(default=0, choices=[(0, b'Draft'), (1, b'Pending'), (2, b'Problematic'), (3, b'Accepted'), (5, b'In Preparation'), (6, b'Ready'), (7, b'Delivered'), (8, b'Paid'), (9, b'Canceled by Client'), (10, b'Rejected by Responsible')])),
                ('client', models.CharField(max_length=255, null=True, blank=True)),
                ('delivery_location', models.CharField(max_length=255, null=True, blank=True)),
                ('delivery_date', models.DateField(null=True, blank=True)),
                ('quote', models.FloatField(default=0.0)),
                ('delivery_boy', models.ForeignKey(related_name='orders_delivered', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('originator', models.ForeignKey(related_name='orders_created', to=settings.AUTH_USER_MODEL)),
                ('responsible', models.ForeignKey(related_name='orders_responsible', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='OrderLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.PositiveSmallIntegerField(choices=[(0, b'Draft'), (1, b'Pending'), (2, b'Problematic'), (3, b'Accepted'), (5, b'In Preparation'), (6, b'Ready'), (7, b'Delivered'), (8, b'Paid'), (9, b'Canceled by Client'), (10, b'Rejected by Responsible')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('order', models.ForeignKey(related_name='logs', to='industry.Order')),
                ('user', models.ForeignKey(related_name='logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['order', 'date'],
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='OrderRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField()),
                ('cost', models.FloatField(default=0.0)),
                ('surcharge', models.FloatField(default=0.0)),
                ('catalog_entry', models.ForeignKey(related_name='order_rows', to='industry.CatalogEntry')),
                ('order', models.ForeignKey(related_name='rows', to='industry.Order')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='OwnedBlueprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typeID', models.IntegerField()),
                ('me', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('pe', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('copy', models.BooleanField(default=False)),
                ('runs', models.SmallIntegerField(default=0)),
                ('invented', models.BooleanField(default=False)),
                ('catalog_entry', models.ForeignKey(related_name='blueprints', blank=True, to='industry.CatalogEntry', null=True)),
            ],
            options={
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Price History',
                'verbose_name_plural': 'Prices History',
            },
        ),
        migrations.CreateModel(
            name='PricingPolicy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('surcharge_relative', models.FloatField(default=0.0)),
                ('surcharge_absolute', models.FloatField(default=0.0)),
                ('priority', models.SmallIntegerField(default=0)),
                ('item_group', models.ForeignKey(default=None, blank=True, to='industry.ItemGroup', null=True)),
                ('user_group', models.ForeignKey(default=None, blank=True, to='auth.Group', null=True)),
            ],
            options={
                'verbose_name': 'Surcharge Policy',
                'verbose_name_plural': 'Surcharge Policies',
            },
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('typeID', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('price', models.FloatField(default=0.0)),
                ('auto_update', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Supplies',
            },
        ),
        migrations.CreateModel(
            name='SupplySource',
            fields=[
                ('location_id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='supply',
            name='supply_source',
            field=models.ForeignKey(related_name='prices', default=1, to='industry.SupplySource'),
        ),
        migrations.AddField(
            model_name='pricehistory',
            name='supply',
            field=models.ForeignKey(related_name='price_histories', to='industry.Supply'),
        ),
        migrations.AddField(
            model_name='job',
            name='blueprint',
            field=models.ForeignKey(related_name='jobs', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='industry.OwnedBlueprint', null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='order',
            field=models.ForeignKey(related_name='jobs', blank=True, to='industry.Order', null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='parent_job',
            field=models.ForeignKey(related_name='children_jobs', blank=True, to='industry.Job', null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='row',
            field=models.ForeignKey(related_name='jobs', blank=True, to='industry.OrderRow', null=True),
        ),
    ]
