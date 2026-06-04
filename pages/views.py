from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import AboutPage, PromotionPost
from core.seo import article_schema, breadcrumb_schema, clean_text, format_title, get_site_setting, item_list_schema, local_business_schema, seo_context


def about(request):
    page = AboutPage.objects.first()
    site_setting = get_site_setting(request)
    title = format_title(page.title if page else 'Gioi thieu', site_setting)
    description = clean_text(page.content if page else '', 34) or 'Gioi thieu don vi cung cap phu tung o to chinh hang.'
    return render(request, 'about.html', {
        'page': page,
        **seo_context(
            request,
            title=title,
            description=description,
            image=page.image.url if page and page.image else '',
            canonical_path=reverse('pages:about'),
            json_ld=[
                local_business_schema(request, site_setting),
                breadcrumb_schema(request, [('Trang chá»§', reverse('core:home')), ('Giá»›i thiá»‡u', reverse('pages:about'))]),
            ],
        ),
    })


def promotion(request):
    posts = PromotionPost.objects.filter(is_active=True)
    site_setting = get_site_setting(request)
    return render(request, 'promotion.html', {
        'posts': posts,
        **seo_context(
            request,
            title=format_title('Khuyen mai phu tung o to', site_setting),
            description='Cap nhat uu dai, khuyen mai va chuong trinh bao gia phu tung o to.',
            canonical_path=reverse('promotion'),
            json_ld=[
                local_business_schema(request, site_setting),
                item_list_schema(request, posts, name='Khuyen mai phu tung o to'),
                breadcrumb_schema(request, [('Trang chá»§', reverse('core:home')), ('Khuyáº¿n mÃ£i', reverse('promotion'))]),
            ],
        ),
    })


def promotion_detail(request, slug):
    post = get_object_or_404(PromotionPost, slug=slug, is_active=True)
    site_setting = get_site_setting(request)
    description = post.summary or clean_text(post.content, 34)
    return render(request, 'promotion_detail.html', {
        'post': post,
        **seo_context(
            request,
            title=format_title(post.title, site_setting),
            description=description,
            image=post.image.url if post.image else '',
            canonical_path=post.get_absolute_url(),
            og_type='article',
            json_ld=[
                article_schema(request, post),
                breadcrumb_schema(request, [
                    ('Trang chá»§', reverse('core:home')),
                    ('Khuyáº¿n mÃ£i', reverse('promotion')),
                    (post.title, post.get_absolute_url()),
                ]),
            ],
        ),
    })

# Create your views here.
