from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.template.loader_tags import register
from django.views.generic import ListView, DetailView, TemplateView

from categories.models import Category
from products.models import Product
from shopping_baskets.models import ShoppingBasket


@register.simple_tag
def show_categories():
    return {
        # 'categories': Category.objects.get_root_categories()
        'categories': Category.objects.all()
    }


class CategoryList(ListView):
    model = Category
    fields = ('id', 'name',)
    template_name = 'categories/categories.html'

    def get_context_data(self, *args, **kwargs):
        categories = Category.objects.get_root_categories()
        return {
            'categories': categories
        }


class ProductList(ListView):
    model = Product
    fields = ('name', 'description')
    template_name = 'categories/product-list.html'

    def get_context_data(self, *args, **kwargs):
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
        product = get_object_or_404(Product, id=self.kwargs.get('pk'))
        shopping_basket = None
        if not isinstance(self.request.user, AnonymousUser):
            shopping_basket = ShoppingBasket.objects.get(user=self.request.user)
        return {
            'product': product,
            'basket': shopping_basket
        }


class ShoppingBasketView(TemplateView):
    model = ShoppingBasket
    fields = ('products', 'user')
    template_name = 'categories/shopping-basket.html'

    def get_context_data(self, *args, **kwargs):
        shopping_basket = None
        if not isinstance(self.request.user, AnonymousUser):
            shopping_basket = ShoppingBasket.objects.get(user=self.request.user)
        return {
            'basket': shopping_basket
        }
