from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from categories.forms import CategoryEditForm
from categories.models import Category
from categories.serializers import CategorySerializer, CategoryCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return CategoryCreateSerializer
        return CategorySerializer


class CategoryList(ListView):
    model = Category
    fields = ('id', 'name',)
    template_name = 'categories/categories.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'categories': Category.objects.filter(parent__isnull=True)
        }


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'categories/category_edit.html'
    form_class = CategoryEditForm

    def get_context_data(self, *args, **kwargs):
        return {
            'form': CategoryEditForm(),
            'user': self.request.user,
        }

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('categories'))
        return render(request, 'categories/categories.html', {'form': form})


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'categories/category_edit.html'
    form_class = CategoryEditForm
    success_url = reverse_lazy('categories')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')
