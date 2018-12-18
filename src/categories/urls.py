from rest_framework import routers

from categories import views

router = routers.SimpleRouter()
router.register('', views.CategoryViewSet, base_name='categories')

urlpatterns = router.urls
