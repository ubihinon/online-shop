from rest_framework import routers

from shopping_baskets import views

router = routers.SimpleRouter()
router.register('', views.ShoppingBasketViewSet, base_name='shopping-baskets')

urlpatterns = router.urls
