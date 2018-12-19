from rest_framework import serializers

from categories.models import Category
from products.serializers import ProductSerializer


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'products')
