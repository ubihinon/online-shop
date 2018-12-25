from django.db.models.signals import post_save
from django.dispatch import receiver

from shopping_baskets.models import ShoppingBasket
from users.models import User


@receiver(post_save, sender=User)
def create_shopping_basket(sender, instance, created=False, **kwargs):
    if created:
        ShoppingBasket.objects.create(user=instance)
