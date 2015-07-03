# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0003_auto_20150701_1110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='stateitem',
            options={'default_permissions': ()},
        ),
    ]
