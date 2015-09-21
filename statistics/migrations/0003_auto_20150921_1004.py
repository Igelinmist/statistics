# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0002_auto_20150921_0944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journal',
            options={'ordering': ['equipment__name'], 'default_permissions': [], 'verbose_name': 'журнал', 'verbose_name_plural': 'журналы', 'permissions': (('view_journal_details', 'Может просматривать записи журнала'), ('view_journal_list', 'Может посмотреть список журналов'), ('create_journal_record', 'Может создать запись в журнале'), ('edit_journal_record', 'Может редактировать запись в журнале'), ('delete_journal_record', 'Может удалить запись в журнале'), ('create_journal_event', 'Может создать событие в журнале'), ('delete_journal_event', 'Может удалить событие в журнале'))},
        ),
    ]
