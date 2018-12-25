"""online_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from categories.views import CategoryList
from online_shop import settings
from orders.views import OrderSuccess, OrderCreate
from products.views import ProductDetail, ProductUpdateView, ProductDeleteView, ProductList
from shopping_baskets.views import ShoppingBasketView
from users.views import SignupView


api_urls = [
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('categories/', include(('categories.urls', 'categories'), namespace='categories')),
    path(
        'shopping_baskets/',
        include(('shopping_baskets.urls', 'shopping_baskets'), namespace='shopping_baskets')
    ),
]

ui_urls = [
    path('categories/<int:category_id>/products/<slug:pk>/', ProductDetail.as_view(),
         name='products-detail'),
    path('categories/<int:category_id>/products/<slug:pk>/edit/', ProductUpdateView.as_view(),
         name='product-edit'),
    path(
        'categories/<int:category_id>/products/<slug:pk>/delete/',
        ProductDeleteView.as_view(),
        name='product-delete'
    ),
    path('categories/<int:category_id>/products/', ProductList.as_view(), name='products'),
    path('shopping-basket/', ShoppingBasketView.as_view(), name='shopping-basket-ui'),
    path('order-success/', OrderSuccess.as_view(), name='order-success'),
    path('order/', OrderCreate.as_view(), name='order-create'),
    path('auth/', include('django.contrib.auth.urls')),
    path('signup/', SignupView.as_view(), name='signup'),
    path('', CategoryList.as_view(), name='categories'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('', include(ui_urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
