# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayedMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=0)),
                ('playedDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('_game', models.ForeignKey(to='Store.Game')),
                ('_player', models.ForeignKey(to='Users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='SavedGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.TextField()),
                ('savedDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('settings', models.TextField()),
                ('_game', models.ForeignKey(to='Store.Game')),
                ('_player', models.ForeignKey(to='Users.Profile')),
            ],
        ),
    ]
