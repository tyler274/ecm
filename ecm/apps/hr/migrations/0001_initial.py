# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ecm.lib.bigint
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('corp', '0001_initial'),
        ('eve', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recordID', models.BigIntegerField()),
                ('startDate', models.DateTimeField()),
                ('corporation', models.ForeignKey(related_name='employment_history', to='corp.Corporation')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('characterID', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128, db_index=True)),
                ('nickname', models.CharField(default=b'', max_length=256)),
                ('baseID', models.BigIntegerField(default=0)),
                ('corpDate', models.DateTimeField(auto_now_add=True)),
                ('lastLogin', models.DateTimeField(auto_now_add=True)),
                ('lastLogoff', models.DateTimeField(auto_now_add=True)),
                ('locationID', models.IntegerField(default=0, db_index=True)),
                ('location', models.CharField(default=b'???', max_length=256, null=True, blank=True)),
                ('ship', models.CharField(default=b'???', max_length=128)),
                ('accessLvl', models.BigIntegerField(default=0)),
                ('notes', models.TextField(null=True, blank=True)),
                ('DoB', models.CharField(max_length=128, null=True, blank=True)),
                ('race', models.CharField(max_length=128, null=True, blank=True)),
                ('bloodLine', models.CharField(max_length=128, null=True, blank=True)),
                ('ancestry', models.CharField(max_length=128, null=True, blank=True)),
                ('gender', models.CharField(max_length=128, null=True, blank=True)),
                ('cloneName', models.CharField(max_length=128, null=True, blank=True)),
                ('cloneSkillPoints', models.IntegerField(null=True, blank=True)),
                ('balance', models.FloatField(default=0.0)),
                ('memoryBonusName', models.CharField(max_length=128, null=True, blank=True)),
                ('memoryBonusValue', models.IntegerField(null=True, blank=True)),
                ('intelligenceBonusName', models.CharField(max_length=128, null=True, blank=True)),
                ('intelligenceBonusValue', models.IntegerField(null=True, blank=True)),
                ('charismaBonusName', models.CharField(max_length=128, null=True, blank=True)),
                ('charismaBonusValue', models.IntegerField(null=True, blank=True)),
                ('willpowerBonusName', models.CharField(max_length=128, null=True, blank=True)),
                ('willpowerBonusValue', models.IntegerField(null=True, blank=True)),
                ('perceptionBonusName', models.CharField(max_length=128, null=True, blank=True)),
                ('perceptionBonusValue', models.IntegerField(null=True, blank=True)),
                ('intelligence', models.IntegerField(default=0)),
                ('memory', models.IntegerField(default=0)),
                ('charisma', models.IntegerField(default=0)),
                ('perception', models.IntegerField(default=0)),
                ('willpower', models.IntegerField(default=0)),
                ('is_cyno_alt', models.BooleanField(default=False)),
                ('corp', models.ForeignKey(related_name='members', blank=True, to='corp.Corporation', null=True)),
                ('owner', models.ForeignKey(related_name='characters', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MemberDiff',
            fields=[
                ('id', ecm.lib.bigint.BigAutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('nickname', models.CharField(max_length=256, db_index=True)),
                ('new', models.BooleanField(default=True, db_index=True)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('member', models.ForeignKey(related_name='diffs', to='hr.Member')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='MemberSession',
            fields=[
                ('id', ecm.lib.bigint.BigAutoField(serialize=False, primary_key=True)),
                ('character_id', models.BigIntegerField(db_index=True)),
                ('session_begin', models.DateTimeField(db_index=True)),
                ('session_end', models.DateTimeField(db_index=True)),
                ('session_seconds', models.BigIntegerField(default=0, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recruiter', models.ForeignKey(related_name='recruiter', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('reference', models.ManyToManyField(related_name='reference', to=settings.AUTH_USER_MODEL, blank=True)),
                ('user', models.OneToOneField(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('roleID', models.BigIntegerField()),
                ('roleName', models.CharField(max_length=64)),
                ('dispName', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=256)),
                ('accessLvl', models.BigIntegerField(default=0)),
                ('hangar', models.ForeignKey(blank=True, to='corp.Hangar', null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RoleMemberDiff',
            fields=[
                ('id', ecm.lib.bigint.BigAutoField(serialize=False, primary_key=True)),
                ('new', models.BooleanField(default=True, db_index=True)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('member', models.ForeignKey(to='hr.Member')),
                ('role', models.ForeignKey(to='hr.Role')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='RoleMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member', models.ForeignKey(to='hr.Member')),
                ('role', models.ForeignKey(to='hr.Role')),
            ],
            options={
                'ordering': ['member'],
            },
        ),
        migrations.CreateModel(
            name='RoleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typeName', models.CharField(unique=True, max_length=64)),
                ('dispName', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['dispName'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skillpoints', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('character', models.ForeignKey(related_name='skills', to='hr.Member')),
                ('eve_type', models.ForeignKey(to='eve.Type', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titleID', models.BigIntegerField()),
                ('titleName', models.CharField(max_length=256)),
                ('tiedToBase', models.BigIntegerField(default=0)),
                ('accessLvl', models.BigIntegerField(default=0)),
                ('corp', models.ForeignKey(related_name='titles', to='corp.Corporation')),
            ],
            options={
                'ordering': ['titleID'],
            },
        ),
        migrations.CreateModel(
            name='TitleCompoDiff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('new', models.BooleanField(default=True, db_index=True)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('role', models.ForeignKey(related_name='title_compo_diffs', to='hr.Role')),
                ('title', models.ForeignKey(related_name='title_compo_diffs', to='hr.Title')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='TitleComposition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.ForeignKey(to='hr.Role')),
                ('title', models.ForeignKey(to='hr.Title')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='TitleMemberDiff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('new', models.BooleanField(default=True, db_index=True)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('member', models.ForeignKey(related_name='title_member_diffs', to='hr.Member')),
                ('title', models.ForeignKey(related_name='title_member_diffs', to='hr.Title')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='TitleMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member', models.ForeignKey(to='hr.Member')),
                ('title', models.ForeignKey(to='hr.Title')),
            ],
            options={
                'ordering': ['member'],
            },
        ),
        migrations.AddField(
            model_name='title',
            name='members',
            field=models.ManyToManyField(related_name='titles', through='hr.TitleMembership', to='hr.Member'),
        ),
        migrations.AddField(
            model_name='title',
            name='roles',
            field=models.ManyToManyField(related_name='titles', through='hr.TitleComposition', to='hr.Role'),
        ),
        migrations.AddField(
            model_name='role',
            name='members',
            field=models.ManyToManyField(related_name='roles', through='hr.RoleMembership', to='hr.Member'),
        ),
        migrations.AddField(
            model_name='role',
            name='roleType',
            field=models.ForeignKey(related_name='roles', to='hr.RoleType'),
        ),
        migrations.AddField(
            model_name='role',
            name='wallet',
            field=models.ForeignKey(blank=True, to='corp.Wallet', null=True),
        ),
        migrations.AddField(
            model_name='employmenthistory',
            name='member',
            field=models.ForeignKey(related_name='employment_history', to='hr.Member'),
        ),
    ]
