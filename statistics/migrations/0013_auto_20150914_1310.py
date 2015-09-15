# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0012_auto_20150911_0839'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='column',
            options={'ordering': ['weigh'], 'verbose_name': 'столбец', 'verbose_name_plural': 'столбцы'},
        ),
    ]
