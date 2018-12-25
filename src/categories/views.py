from django.views.generic import ListView
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

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
