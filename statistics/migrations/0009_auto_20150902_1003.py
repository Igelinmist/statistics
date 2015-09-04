# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0008_auto_20150901_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('column_type', models.CharField(max_length=3, choices=[('ITV', 'Интервал'), ('DT', 'Дата'), ('PCN', 'Количество пусков'), ('OCN', 'Количество остановов')])),
                ('from_event', models.CharField(max_length=3, choices=[('FVZ', 'от ввода/замены'), ('FKR', 'от капремонта'), ('FSR', 'от среднего ремонта'), ('FRC', 'от реконструкции')])),
                ('element_name_filter', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'verbose_name': 'отчет', 'verbose_name_plural': 'отчеты'},
        ),
        migrations.AddField(
            model_name='column',
            name='report',
            field=models.ForeignKey(to='statistics.Report'),
        ),
    ]
