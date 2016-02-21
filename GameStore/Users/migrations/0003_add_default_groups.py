# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def combine_names(apps, schema_editor):
    Group = apps.get_model("auth","Group")
    Group.objects.create(name='players')
    Group.objects.create(name='developers')


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_profile__ownedgames'),
    ]

    operations = [
        migrations.RunPython(combine_names),
    ]
