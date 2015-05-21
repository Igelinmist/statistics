# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import statistics.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20150521_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('event', models.CharField(max_length=3, choices=[('VVD', 'Ввод'), ('ZMN', 'Замена'), ('SPS', 'Списание')])),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extended_stat', models.BooleanField(default=False)),
                ('stat_by_parent', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('last_stat', models.CharField(default=statistics.models.default_stat, max_length=100, editable=False)),
                ('equipment', models.ForeignKey(to='catalog.Unit')),
            ],
        ),
        migrations.CreateModel(
            name='JournalLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('period_length', models.IntegerField(default=24, choices=[(24, 'Сутки'), (8760, 'Год'), (8784, 'Вис. год')])),
                ('pusk_cnt', models.IntegerField(default=0)),
                ('ostanov_cnt', models.IntegerField(default=0)),
                ('journal', models.ForeignKey(to='statistics.Journal')),
            ],
        ),
        migrations.CreateModel(
            name='StateItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default='WRK', max_length=3, db_index=True, choices=[('WRK', 'Работа'), ('RSV', 'Резерв'), ('TRM', 'Тек. ремонт'), ('ARM', 'Ав. ремонт'), ('KRM', 'Кап. ремонт'), ('SRM', 'Сред. ремонт'), ('RCD', 'Реконструкция')])),
                ('time_in_state', models.DurationField()),
                ('journal_line', models.ForeignKey(to='statistics.JournalLine')),
            ],
        ),
        migrations.AddField(
            model_name='eventitem',
            name='journal',
            field=models.ForeignKey(to='statistics.Journal'),
        ),
    ]
