from django.db import models


class ShoppingBasket(models.Model):
    products = models.ManyToManyField('products.Product', related_name='shopping_basket_products')
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
