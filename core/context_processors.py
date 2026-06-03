from products.models import Category

from .models import SiteSetting


def site_settings(request):
    site_setting = SiteSetting.objects.first()
    request.site_setting = site_setting
    return {
        'site_setting': site_setting,
        'global_categories': Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related('children'),
    }
