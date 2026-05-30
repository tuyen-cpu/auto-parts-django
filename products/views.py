import unicodedata

from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Category, Product


def normalize_search_text(value):
    value = unicodedata.normalize('NFD', value or '')
    value = ''.join(char for char in value if unicodedata.category(char) != 'Mn')
    return value.casefold()


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 8

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
        return Product.objects.filter(is_active=True).select_related('category', 'category__parent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            is_active=True,
            category=self.object.category,
        ).exclude(pk=self.object.pk)[:4]
        return context

# Create your views here.
