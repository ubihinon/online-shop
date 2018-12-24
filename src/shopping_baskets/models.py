from django.contrib.auth.models import AnonymousUser
from django.db import models


class ShoppingBasketQuerySet(models.QuerySet):

    def get_user_shopping_basket(self, user):
        shopping_basket = None
        if not isinstance(user, AnonymousUser):
            shopping_basket = ShoppingBasket.objects.get(user=user)
        return shopping_basket


class ShoppingBasket(models.Model):
    products = models.ManyToManyField('products.Product', related_name='shopping_basket_products')
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    objects = ShoppingBasketQuerySet.as_manager()

    def __str__(self):
        return self.user.username
