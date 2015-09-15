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
    detail22 = UnitFactory(plant_id=subunit2.id, name='detail2_')
    full_journal = JournalFactory(equipment_id=subunit1.id, extended_stat=True)
    base_journal = JournalFactory(equipment_id=subunit2.id, extended_stat=False)

    subjournal = JournalFactory(equipment_id=detail11.id, stat_by_parent=True)
    JournalFactory(equipment_id=detail12.id, stat_by_parent=True)
    JournalFactory(equipment_id=detail21.id, stat_by_parent=True)
    JournalFactory(equipment_id=detail22.id, stat_by_parent=True)
    return {
        'full_journal': full_journal,
        'base_journal': base_journal,
        'journal1': full_journal,
        'journal2': base_journal,
        'subjournal': subjournal,
        'unit_root': unit_root,
        'detail11': detail11,
        'detail12': detail12,
        'detail21': detail21,
        'detail22': detail22,
    }


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
    equipment = journal_tree['unit_root']
    test_journal = journal_tree['full_journal']
    edate = None
    if fevent and create_event:
        edate = test_journal.record_set.order_by('date').all()[2].date
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
