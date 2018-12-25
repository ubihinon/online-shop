from django import forms

from categories.models import Category


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
            'parent',
        )
