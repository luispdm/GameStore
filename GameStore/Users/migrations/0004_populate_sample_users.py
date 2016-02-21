# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import hashers
from django.db import models, migrations
import uuid


def create_users(apps, schema_editor):
    Group = apps.get_model("auth","Group")
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("Users", "Profile")



    # Add 100 users: first 95 users are players, while last 5 are devs
    for i in range(1,95):
        username = "user%d" % i
        us1 = User(username=username, password=hashers.make_password("00000000"), email=("%s@gmail.com" % username))
        us1.is_active=True
        us1.save()

        user1 = Profile(user=us1, activationToken=uuid.uuid4())
        user1.save()

        players = Group.objects.get(name='players')
        us1.groups.add(players)

    for i in range(96, 100):
        username = "dev%d" % i
        us1 = User(username=username,  password=hashers.make_password("00000000"), email=("%s@gmail.com" % username))
        us1.is_active=True
        us1.save()

        user1 = Profile(user=us1, activationToken=uuid.uuid4())
        user1.save()

        developers = Group.objects.get(name='developers')
        us1.groups.add(developers)


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_add_default_groups'),
    ]

    operations = [
        migrations.RunPython(create_users),
    ]
