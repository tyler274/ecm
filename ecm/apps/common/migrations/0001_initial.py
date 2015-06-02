# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='APICall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=1024)),
                ('mask', models.IntegerField()),
                ('type', models.SmallIntegerField(choices=[(1, b'Character'), (2, b'Corporation')])),
                ('group', models.SmallIntegerField(choices=[(1, b'Account and Market'), (2, b'Science and Industry'), (3, b'Private Information'), (4, b'Public Information'), (5, b'Corporation Members'), (6, b'Outposts and Starbases'), (7, b'Communications')])),
                ('required', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'API Call',
                'verbose_name_plural': 'API Calls',
            },
        ),
        migrations.CreateModel(
            name='ColorThreshold',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', models.CharField(max_length=64)),
                ('threshold', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ExternalApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, validators=[django.core.validators.RegexValidator(b'^\\w+$', message=b'Only letters and digits')])),
                ('url', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='GroupBinding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField()),
                ('external_name', models.CharField(max_length=256)),
                ('external_app', models.ForeignKey(related_name='group_bindings', to='common.ExternalApplication')),
                ('group', models.ForeignKey(related_name='bindings', to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Motd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField(default=b'MOTD Text')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('markup', models.SmallIntegerField(default=0, choices=[(0, b'Plain Text')])),
                ('user', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
                'get_latest_by': 'date',
                'verbose_name': 'Message of the day',
                'verbose_name_plural': 'Messages of the day',
            },
        ),
        migrations.CreateModel(
            name='RegistrationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, verbose_name=b'activation key')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'registration profile',
                'verbose_name_plural': 'registration profiles',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('name', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('value', models.TextField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UpdateDate',
            fields=[
                ('model_name', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('update_date', models.DateTimeField()),
                ('prev_update', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-update_date'],
            },
        ),
        migrations.CreateModel(
            name='UrlPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.CharField(max_length=256)),
                ('groups', models.ManyToManyField(related_name='allowed_urls', to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='UserAPIKey',
            fields=[
                ('keyID', models.IntegerField(serialize=False, primary_key=True)),
                ('vCode', models.CharField(max_length=255)),
                ('is_valid', models.BooleanField(default=True)),
                ('user', models.ForeignKey(related_name='eve_accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='UserBinding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField()),
                ('external_name', models.CharField(max_length=255)),
                ('external_app', models.ForeignKey(related_name='user_bindings', to='common.ExternalApplication')),
                ('user', models.ForeignKey(related_name='bindings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
