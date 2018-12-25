from django.template.loader_tags import register


@register.inclusion_tag('categories/field_errors.html')
def field_errors(field):
    return {
        'field': field
    }
