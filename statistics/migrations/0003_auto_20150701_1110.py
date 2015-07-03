# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0002_remove_record_period_length'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journal',
            options={'ordering': ['equipment__name'], 'permissions': (('view_journal_details', 'Может просматривать записи журнала'), ('view_journal_list', 'Может посмотреть список журналов'), ('create_journal_record', 'Может создать запись в журнале'), ('edit_journal_record', 'Может редактировать запись в журнале'), ('delete_journal_record', 'Может удалить запись в журнале'), ('create_journal_event', 'Может создать событие в журнале'), ('delete_journal_evtent', 'Может удалить событие в журнале'))},
        ),
    ]
