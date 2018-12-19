from django.db import models

from categories.models import Category


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

    def __str__(self):
        return f"{self.name} at {self.category.name if self.category else 'unknown'}"
