# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='_ownedGames',
            field=models.ManyToManyField(default=None, to='Store.Game', blank=True),
        ),
    ]
