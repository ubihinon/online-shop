from rest_framework import routers

from products import views

router = routers.SimpleRouter()
router.register('products', views.ProductViewSet, base_name='products')

urlpatterns = router.urls
