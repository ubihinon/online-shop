from django.views.generic import TemplateView
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from products.models import Product
from shopping_baskets.models import ShoppingBasket
from shopping_baskets.permissions import IsOwner
from shopping_baskets.serializers import (
    ShoppingBasketSerializer,
    ShoppingBasketRetrieveSerializer
)


class ShoppingBasketViewSet(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    permission_classes = (IsOwner,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ShoppingBasketRetrieveSerializer
        return ShoppingBasketSerializer

    def get_queryset(self):
        if self.request.user.id:
            return ShoppingBasket.objects.filter(user=self.request.user)
        return []

    @action(
        detail=True,
        url_path='products',
        methods=['PUT'],
    )
    def add_products(self, request, *args, **kwargs):
        basket = ShoppingBasket.objects.get(id=self.kwargs.get('pk'), user=request.user)

        product_ids = []
        products_key = 'products[]' if 'products[]' in dict(request.data) else 'products'
        for product_id in dict(request.data).get(products_key):
            if int(product_id) not in list(basket.products.all().values_list('id', flat=True)):
                product_ids.append(product_id)
        basket.products.add(*product_ids)

        serializer = self.get_serializer(
            {
                "products": Product.objects.filter(id__in=dict(request.data).get(products_key))
            }
        )
        return Response(serializer.data)

    @action(
        detail=True,
        url_path='products/(?P<product_id>[^/.]+)',
        methods=['DELETE']
    )
    def delete_product(self, request, *args, **kwargs):
        if self.kwargs.get('product_id').isdigit():
            basket = ShoppingBasket.objects.get(user=request.user)
            basket.products.remove(self.kwargs.get('product_id'))
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShoppingBasketView(TemplateView):
    model = ShoppingBasket
    fields = ('products', 'user')
    template_name = 'categories/shopping_basket.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'basket': ShoppingBasket.objects.get_user_shopping_basket(self.request.user),
        }
