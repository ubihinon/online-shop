from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from categories.models import Category
from products.models import Product


def show_categories():
    return {
        'categories': Category.objects.get_root_categories()
    }


class CategoryList(ListView):
    model = Category
    fields = ('id', 'name',)
    template_name = 'categories/category-list.html'

    def get_context_data(self, *args, **kwargs):
        print(f"CategoryList: {self.kwargs}")
        if self.kwargs.get('category_id'):
            categories = Category.objects.get_children_categories(self.kwargs.get('category_id'))
        else:
            categories = Category.objects.get_root_categories()
        return {
            'categories': categories
        }


class ProductList(ListView):
    model = Product
    fields = ('name', 'description')
    template_name = 'categories/product-list.html'

    def get_context_data(self, *args, **kwargs):
        # if self.kwargs.get('category_id'):
        category = get_object_or_404(Category, id=self.kwargs.get('category_id'))
        return {
            'category': category
        }


class ProductDetail(DetailView):
    model = Product
    fields = ('name', 'description')
    template_name = 'categories/product-detail.html'
    slug_field = 'product_id'

    def get_context_data(self, *args, **kwargs):
        print(f"PRODUCT: {self.kwargs.get('pk')}")
        product = get_object_or_404(Product, id=self.kwargs.get('pk'))
        return {
            'product': product
        }
