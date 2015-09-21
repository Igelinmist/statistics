# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='column',
            options={'ordering': ['weigh'], 'default_permissions': [], 'verbose_name': 'столбец', 'verbose_name_plural': 'столбцы'},
        ),
        migrations.AlterModelOptions(
            name='journal',
            options={'ordering': ['equipment__name'], 'default_permissions': [], 'verbose_name': 'журнал', 'verbose_name_plural': 'журналы'},
        ),
        migrations.AlterModelOptions(
            name='record',
            options={'default_permissions': [], 'verbose_name': 'запись', 'verbose_name_plural': 'записи'},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'default_permissions': [], 'verbose_name': 'отчет', 'verbose_name_plural': 'отчеты'},
        ),
        migrations.AddField(
            model_name='report',
            name='weigh',
            field=models.IntegerField(default=0),
        ),
    ]
