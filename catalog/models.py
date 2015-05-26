from django.db import models


class Unit(models.Model):
    plant = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        if self.plant is None:
            plant_name = '\\'
        else:
            plant_name = self.plant
        return '{0} - {1}'.format(plant_name, self.name)

    class Meta:
        ordering = ['plant_id', 'name']
        verbose_name_plural = "units"
