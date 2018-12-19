import django_filters

from products.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_by_name')
    min_price = django_filters.CharFilter(method='filter_from_min_price', label='min_price')
    max_price = django_filters.CharFilter(method='filter_until_max_price', label='max_price')
    description = django_filters.CharFilter(method='filter_by_description')
    ordering = django_filters.OrderingFilter(
        fields={
            'name': 'name',
            'price': 'price'
        }
    )

    class Meta:
        model = Product
        fields = ('name', 'description')

    def filter_by_name(self, queryset, name, value):
        return queryset.get_products_by_name(value)

    def filter_by_description(self, queryset, name, value):
        return queryset.get_products_by_description(value)

    def filter_from_min_price(self, queryset, name, value):
        return queryset.get_products_price_more_than(value)

    def filter_until_max_price(self, queryset, name, value):
        return queryset.get_products_price_less_than(value)
