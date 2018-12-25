from django.template.loader_tags import register

from categories.models import Category


@register.simple_tag
def show_categories():
    return {
        'categories': Category.objects.get_root_categories()
    }
