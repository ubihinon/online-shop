from rest_framework.permissions import BasePermission

from shopping_baskets.models import ShoppingBasket


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        shopping_basket = ShoppingBasket.objects.get(id=view.kwargs['pk'])
        return request.user == shopping_basket.user

