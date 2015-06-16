from django.db import models


class Unit(models.Model):
    plant = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=50)

    def tree_list(root_unit=None):
        """
        Функция переупорядочивает список самоприсоединенных объектов
        в виде дерева от корневого объекта. Корневой объект не входит
        в выходной список.
        """
        def get_knot_dict(input_set):
            res = {}
            for unit in input_set:
                if unit.plant_id in res:
                    res[unit.plant_id].append(unit)
                else:
                    res[unit.plant_id] = [unit]
            return res

        def get_tree(knot_dict, tree_list, ident=0, node=None):
            if node:
                tree_list.append((node, ident))
            ident += 1
            for branch_object in knot_dict[node.id if node else None]:
                if branch_object.id in knot_dict:
                    get_tree(knot_dict, tree_list, ident, branch_object)
                else:
                    tree_list.append((branch_object, ident))
            ident -= 1

        units = Unit.objects.all()
        tree_list = []
        knot_dict = get_knot_dict(units)
        get_tree(knot_dict, tree_list, 0, root_unit)
        return tree_list

    def __str__(self):
        if self.plant is None:
            plant_name = '\\'
        else:
            plant_name = self.plant
        return '{0} - {1}'.format(plant_name, self.name)

    class Meta:
        ordering = ['plant_id', 'name']
        verbose_name_plural = "units"
