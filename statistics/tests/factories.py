import factory

from catalog.factories import UnitFactory
from statistics import models


class JournalFactory(factory.Factory):
    """Factory for creation Journal for equipment"""
    class Meta:
        model = models.Journal

    equipment = factory.SubFactory(UnitFactory, name='Equipment_journal')
    extended_stat = False
    stat_by_parent = False
    description = 'Journal description'
    last_stat = "wd=00:00,psk=0,ost=0"
