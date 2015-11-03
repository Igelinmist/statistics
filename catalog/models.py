from django.db import models


class Unit(models.Model):
    plant = models.ForeignKey('self', blank=True,
                              null=True, on_delete=models.CASCADE)
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

        units = Unit.objects.all()
        tree_list = []
        knot_dict = get_knot_dict(units)
        get_tree(knot_dict, tree_list, 0, root_unit)
        return tree_list

    def unit_tree(self):
        """
        Метод строит дерево входящих объектов
        """
        def get_knot_dict(input_set):
            res = {}
            for unit in input_set:
                if unit.plant_id in res:
                    res[unit.plant_id].append(unit)
                else:
                    res[unit.plant_id] = [unit]
            return res

        def get_tree(knot_dict, tree, ident=0, node=None):
            if node:
                tree.append((node, ident))
            ident += 1
            for branch_object in knot_dict[node.id if node else None]:
                if branch_object.id in knot_dict:
                    get_tree(knot_dict, tree, ident, branch_object)
                else:
                    tree.append((branch_object, ident))

        units = Unit.objects.all()
        tree = []
        knot_dict = get_knot_dict(units)
        get_tree(knot_dict, tree, 0, self)
        return tree

    def get_records(self, rdate):
        """
        Метод ищет существующие записи на дату в журналах,
        входящих в дерево от данного оборудования.
        """
        #TODO доделать
        records = {}
        unit_tree = self.unit_tree()
        for unit, ident in unit_tree:
            pass
        journals_id = [u.journal.id for u, i in unit_tree]
        rec_set = Record.objects.filter(date=reqdate(rdate))
        rec_set = rec_set.filter(journal_id__in=journals_id)
        for rec in rec_set.all():
            records[rec.journal_id] = rec.get_data()
        return records

    def __str__(self):
        if self.plant is None:
            plant_name = '\\'
        else:
            plant_name = self.plant
        return '{0} - {1}'.format(plant_name, self.name)

    class Meta:
        ordering = ['plant_id', 'name']
        verbose_name = 'оборудование'
        verbose_name_plural = 'оборудование'
