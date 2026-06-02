from django.contrib import admin
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.urls import path
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

import uuid

from .models import AboutPage, PromotionPage, PromotionPost


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    search_fields = ('title', 'content')
    readonly_fields = ('updated_at',)

    class Media:
        css = {
            'all': ('css/admin-about-ckeditor.css',),
        }
        js = (
            'https://cdn.ckeditor.com/4.22.1/full-all/ckeditor.js',
            'js/admin-about-ckeditor.js',
        )

    def has_add_permission(self, request):
        if AboutPage.objects.exists():
            return False
        return super().has_add_permission(request)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'ckeditor-upload/',
                self.admin_site.admin_view(csrf_exempt(self.ckeditor_upload)),
                name='pages_aboutpage_ckeditor_upload',
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
        path_name = f'pages/editor/{today:%Y/%m}/{filename}'
        saved_path = default_storage.save(path_name, uploaded_file)

        file_url = default_storage.url(saved_path)
        return JsonResponse({
            'uploaded': 1,
            'fileName': uploaded_file.name,
            'url': file_url,
        })


@admin.register(PromotionPage)
class PromotionPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    search_fields = ('title', 'content')
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        if PromotionPage.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(PromotionPost)
class PromotionPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'sort_order', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'sort_order')
    readonly_fields = ('created_at', 'updated_at')

# Register your models here.
