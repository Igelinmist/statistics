# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0005_auto_20150701_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventitem',
            name='event',
            field=models.CharField(max_length=3, choices=[('ZMN', 'Замена'), ('VVD', 'Ввод'), ('SPS', 'Списание')]),
        ),
    ]
