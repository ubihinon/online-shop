from rest_framework import serializers

from shopping_baskets.models import ShoppingBasket


class ShoppingBasketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingBasket
        fields = ('id', 'user')


class ShoppingBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingBasket
        fields = ('products',)
