from products.models import Category

from .models import SiteSetting


def site_settings(request):
    return {
        'site_setting': SiteSetting.objects.first(),
        'global_categories': Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related('children'),
    }
