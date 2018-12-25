import os

from celery import Celery
from online_shop import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_shop.settings")

app = Celery('online_shop')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)
