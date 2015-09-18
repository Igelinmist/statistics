# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import statistics.models.journal


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20150722_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('column_type', models.CharField(max_length=3, choices=[('ITV', 'Интервал'), ('DT', 'Дата'), ('PCN', 'Количество пусков'), ('OCN', 'Количество остановов')])),
                ('from_event', models.CharField(max_length=3, choices=[('FVZ', 'ввод/замена'), ('FKR', 'капремонт'), ('FSR', 'средний ремонт'), ('FRC', 'реконструкция')])),
                ('element_name_filter', models.CharField(max_length=50, blank=True)),
                ('weigh', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['weigh'],
                'verbose_name': 'столбец',
                'verbose_name_plural': 'столбцы',
            },
        ),
        migrations.CreateModel(
            name='EventItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('event', models.CharField(max_length=3, choices=[('VVD', 'Ввод'), ('VKR', 'Ввод из капремонта'), ('VSR', 'Ввод из ср. ремонта'), ('VRC', 'Ввод из реконструкции'), ('ZMN', 'Ввод после замены'), ('SPS', 'Списание')])),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extended_stat', models.BooleanField(default=False)),
                ('stat_by_parent', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('last_stat', models.CharField(default=statistics.models.journal.default_stat, max_length=250, editable=False)),
                ('equipment', models.OneToOneField(to='catalog.Unit')),
            ],
            options={
                'ordering': ['equipment__name'],
                'default_permissions': [],
                'verbose_name': 'журнал',
                'verbose_name_plural': 'журналы',
                'permissions': (('view_journal_details', 'Может просматривать записи журнала'), ('view_journal_list', 'Может посмотреть список журналов'), ('create_journal_record', 'Может создать запись в журнале'), ('edit_journal_record', 'Может редактировать запись в журнале'), ('delete_journal_record', 'Может удалить запись в журнале'), ('create_journal_event', 'Может создать событие в журнале'), ('delete_journal_event', 'Может удалить событие в журнале')),
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('work', models.DurationField(default='00:00')),
                ('pusk_cnt', models.IntegerField(default=0)),
                ('ostanov_cnt', models.IntegerField(default=0)),
                ('journal', models.ForeignKey(to='statistics.Journal')),
            ],
            options={
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('is_generalizing', models.BooleanField(default=False)),
                ('equipment', models.OneToOneField(related_name='report', to='catalog.Unit')),
            ],
            options={
                'verbose_name': 'отчет',
                'verbose_name_plural': 'отчеты',
            },
        ),
        migrations.CreateModel(
            name='StateItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default='RSV', max_length=3, db_index=True, choices=[('RSV', 'Резерв'), ('TRM', 'Тек. ремонт'), ('ARM', 'Ав. ремонт'), ('KRM', 'Кап. ремонт'), ('SRM', 'Сред. ремонт'), ('RCD', 'Реконструкция')])),
                ('time_in_state', models.DurationField()),
                ('record', models.ForeignKey(to='statistics.Record')),
            ],
            options={
                'default_permissions': [],
            },
        ),
        migrations.AddField(
            model_name='eventitem',
            name='journal',
            field=models.ForeignKey(to='statistics.Journal'),
        ),
        migrations.AddField(
            model_name='column',
            name='report',
            field=models.ForeignKey(to='statistics.Report'),
        ),
    ]
