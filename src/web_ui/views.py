from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader_tags import register
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from categories.models import Category
from orders.models import Order
from products.models import Product
from shopping_baskets.models import ShoppingBasket
from users.models import User
from web_ui.forms import SignUpForm, OrderForm


@register.simple_tag
def show_categories():
    return {
        'categories': Category.objects.get_root_categories()
    }


def show_categories(request):
    return render(
        request,
        'categories/category-list.html', {
            'categories': Category.objects.filter(parent__isnull=True)
            # 'categories': Category.objects.all()
        }
    )


class CategoryList(ListView):
    model = Category
    fields = ('id', 'name',)
    template_name = 'categories/categories.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'categories': Category.objects.filter(parent__isnull=True)
        }


class ProductList(ListView):
    model = Product
    fields = ('name', 'description')
    template_name = 'products/product-list.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'category': get_object_or_404(Category, id=self.kwargs.get('category_id'))
        }


class ProductDetail(DetailView):
    model = Product
    fields = ('name', 'description')
    template_name = 'products/product-detail.html'
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


class SignupView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        form = self.get_form(SignUpForm)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('categories'))
        return render(request, 'registration/signup.html', {'form': form})
