from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from orders.forms import OrderForm
from orders.models import Order
from shopping_baskets.models import ShoppingBasket


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'basket': ShoppingBasket.objects.get_user_shopping_basket(self.request.user),
            'form': OrderForm(),
            'user': self.request.user
        }

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = request.user.id
            shopping_basket = ShoppingBasket.objects.get_user_shopping_basket(self.request.user)
            order.save()
            order.products.add(*[p['id'] for p in shopping_basket.products.all().values('id')])
            return HttpResponseRedirect(reverse_lazy('order-success'))
        return render(request, 'orders/order_create.html', {'form': form})


class OrderSuccess(TemplateView):
    model = Order
    template_name = 'orders/order_success.html'
