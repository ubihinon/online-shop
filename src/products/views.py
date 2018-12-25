from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from categories.models import Category
from products.filters import ProductFilter
from products.forms import ProductEditForm
from products.models import Product
from products.serializers import ProductSerializer
from shopping_baskets.models import ShoppingBasket


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name', 'description', 'price')

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class ProductList(ListView):
    model = Product
    fields = ('name', 'description')
    template_name = 'products/product_list.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'category': get_object_or_404(Category, id=self.kwargs.get('category_id'))
        }


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    slug_field = 'product_id'

    def get_context_data(self, *args, **kwargs):
        return {
            'user': self.request.user,
            'product': get_object_or_404(Product, id=self.kwargs.get('pk')),
            'basket': ShoppingBasket.objects.get_user_shopping_basket(self.request.user),
        }


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/product_edit.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse_lazy(
            'products-detail',
            kwargs={'category_id': self.kwargs.get('category_id'), 'pk': self.kwargs.get('pk')}
        )


class ProductDeleteView(DeleteView):
    model = Product

    def get_success_url(self):
        return reverse_lazy(
            'products',
            kwargs={'category_id': self.kwargs.get('category_id')}
        )
