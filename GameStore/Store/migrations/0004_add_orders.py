# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_orders(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("Users", "Profile")
    Category = apps.get_model("Store", "Category")
    Game = apps.get_model("Store", "Game")



class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_populate_sample_games2'),
    ]

    operations = [
        migrations.RunPython(create_orders),
    ]
