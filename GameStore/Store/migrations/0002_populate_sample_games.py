# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model("Store", "Category")
    Category.objects.create(name="Action")
    Category.objects.create(name="Adventure")
    Category.objects.create(name="FPS")
    Category.objects.create(name="Racing")
    Category.objects.create(name="Sports")
    Category.objects.create(name="Puzzle")
    Category.objects.create(name="Test")

class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]
