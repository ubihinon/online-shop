from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from shopping_baskets.models import ShoppingBasket
from users.models import User


@receiver(post_save, sender=User)
def create_sopping_basket(sender, instance, created=False, **kwargs):
    if created:
        ShoppingBasket.objects.create(user=instance)


@receiver(post_save, sender=Order)
def clear_sopping_basket(sender, instance, created=False, **kwargs):
    if created:
        ShoppingBasket.objects.get(user=instance.user).products.clear()
