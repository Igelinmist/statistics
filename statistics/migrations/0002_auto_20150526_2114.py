# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='work',
            field=models.DurationField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='stateitem',
            name='state',
            field=models.CharField(default='RSV', max_length=3, db_index=True, choices=[('RSV', 'Резерв'), ('TRM', 'Тек. ремонт'), ('ARM', 'Ав. ремонт'), ('KRM', 'Кап. ремонт'), ('SRM', 'Сред. ремонт'), ('RCD', 'Реконструкция')]),
        ),
    ]
