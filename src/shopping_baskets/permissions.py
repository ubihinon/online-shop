from rest_framework.permissions import BasePermission

from shopping_baskets.models import ShoppingBasket
from users.models import User


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if ShoppingBasket.objects.filter(id=view.kwargs.get('pk')).exists():
            shopping_basket = ShoppingBasket.objects.get(id=view.kwargs.get('pk'))
            return request.user == shopping_basket.user
        return User.objects.filter(id=request.user.id).exists()
