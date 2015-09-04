# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20150722_1010'),
        ('statistics', '0007_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='journal',
        ),
        migrations.AddField(
            model_name='report',
            name='equipment',
            field=models.OneToOneField(default=None, to='catalog.Unit'),
            preserve_default=False,
        ),
    ]
