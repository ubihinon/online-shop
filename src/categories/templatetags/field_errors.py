from django.template.loader_tags import register


@register.inclusion_tag('common/field_errors.html')
def field_errors(field):
    return {
        'field': field
    }
