from datetime import timedelta, date
import factory

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
    work = timedelta(hours=20)
    pusk_cnt = 1
    ostanov_cnt = 1


class ReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Report

    title = "Test Report"


class ColumnFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Column

    title = "Test column"
