from datetime import timedelta, date
import factory

from catalog.factories import UnitFactory
from statistics.models import Journal, Record, Report, Column


class JournalFactory(factory.django.DjangoModelFactory):
    """Factory for creation Journal for equipment"""
    class Meta:
        model = Journal

    stat_by_parent = False
    description = 'Journal description'


class RecordFactory(factory.django.DjangoModelFactory):
    """Factory for Record generation"""
    class Meta:
        model = Record

    date = factory.Sequence(lambda n: (date(2015, 1, 1) + timedelta(days=n)))
    work = timedelta(days=1)
    pusk_cnt = 0
    ostanov_cnt = 0


class ReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Report

    title = "Test Report"


class ColumnFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Column

    title = "Test column"


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

    JournalFactory(equipment_id=detail11.id, stat_by_parent=True)
    JournalFactory(equipment_id=detail12.id, stat_by_parent=True)
    JournalFactory(equipment_id=detail21.id, stat_by_parent=True)
    JournalFactory(equipment_id=detail22.id, stat_by_parent=True)
    return {
        'full_journal': full_journal,
        'base_journal': base_journal,
        'journal1': full_journal,
        'journal2': base_journal,
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
