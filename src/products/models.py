from django.db import models

from categories.models import Category


class ProductQueryset(models.QuerySet):

    def get_products_price_more_than(self, value):
        return self.filter(price__gte=value)

    def get_products_price_less_than(self, value):
        return self.filter(price__lte=value)

    def get_products_by_name(self, value):
        return self.filter(name__icontains=value)

    def get_products_by_description(self, value):
        return self.filter(description__icontains=value)


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        null=True
    )

    objects = ProductQueryset.as_manager()

    def __str__(self):
        return f"{self.name} at {self.category.name if self.category else 'unknown'}"
