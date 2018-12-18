from django.conf import settings
from django.core.management.base import BaseCommand
from ...models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            print('Creating user for %s (%s)' % (settings.ADMIN_USERNAME, settings.ADMIN_EMAIL))
            admin = User.objects.create_superuser(
                email=settings.ADMIN_EMAIL,
                username=settings.ADMIN_USERNAME,
                password=settings.ADMIN_INITIAL_PASSWORD
            )
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin user can only be initialized if no users exist')
