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
