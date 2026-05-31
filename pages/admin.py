from django.contrib import admin

from .models import AboutPage, PromotionPage, PromotionPost


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    search_fields = ('title', 'content')
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        if AboutPage.objects.exists():
            return False
        return super().has_add_permission(request)


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
