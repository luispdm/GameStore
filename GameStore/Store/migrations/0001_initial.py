# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Store.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
                ('description', models.TextField()),
                ('url', models.URLField(unique=True)),
                ('price', models.FloatField(default=0)),
                ('publicationDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('logo', models.URLField(default='http://www.yourimage.com')),
                ('popularity', models.IntegerField(default=0)),
                ('_category', models.ForeignKey(to='Store.Category')),
                ('_developer', models.ForeignKey(to='Users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('total', models.FloatField(default=0)),
                ('orderDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('orderDateYMD', models.CharField(max_length=8, default=Store.models.get_default_ymd)),
                ('orderDateYW', models.CharField(max_length=6, default=Store.models.get_default_yw)),
                ('orderDateYM', models.CharField(max_length=6, default=Store.models.get_default_ym)),
                ('orderDateY', models.CharField(max_length=4, default=Store.models.get_default_y)),
                ('paymentDate', models.DateTimeField(null=True, default=None)),
                ('paymentRef', models.IntegerField(null=True, default=0)),
                ('status', models.CharField(max_length=10, default='pending')),
                ('_games', models.ManyToManyField(blank=True, default=None, to='Store.Game')),
                ('_player', models.ForeignKey(to='Users.Profile')),
            ],
        ),
    ]
