from django import forms

from products.models import Product


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
        )
