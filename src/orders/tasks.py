from celery.utils.log import get_task_logger
from django.core.mail import send_mail

from online_shop import settings
from online_shop.celery import app
from orders.models import Order
from users.models import User

logger = get_task_logger(__name__)


@app.task(bind=True)
def send_order_email(self, user_id, order_id):
    try:
        user = User.objects.get(id=user_id)
        order = Order.objects.get(id=order_id)
        products = ', '.join([p.name for p in order.products.all()])
        send_mail(
            'Order №{}'.format(order.id),
            '''
            Dear {}, you received this email because you have made the order in Online Shop.
            Our staff will call you as soon as possible.
            Your ordered goods:
            {}
            '''.format(user.username, products),
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        logger.info('Email send successfully')
    except Exception as e:
        logger.info(f'Exception {e}')
        self.retry(countdown=2, exc=e, max_retries=3)
