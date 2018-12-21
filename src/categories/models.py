from django.db import models
from django.db.models import Value, CharField


class CategoryQueryset(models.QuerySet):

    def get_root_categories(self):
        return self.filter(parent__isnull=True)

    def get_children_categories(self, category):
        return self.filter(parent_id=category)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    objects = CategoryQueryset.as_manager()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def get_children(self):
        return Category.objects.filter(parent=self)
        # return Category.objects.annotate(children=Value(self, output_field=CharField())).filter(parent=self)
        # return Category.objects.annotate(children=Value(self, output_field=CharField())).filter(parent=self)
        # sub_categories = [self]
        # k = self.parent
        # while k is not None:
        #     sub_categories.append(k)
        #     k = k.parent
        # return sub_categories[::-1]
        # return Category.objects.filter(parent=self)

        # return Category.objects.annotate(children=Value(F('category_parent').name, output_field=CharField())).filter(parent=self)
        # return Category.objects.select_related('parent').annotate(children=Value(F('category_parent').name, output_field=CharField())).filter(parent=self)
        # return Category.objects.extra(select={'parent': 'category.parent'})
        # .select_related('parent')\

        # sub_categories = [self]
        # k = self.parent
        # while k is not None:
        #     sub_categories.append(k)
        #     k = k.parent
        # return sub_categories[::-1]

        # # return Category.objects.filter(parent__category=self)
        # return Category.objects.annotate(children=Value('dsf', output_field=CharField()))
        # # sub_categories = [self]
        # # k = self.parent
        # # while k is not None:
        # #     sub_categories.append(k)
        # #     k = k.parent
        # # return sub_categories[::-1]
