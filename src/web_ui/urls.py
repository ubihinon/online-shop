from django.urls import path, include

from web_ui import views

urlpatterns = [
    path('categories/<int:category_id>/products/<slug:pk>/', views.ProductDetail.as_view(),
         name='products-detail'),
    path('categories/<int:category_id>/products/', views.ProductList.as_view(), name='products'),
    path('shopping-basket/', views.ShoppingBasketView.as_view(), name='shopping-basket'),
    path('order-success/', views.OrderSuccess.as_view(), name='order-success'),
    path('order/', views.OrderCreate.as_view(), name='order-create'),
    path('auth/', include('django.contrib.auth.urls')),
    path('', views.CategoryList.as_view(), name='categories'),
]
