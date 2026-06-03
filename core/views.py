from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape
from django.db.models import Count, Q

from pages.models import AboutPage, PromotionPost
from products.models import Category, Product

from .models import Banner
from .seo import local_business_schema, seo_context, website_schema


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
    site_setting = getattr(request, 'site_setting', None)
    title = f'{getattr(site_setting, "site_name", "") or "AutoParts"} - Phu tung o to chinh hang, bao gia nhanh'
    description = (
        getattr(site_setting, 'seo_description', '')
        or getattr(site_setting, 'slogan', '')
        or 'Phu tung o to chinh hang cho nhieu dong xe, tu van dung ma theo xe, bao gia nhanh, san pham ro nguon goc va giao hang toan quoc.'
    )
    seo = seo_context(
        request,
        title=title,
        description=description,
        image=hero_banner.image.url if hero_banner and hero_banner.image else '',
        canonical_path=request.path,
        json_ld=[
            local_business_schema(request, site_setting),
            website_schema(request, site_setting),
        ],
    )
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
            **seo,
        },
    )

# Create your views here.


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse('sitemap_xml'))
    llms_url = request.build_absolute_uri(reverse('llms_txt'))
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /*?q=',
        'Disallow: /*?sort=',
        f'Sitemap: {sitemap_url}',
        f'LLMS: {llms_url}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def llms_txt(request):
    site_setting = getattr(request, 'site_setting', None)
    name = getattr(site_setting, 'site_name', '') or 'AutoParts'
    description = (
        getattr(site_setting, 'seo_description', '')
        or 'Website cung cap phu tung o to chinh hang, tu van dung ma theo xe, bao gia nhanh va giao hang toan quoc.'
    )
    lines = [
        f'# {name}',
        '',
        description,
        '',
        '## Noi dung chinh',
        '- Danh muc phu tung o to theo nhom san pham.',
        '- Trang chi tiet san pham co ten, SKU, mo ta, gia va hinh anh.',
        '- Trang khuyen mai va thong tin lien he tu van bao gia.',
        '',
        '## Lien ket quan trong',
        f'- Trang chu: {request.build_absolute_uri(reverse("core:home"))}',
        f'- San pham: {request.build_absolute_uri(reverse("products:list"))}',
        f'- Khuyen mai: {request.build_absolute_uri(reverse("promotion"))}',
        f'- Lien he: {request.build_absolute_uri(reverse("contacts:contact"))}',
        f'- Sitemap: {request.build_absolute_uri(reverse("sitemap_xml"))}',
        '',
        '## Huong dan cho LLM',
        'Uu tien doc sitemap.xml de lay URL moi nhat. Khong su dung noi dung trong /admin/ hoac cac URL tim kiem co tham so q/sort lam nguon chinh.',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/markdown; charset=utf-8')


def sitemap_xml(request):
    urls = []

    def add_url(path, priority='0.7', changefreq='weekly', lastmod=None):
        item = {
            'loc': request.build_absolute_uri(path),
            'priority': priority,
            'changefreq': changefreq,
            'lastmod': lastmod,
        }
        urls.append(item)

    add_url(reverse('core:home'), priority='1.0', changefreq='daily')
    add_url(reverse('products:list'), priority='0.9', changefreq='daily')
    add_url(reverse('promotion'), priority='0.7', changefreq='weekly')
    add_url(reverse('pages:about'), priority='0.6', changefreq='monthly')
    add_url(reverse('contacts:contact'), priority='0.6', changefreq='monthly')

    for category in Category.objects.filter(is_active=True):
        add_url(category.get_absolute_url(), priority='0.8', changefreq='weekly')

    for product in Product.objects.filter(is_active=True).only('slug', 'updated_at'):
        add_url(product.get_absolute_url(), priority='0.9', changefreq='weekly', lastmod=product.updated_at)

    for post in PromotionPost.objects.filter(is_active=True).only('slug', 'updated_at'):
        add_url(post.get_absolute_url(), priority='0.7', changefreq='weekly', lastmod=post.updated_at)

    now = timezone.now()
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for item in urls:
        lastmod = item['lastmod'] or now
        body.extend([
            '  <url>',
            f'    <loc>{escape(item["loc"])}</loc>',
            f'    <lastmod>{lastmod.date().isoformat()}</lastmod>',
            f'    <changefreq>{item["changefreq"]}</changefreq>',
            f'    <priority>{item["priority"]}</priority>',
            '  </url>',
        ])
    body.append('</urlset>')
    return HttpResponse('\n'.join(body), content_type='application/xml')
