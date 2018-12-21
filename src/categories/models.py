from django.db import models


class CategoryQueryset(models.QuerySet):

    def get_root_categories(self):
        return self.filter(parent__isnull=True)

    def get_children_categories(self, category):
        return self.filter(parent_id=category)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    objects = CategoryQueryset.as_manager()

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def get_children(self):
        sub_categories = [self]
        k = self.parent
        while k is not None:
            sub_categories.append(k)
            k = k.parent
        return sub_categories[::-1]
