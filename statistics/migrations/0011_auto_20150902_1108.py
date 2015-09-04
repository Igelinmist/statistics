# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0010_auto_20150902_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='weigh',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='column',
            name='element_name_filter',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='column',
            name='from_event',
            field=models.CharField(max_length=3, choices=[('FVZ', 'ввод/замена'), ('FKR', 'капремонт'), ('FSR', 'средний ремонт'), ('FRC', 'реконструкция')]),
        ),
    ]
