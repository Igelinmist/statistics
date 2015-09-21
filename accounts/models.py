from django.db import models
from django.contrib.auth.models import User

from catalog.models import Unit


class Employee(models.Model):
    """custom profile for User - Employee"""
    user = models.OneToOneField(User, related_name='profile')
    # user = models.ForeignKey(User, unique=True)
    department = models.CharField(max_length=100)
    responsible_for_equipment = models.ForeignKey(Unit, blank=True, null=True)
