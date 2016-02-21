# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Store.models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_add_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderDateYMD',
            field=models.CharField(default=Store.models.get_default_ymd, max_length=8),
        ),
    ]
