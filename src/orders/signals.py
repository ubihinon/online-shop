from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from orders.tasks import send_order_email


@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created=False, **kwargs):
    send_order_email.delay(user_id=instance.user.id, order_id=instance.id)
