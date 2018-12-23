from rest_framework import serializers

from products.serializers import ProductSerializer
from shopping_baskets.models import ShoppingBasket


class ShoppingBasketRetrieveSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = ShoppingBasket
        fields = ('id', 'user', 'products')


class ShoppingBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingBasket
        fields = ('products',)
