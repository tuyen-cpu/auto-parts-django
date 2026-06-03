import unicodedata

from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from core.seo import breadcrumb_schema, clean_text, item_list_schema, local_business_schema, product_schema, seo_context

from .models import Category, Product, ProductImage


def normalize_search_text(value):
    value = unicodedata.normalize('NFD', value or '')
    value = ''.join(char for char in value if unicodedata.category(char) != 'Mn')
    return value.casefold()


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 39

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category', 'category__parent')
        self.category = None
        slug = self.kwargs.get('slug')
        if slug:
            self.category = get_object_or_404(Category, slug=slug, is_active=True)
            if self.category.parent_id:
                queryset = queryset.filter(category=self.category)
            else:
                queryset = queryset.filter(Q(category=self.category) | Q(category__parent=self.category))

        query = self.request.GET.get('q', '').strip()

        sort = self.request.GET.get('sort', 'newest')
        if sort == 'price_asc':
            queryset = queryset.order_by('sale_price', 'price', '-created_at')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-sale_price', '-price', '-created_at')
        else:
            queryset = queryset.order_by('-created_at')

        if query:
            normalized_query = normalize_search_text(query)
            queryset = [
                product for product in queryset
                if normalized_query in normalize_search_text(
                    ' '.join([
                        product.name,
                        product.sku,
                        product.short_description,
                        product.category.name,
                    ])
                )
            ]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        context['categories'] = Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related('children')
        context['q'] = self.request.GET.get('q', '')
        context['sort'] = self.request.GET.get('sort', 'newest')
        site_setting = getattr(self.request, 'site_setting', None)
        site_name = getattr(site_setting, 'site_name', '') or 'AutoParts'
        if self.category:
            title = self.category.seo_title or f'Phu tung {self.category.name} chinh hang, bao gia nhanh | {site_name}'
            description = (
                self.category.seo_description
                or clean_text(self.category.description, 34)
                or f'Danh muc phu tung {self.category.name} chinh hang, tu van dung ma theo xe, bao gia nhanh va giao hang toan quoc.'
            )
            breadcrumb_items = [
                ('Trang chủ', reverse('core:home')),
                ('Sản phẩm', reverse('products:list')),
                (self.category.name, self.category.get_absolute_url()),
            ]
            canonical_path = self.category.get_absolute_url()
        else:
            title = f'San pham phu tung o to chinh hang, bao gia nhanh | {site_name}'
            description = 'Danh sach phu tung o to chinh hang, nhieu danh muc, ho tro tim theo ten san pham hoac SKU, tu van dung ma theo xe.'
            breadcrumb_items = [
                ('Trang chủ', reverse('core:home')),
                ('Sản phẩm', reverse('products:list')),
            ]
            canonical_path = reverse('products:list')
        robots = 'noindex,follow' if self.request.GET.get('q') else 'index,follow'
        context.update(seo_context(
            self.request,
            title=title,
            description=description,
            canonical_path=canonical_path,
            robots=robots,
            json_ld=[
                local_business_schema(self.request, site_setting),
                breadcrumb_schema(self.request, breadcrumb_items),
                item_list_schema(
                    self.request,
                    context['products'],
                    name=self.category.name if self.category else 'San pham phu tung o to',
                ),
            ],
        ))
        if context.get('is_paginated'):
            context['page_range'] = context['paginator'].get_elided_page_range(
                context['page_obj'].number,
                on_each_side=2,
                on_ends=2,
            )
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category', 'category__parent').prefetch_related('gallery_images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_images'] = ProductImage.objects.filter(product=self.object)
        context['related_products'] = Product.objects.filter(
            is_active=True,
            category=self.object.category,
        ).exclude(pk=self.object.pk)[:4]
        site_setting = getattr(self.request, 'site_setting', None)
        site_name = getattr(site_setting, 'site_name', '') or 'AutoParts'
        title = self.object.seo_title or f'{self.object.name} {self.object.sku} | {site_name}'
        description = (
            self.object.seo_description
            or self.object.short_description
            or clean_text(self.object.description, 34)
            or f'{self.object.name} chinh hang, ma {self.object.sku}, tu van dung ma theo xe, bao gia nhanh va ho tro giao hang toan quoc.'
        )
        breadcrumb_items = [
            ('Trang chủ', reverse('core:home')),
            ('Sản phẩm', reverse('products:list')),
            (self.object.category.name, self.object.category.get_absolute_url()),
            (self.object.name, self.object.get_absolute_url()),
        ]
        context.update(seo_context(
            self.request,
            title=title,
            description=description,
            image=self.object.image.url if self.object.image else '',
            canonical_path=self.object.get_absolute_url(),
            og_type='product',
            json_ld=[
                product_schema(self.request, self.object),
                breadcrumb_schema(self.request, breadcrumb_items),
            ],
        ))
        return context

# Create your views here.
