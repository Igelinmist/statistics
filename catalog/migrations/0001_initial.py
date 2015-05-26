# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('plant', models.ForeignKey(blank=True, to='catalog.Unit', null=True)),
            ],
            options={
                'ordering': ['plant_id', 'name'],
                'verbose_name_plural': 'units',
            },
        ),
    ]
