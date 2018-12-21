from django.urls import path, include, re_path

from web_ui import views

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    # path('categories/<int:category_id>/products/', views.ProductList.as_view(),
    #      name='products-detail'),
    # path('categories/<int:category_id>/', views.CategoryList.as_view(), name='categories-detail'),
    # re_path('(?P<category_id>\\d+)/?$', views.CategoryList.as_view(), name='categories'),
    path('categories/<int:category_id>/products/<slug:pk>/', views.ProductDetail.as_view(),
         name='products-detail'),
    path('categories/<int:category_id>/products/', views.ProductList.as_view(), name='products'),
]
