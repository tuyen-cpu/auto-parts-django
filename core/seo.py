import json
import re
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import Truncator


DEFAULT_SITE_NAME = 'AutoParts - Phu tung o to chinh hang, bao gia nhanh'
DEFAULT_DESCRIPTION = (
    'Phu tung o to chinh hang cho nhieu dong xe, tu van dung ma theo xe, bao gia nhanh, san pham ro nguon goc va giao hang toan quoc.'
)


def clean_text(value, words=32):
    text = strip_tags(value or '')
    text = re.sub(r'\s+', ' ', text).strip()
    return Truncator(text).words(words, truncate='') if text else ''


def absolute_url(request, path_or_url=''):
    if not path_or_url:
        return request.build_absolute_uri('/')
    if str(path_or_url).startswith(('http://', 'https://')):
        return path_or_url
    return request.build_absolute_uri(path_or_url)


def media_absolute_url(request, image_field):
    if not image_field:
        return ''
    try:
        return absolute_url(request, image_field.url)
    except ValueError:
        return ''


def site_name(site_setting=None):
    return getattr(site_setting, 'site_name', '') or DEFAULT_SITE_NAME


def get_site_setting(request):
    site_setting = getattr(request, 'site_setting', None)
    if site_setting is None:
        from .models import SiteSetting

        site_setting = SiteSetting.objects.first()
        request.site_setting = site_setting
    return site_setting


def site_title(site_setting=None):
    return getattr(site_setting, 'seo_title', '') or site_name(site_setting)


def format_title(title='', site_setting=None):
    title = (title or '').strip()
    resolved_site_title = site_title(site_setting)
    if not title or title == resolved_site_title:
        return resolved_site_title
    return f'{title} | {resolved_site_title}'


def site_description(site_setting=None):
    return (
        getattr(site_setting, 'seo_description', '')
        or getattr(site_setting, 'description', '')
        or getattr(site_setting, 'slogan', '')
        or DEFAULT_DESCRIPTION
    )


def site_summary(site_setting=None):
    return (
        getattr(site_setting, 'description', '')
        or getattr(site_setting, 'seo_description', '')
        or getattr(site_setting, 'slogan', '')
        or DEFAULT_DESCRIPTION
    )


def seo_context(
    request,
    *,
    title,
    description='',
    image='',
    canonical_path=None,
    og_type='website',
    robots='index,follow',
    json_ld=None,
):
    site_setting = get_site_setting(request)
    resolved_description = clean_text(description, 34) or site_description(site_setting)
    canonical_url = absolute_url(request, canonical_path or request.path)
    image_url = absolute_url(request, image) if image else ''

    return {
        'seo': {
            'title': title,
            'description': resolved_description,
            'canonical_url': canonical_url,
            'image_url': image_url,
            'og_type': og_type,
            'robots': robots,
            'json_ld': json_ld or [],
        }
    }


def local_business_schema(request, site_setting=None):
    name = site_name(site_setting)
    schema = {
        '@context': 'https://schema.org',
        '@type': 'AutoPartsStore',
        'name': name,
        'url': absolute_url(request, reverse('core:home')),
        'description': site_summary(site_setting),
    }
    logo = media_absolute_url(request, getattr(site_setting, 'logo', None))
    if logo:
        schema['logo'] = logo
        schema['image'] = logo
    if getattr(site_setting, 'hotline', ''):
        schema['telephone'] = site_setting.hotline
    if getattr(site_setting, 'email', ''):
        schema['email'] = site_setting.email
    if getattr(site_setting, 'address', ''):
        schema['address'] = {
            '@type': 'PostalAddress',
            'streetAddress': site_setting.address,
            'addressCountry': 'VN',
        }
    same_as = [
        url for url in [
            getattr(site_setting, 'facebook_url', ''),
            getattr(site_setting, 'zalo_url', ''),
            getattr(site_setting, 'tiktok_url', ''),
            getattr(site_setting, 'instagram_url', ''),
            getattr(site_setting, 'youtube_url', ''),
            getattr(site_setting, 'x_url', ''),
            getattr(site_setting, 'linkedin_url', ''),
            getattr(site_setting, 'google_business_url', ''),
        ] if url
    ]
    if same_as:
        schema['sameAs'] = same_as
    return schema


def website_schema(request, site_setting=None):
    return {
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        'name': site_name(site_setting),
        'url': absolute_url(request, reverse('core:home')),
        'description': site_summary(site_setting),
        'potentialAction': {
            '@type': 'SearchAction',
            'target': f'{absolute_url(request, reverse("products:list"))}?q={{search_term_string}}',
            'query-input': 'required name=search_term_string',
        },
    }


def item_list_schema(request, items, *, name='Danh sach san pham'):
    return {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'name': name,
        'itemListElement': [
            {
                '@type': 'ListItem',
                'position': index,
                'url': absolute_url(request, item.get_absolute_url()),
                'name': getattr(item, 'name', getattr(item, 'title', '')),
            }
            for index, item in enumerate(items, start=1)
        ],
    }


def article_schema(request, post):
    image = media_absolute_url(request, post.image)
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': post.title,
        'description': post.summary or clean_text(post.content, 34),
        'url': absolute_url(request, post.get_absolute_url()),
        'datePublished': post.created_at.isoformat(),
        'dateModified': post.updated_at.isoformat(),
        'publisher': {
            '@type': 'Organization',
            'name': site_name(getattr(request, 'site_setting', None)),
        },
    }
    if image:
        schema['image'] = [image]
    return schema


def breadcrumb_schema(request, items):
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {
                '@type': 'ListItem',
                'position': index,
                'name': name,
                'item': absolute_url(request, url),
            }
            for index, (name, url) in enumerate(items, start=1)
        ],
    }


def product_schema(request, product):
    image = media_absolute_url(request, product.image)
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Product',
        'name': product.name,
        'sku': product.sku,
        'category': product.category.name,
        'description': clean_text(product.description, 60) or product.short_description,
        'url': absolute_url(request, product.get_absolute_url()),
        'brand': {
            '@type': 'Brand',
            'name': site_name(getattr(request, 'site_setting', None)),
        },
        'offers': {
            '@type': 'Offer',
            'url': absolute_url(request, product.get_absolute_url()),
            'availability': 'https://schema.org/InStock',
            'itemCondition': 'https://schema.org/NewCondition',
            'priceCurrency': 'VND',
            'seller': {
                '@type': 'Organization',
                'name': site_name(getattr(request, 'site_setting', None)),
            },
        },
    }
    if image:
        schema['image'] = [image]
    if product.display_price:
        schema['offers']['price'] = str(product.display_price)
    if product.rating:
        schema['aggregateRating'] = {
            '@type': 'AggregateRating',
            'ratingValue': str(product.rating),
            'reviewCount': '1',
        }
    return schema


def dump_json_ld(data):
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))
