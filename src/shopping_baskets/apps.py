from django.apps import AppConfig


class ProductBinConfig(AppConfig):
    name = 'shopping_baskets'

    def ready(self):
        import shopping_baskets.signals
