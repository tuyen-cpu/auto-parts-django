from django import template

register = template.Library()


@register.filter
def vnd(value):
    if value is None:
        return 'Liên hệ'
    return f'{value:,.0f}'.replace(',', '.') + ' VND'
