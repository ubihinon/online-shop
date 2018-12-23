from django.urls import path, include

from web_ui import views

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('shopping-basket/', views.ShoppingBasketView.as_view(), name='shopping-basket'),
    path('categories/<int:category_id>/products/<slug:pk>/', views.ProductDetail.as_view(),
         name='products-detail'),
    path('categories/<int:category_id>/products/', views.ProductList.as_view(), name='products'),
]
