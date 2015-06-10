# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import statistics.models


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0002_auto_20150526_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='last_stat',
            field=models.CharField(default=statistics.models.default_stat, max_length=250, editable=False),
        ),
    ]
