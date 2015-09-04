# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0009_auto_20150902_1003'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='column',
            options={'verbose_name': 'столбец', 'verbose_name_plural': 'столбцы'},
        ),
    ]
