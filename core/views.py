from django.shortcuts import render
from django.db.models import Count, Q

from pages.models import AboutPage
from products.models import Category, Product

from .models import Banner


def home(request):
    banners = Banner.objects.filter(is_active=True)
    hero_banner = banners.first()
    parent_categories = Category.objects.filter(is_active=True, parent__isnull=True).annotate(
        child_count=Count('children', filter=Q(children__is_active=True), distinct=True),
        direct_product_count=Count('products', filter=Q(products__is_active=True), distinct=True),
    )[:8]
    featured_products = Product.objects.filter(is_active=True, is_featured=True).select_related('category')[:9]
    new_products = Product.objects.filter(is_active=True).select_related('category')[:9]
    about = AboutPage.objects.first()
    return render(
        request,
        'home.html',
        {
            'banners': banners,
            'hero_banner': hero_banner,
            'parent_categories': parent_categories,
            'featured_products': featured_products,
            'new_products': new_products,
            'about': about,
        },
    )

# Create your views here.
