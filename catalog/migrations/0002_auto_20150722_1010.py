# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='unit',
            options={'ordering': ['plant_id', 'name'], 'verbose_name': 'оборудование', 'verbose_name_plural': 'оборудование'},
        ),
    ]
