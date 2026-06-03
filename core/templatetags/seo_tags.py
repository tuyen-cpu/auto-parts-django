from django import template
from django.utils.safestring import mark_safe

from core.seo import dump_json_ld

register = template.Library()


@register.filter
def json_ld(value):
    return mark_safe(dump_json_ld(value))
