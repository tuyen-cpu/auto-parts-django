from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.forms.models import BaseInlineFormSet
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import uuid

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'sort_order')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'slug', 'description', 'seo_title', 'seo_description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'sort_order')
    fieldsets = (
        ('Thong tin danh muc', {
            'fields': ('name', 'slug', 'parent', 'image', 'description'),
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description'),
        }),
        ('Hien thi', {
            'fields': ('is_active', 'sort_order'),
        }),
    )


class ProductImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        active_forms = [
            form for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        ]
        if len(active_forms) > 20:
            raise ValidationError('Mỗi sản phẩm chỉ được thêm tối đa 20 ảnh phụ.')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    formset = ProductImageInlineFormSet
    extra = 3
    max_num = 20
    fields = ('image', 'alt_text', 'sort_order')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'sale_price', 'is_featured', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_featured', 'category', 'created_at')
    search_fields = ('name', 'sku', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_featured', 'is_active')
    date_hierarchy = 'created_at'
    inlines = (ProductImageInline,)
    fieldsets = (
        ('Thong tin san pham', {
            'fields': ('name', 'slug', 'sku', 'category', 'image', 'price', 'sale_price', 'rating'),
        }),
        ('Noi dung', {
            'fields': ('short_description', 'description'),
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description'),
        }),
        ('Hien thi', {
            'fields': ('is_featured', 'is_active'),
        }),
        ('Thoi gian', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    class Media:
        css = {
            'all': ('css/admin-about-ckeditor.css',),
        }
        js = (
            'https://cdn.ckeditor.com/4.22.1/full-all/ckeditor.js',
            'js/admin-about-ckeditor.js',
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'ckeditor-upload/',
                self.admin_site.admin_view(csrf_exempt(self.ckeditor_upload)),
                name='products_product_ckeditor_upload',
            ),
        ]
        return custom_urls + urls

    def ckeditor_upload(self, request):
        if request.method != 'POST':
            return JsonResponse({'error': {'message': 'POST method required.'}}, status=405)

        uploaded_file = request.FILES.get('upload')
        if not uploaded_file:
            return JsonResponse({'error': {'message': 'No image uploaded.'}}, status=400)

        if not uploaded_file.content_type.startswith('image/'):
            return JsonResponse({'error': {'message': 'Only image files are allowed.'}}, status=400)

        extension = uploaded_file.name.rsplit('.', 1)[-1].lower() if '.' in uploaded_file.name else 'jpg'
        today = timezone.now()
        filename = f'{uuid.uuid4().hex}.{extension}'
        path_name = f'products/editor/{today:%Y/%m}/{filename}'
        saved_path = default_storage.save(path_name, uploaded_file)

        return JsonResponse({
            'uploaded': 1,
            'fileName': uploaded_file.name,
            'url': default_storage.url(saved_path),
        })

# Register your models here.
