from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader_tags import register
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from categories.models import Category
from orders.forms import OrderForm
from orders.models import Order
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
        return {
            'categories': Category.objects.get_root_categories()
        }


class ProductList(ListView):
    model = Product
    fields = ('name', 'description')
    template_name = 'categories/product-list.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'category': get_object_or_404(Category, id=self.kwargs.get('category_id'))
        }


class ProductDetail(DetailView):
    model = Product
    fields = ('name', 'description')
    template_name = 'categories/product-detail.html'
    slug_field = 'product_id'

    def get_context_data(self, *args, **kwargs):
        return {
            'product': get_object_or_404(Product, id=self.kwargs.get('pk')),
            'basket': ShoppingBasket.objects.get_user_shopping_basket(self.request.user),
        }


class ShoppingBasketView(TemplateView):
    model = ShoppingBasket
    fields = ('products', 'user')
    template_name = 'categories/shopping-basket.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'basket': ShoppingBasket.objects.get_user_shopping_basket(self.request.user),
        }


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order-create.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'basket': ShoppingBasket.objects.get_user_shopping_basket(self.request.user),
            'form': OrderForm()
        }

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        form = self.get_form(OrderForm)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = request.user.id

            shopping_basket = ShoppingBasket.objects.get_user_shopping_basket(self.request.user)
            order.save()
            order.products.add(*[p['id'] for p in shopping_basket.products.all().values('id')])
            return HttpResponseRedirect(reverse_lazy('order-success'))


class OrderSuccess(TemplateView):
    model = Order
    template_name = 'orders/order-success.html'
