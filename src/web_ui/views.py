from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader_tags import register
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, \
    DeleteView

from categories.models import Category
from orders.models import Order
from products.models import Product
from shopping_baskets.models import ShoppingBasket
from users.models import User
from web_ui.forms import SignUpForm, OrderForm, ProductEditForm


@register.simple_tag
def show_categories():
    return {
        'categories': Category.objects.get_root_categories()
    }


@register.inclusion_tag('common/field_errors.html')
def field_errors(field):
    return {
        'field': field
    }


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
    template_name = 'products/product-detail.html'
    slug_field = 'product_id'

    def get_context_data(self, *args, **kwargs):
        return {
            'user': self.request.user,
            'product': get_object_or_404(Product, id=self.kwargs.get('pk')),
            'basket': ShoppingBasket.objects.get_user_shopping_basket(self.request.user),
        }


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/product-edit.html'
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
