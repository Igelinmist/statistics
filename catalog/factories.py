import factory

from . import models


class UnitFactory(factory.django.DjangoModelFactory):
    """Factory for creation Unit nodes"""
    class Meta:
        model = models.Unit
    name = 'Test_unit'
    plant_id = None
