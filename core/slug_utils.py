import re
import unicodedata

from django.utils.text import Truncator


def vietnamese_slug(value, max_length=200, fallback='item'):
    text = unicodedata.normalize('NFD', value or '')
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    text = text.replace('đ', 'd').replace('Đ', 'D')
    text = re.sub(r'[^A-Za-z0-9]+', '-', text).strip('-').lower()
    text = re.sub(r'-{2,}', '-', text)
    text = Truncator(text or fallback).chars(max_length, truncate='')
    return text.strip('-') or fallback


def unique_slug(instance, value, *, slug_field='slug', max_length=200, fallback='item'):
    model = instance.__class__
    base_slug = vietnamese_slug(value, max_length=max_length, fallback=fallback)
    slug = base_slug
    counter = 2

    while model.objects.filter(**{slug_field: slug}).exclude(pk=instance.pk).exists():
        suffix = f'-{counter}'
        trimmed_base = base_slug[:max_length - len(suffix)].strip('-') or fallback
        slug = f'{trimmed_base}{suffix}'
        counter += 1

    return slug
