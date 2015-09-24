from datetime import timedelta, date
from .factories import JournalFactory, RecordFactory
from .factories import ReportFactory, ColumnFactory
from catalog.factories import UnitFactory


def prepare_journal_tree():
    unit_root = UnitFactory(name='unit_root')
    subunit1 = UnitFactory(plant_id=unit_root.id, name='subunit1')
    subunit2 = UnitFactory(plant_id=unit_root.id, name='subunit2')
    detail11 = UnitFactory(plant_id=subunit1.id, name='detail1')
    detail12 = UnitFactory(plant_id=subunit1.id, name='detail2')
    detail21 = UnitFactory(plant_id=subunit2.id, name='detail1')
    # Намеренно не создаем detail2 в subunit2
    full_journal = JournalFactory(equipment_id=subunit1.id, extended_stat=True)
    base_journal = JournalFactory(equipment_id=subunit2.id, extended_stat=False)

    subjournal = JournalFactory(equipment_id=detail11.id, stat_by_parent=True)
    JournalFactory(equipment_id=detail12.id, stat_by_parent=True)
    subjournal2 = JournalFactory(equipment_id=detail21.id, stat_by_parent=True)
    return {
        'full_journal': full_journal,
        'base_journal': base_journal,
        'journal1': full_journal,
        'journal2': base_journal,
        'subjournal': subjournal,
        'subjournal2': subjournal2,
        'unit_root': unit_root,
        'detail11': detail11,
        'detail12': detail12,
        'detail21': detail21,
    }


def prepare_journal_tree_records():
    journal_tree = prepare_journal_tree()
    journal1 = journal_tree['journal1']
    #  10 дней работы (240 часов, всего 240)
    for i in range(10):
        RecordFactory(
            journal_id=journal1.id,
            date=date(2015, 1, 1 + i),
            work=timedelta(days=1),
            pusk_cnt=0,
            ostanov_cnt=0,
        )
    #  10 часов работы, потом останов, 14 часов капремонт
    #  (10 часов работы, всего 250)
    rec = RecordFactory(
        journal_id=journal1.id,
        date=date(2015, 1, 11),
        work=timedelta(hours=10),
        pusk_cnt=0,
        ostanov_cnt=1,
    )
    rec.stateitem_set.create(
        state='KRM',
        time_in_state=timedelta(hours=14, days=34))
    #  14 часов капремонта, потом пуск, 10 часов работы
    #  (10 часов работы, всего 260)
    #  после капремонта 10 часов
    rec = RecordFactory(
        journal_id=journal1.id,
        date=date(2015, 2, 15),
        work=timedelta(hours=10),
        pusk_cnt=1,
        ostanov_cnt=0,
    )
    rec.stateitem_set.create(
        state='KRM',
        time_in_state=timedelta(hours=14))
    journal1.eventitem_set.create(
        date=date(2015, 2, 15),
        event='VKR')

    journal2 = journal_tree['journal2']
    #  5 дней работы (120 часов, всего 120)
    for i in range(5):
        RecordFactory(
            journal_id=journal2.id,
            date=date(2015, 1, 1 + i),
            work=timedelta(days=1),
            pusk_cnt=0,
            ostanov_cnt=0,
        )
    #  10 часов работы, потом останов, 14 часов простоя
    #  (10 часов работы, всего 130)
    RecordFactory(
        journal_id=journal2.id,
        date=date(2015, 1, 6),
        work=timedelta(hours=10),
        pusk_cnt=0,
        ostanov_cnt=1,
    )
    #  после простоя ввод после замены detail21
    subjournal = journal_tree['subjournal2']
    subjournal.eventitem_set.create(
        date=date(2015, 2, 15),
        event='ZMN')
    # 10 часов работы, включение после замены
    # (всего 140 для detail21 - 10)
    RecordFactory(
        journal_id=journal2.id,
        date=date(2015, 2, 15),
        work=timedelta(hours=10),
        pusk_cnt=1,
        ostanov_cnt=0,
    )
    #  сутки работы (всего 164 для detail21 - 34)
    RecordFactory(
        journal_id=journal2.id,
        date=date(2015, 2, 16),
        work=timedelta(days=1),
        pusk_cnt=0,
        ostanov_cnt=0,
    )
    return journal_tree


def prepare_journal_tree_records_report():
    journal_tree = prepare_journal_tree_records()
    equipment = journal_tree['unit_root']
    report = ReportFactory(equipment_id=equipment.id)
    ColumnFactory(
        report_id=report.id,
        title='Наработка',
        column_type='ITV',
        from_event='FVZ',
        weigh=0,
    )
    ColumnFactory(
        report_id=report.id,
        title='Наработка с капремонта',
        column_type='ITV',
        from_event='FKR',
        weigh=1,
    )
    ColumnFactory(
        report_id=report.id,
        title='Дата капремонта',
        column_type='DT',
        from_event='FKR',
        weigh=2,
    )
    ColumnFactory(
        report_id=report.id,
        title='Наработка detail1',
        column_type='ITV',
        from_event='FVZ',
        element_name_filter='detail1',
        weigh=3,
    )
    ColumnFactory(
        report_id=report.id,
        title='Замена detail1',
        column_type='DT',
        from_event='FVZ',
        element_name_filter='detail1',
        weigh=4,
    )
    ColumnFactory(
        report_id=report.id,
        title='Наработка detail2',
        column_type='ITV',
        from_event='FVZ',
        element_name_filter='detail2',
        weigh=5,
    )
    ColumnFactory(
        report_id=report.id,
        title='Замена detail2',
        column_type='DT',
        from_event='FVZ',
        element_name_filter='detail2',
        weigh=6,
    )
    return report


def form_data():
    empty_time = timedelta(hours=0)
    return {'date': date.today()-timedelta(days=1),
            'ostanov_cnt': 1,
            'pusk_cnt': 1,
            'work': timedelta(hours=5),
            'rsv': empty_time,
            'trm': empty_time,
            'arm': timedelta(hours=19),
            'krm': empty_time,
            'srm': empty_time,
            'rcd': empty_time,
            }


def prepare_test_data_and_report_conf(ctype='ITV',
                                      fevent=None,
                                      create_event=True):
    journal_tree = prepare_journal_tree()
    for i in range(5):
        RecordFactory(journal_id=journal_tree['full_journal'].id)
    for i in range(45):
        RecordFactory(
            journal_id=journal_tree['full_journal'].id,
            pusk_cnt=0,
            ostanov_cnt=0,
            work=timedelta(hours=0)
        )
    for i in range(5):
        RecordFactory(journal_id=journal_tree['full_journal'].id)
    equipment = journal_tree['unit_root']
    test_journal = journal_tree['full_journal']
    edate = None
    if fevent and create_event:
        edate = test_journal.record_set.order_by('date').all()[49].date
        if fevent == 'FKR':
            test_journal.eventitem_set.create(
                date=edate,
                event='VKR'
            )
        elif fevent == 'FSR':
            test_journal.eventitem_set.create(
                date=edate,
                event='VSR'
            )
        elif fevent == 'FRC':
            test_journal.eventitem_set.create(
                date=edate,
                event='VRC'
            )
        elif fevent == 'FVZ':
            test_journal.eventitem_set.create(
                date=edate,
                event='ZMN'
            )

    report = ReportFactory(equipment_id=equipment.id)
    ColumnFactory(
        report_id=report.id,
        title='Заголовок',
        column_type=ctype,
        from_event=(fevent if fevent else 'FVZ')
    )
    return {
        'journal_tree': journal_tree,
        'test_journal': test_journal,
        'report': report,
        'edate': edate,
    }


def prepare_test_data_and_report_conf_for_subjournal(ctype='ITV',
                                                     replaced=False):
    journal_tree = prepare_journal_tree()
    for i in range(5):
        RecordFactory(journal_id=journal_tree['full_journal'].id)
    equipment = journal_tree['unit_root']
    main_journal = journal_tree['full_journal']
    test_journal = journal_tree['subjournal']
    if replaced:
        edate = main_journal.record_set.order_by('date').all()[2].date
        test_journal.eventitem_set.create(
            date=edate,
            event='ZMN'
        )
    report = ReportFactory(equipment_id=equipment.id)
    ColumnFactory(
        report_id=report.id,
        title='Заголовок',
        column_type=ctype,
        from_event='FVZ',
        element_name_filter='detail1'
    )
    return {
        'journal_tree': journal_tree,
        'test_journal': test_journal,
        'report': report,
    }


def prepare_test_db_for_report():
    journal_tree = prepare_journal_tree()
    for i in range(5):
        RecordFactory(journal_id=journal_tree['full_journal'].id)
    for i in range(5):
        RecordFactory(journal_id=journal_tree['base_journal'].id)
    equipment = journal_tree['unit_root']
    report = ReportFactory(equipment_id=equipment.id)
    ColumnFactory(
        report_id=report.id,
        title='Наработка с ввода/замены',
        column_type='ITV',
        from_event='FVZ',
    )
    ColumnFactory(
        report_id=report.id,
        title='Кол-во пусков',
        column_type='PCN',
        from_event='FVZ',
    )
    ColumnFactory(
        report_id=report.id,
        title='Наработка detail1',
        column_type='ITV',
        from_event='FVZ',
        element_name_filter='detail1'
    )
    return {'report': report, }
