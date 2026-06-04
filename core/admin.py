from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from .models import Banner, SiteSetting


class NoManagerAuthMixin:
    def _is_admin_user(self, request):
        return request.user.is_superuser or request.user.groups.filter(name='Admin').exists()

    def has_module_permission(self, request):
        return self._is_admin_user(request)

    def has_view_permission(self, request, obj=None):
        return self._is_admin_user(request)

    def has_add_permission(self, request):
        return self._is_admin_user(request)

    def has_change_permission(self, request, obj=None):
        return self._is_admin_user(request)

    def has_delete_permission(self, request, obj=None):
        return self._is_admin_user(request)


try:
    admin.site.unregister(User)
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class RestrictedUserAdmin(NoManagerAuthMixin, UserAdmin):
    pass


@admin.register(Group)
class RestrictedGroupAdmin(NoManagerAuthMixin, GroupAdmin):
    pass


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'slogan', 'hotline', 'email', 'address')
    search_fields = ('site_name', 'slogan', 'seo_title', 'description', 'seo_description', 'hotline', 'email', 'address')
    fieldsets = (
        ('Thông tin chung', {
            'fields': ('site_name', 'slogan', 'seo_title', 'description', 'seo_description', 'logo', 'hotline', 'email', 'address', 'google_analytics_id'),
        }),
        ('Liên kết và bản đồ', {
            'fields': (
                'facebook_url',
                'zalo_url',
                'tiktok_url',
                'instagram_url',
                'youtube_url',
                'x_url',
                'linkedin_url',
                'google_business_url',
                'google_map_iframe',
            ),
        }),
    )

    def has_add_permission(self, request):
        if SiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'eyebrow', 'is_active', 'sort_order')
    list_filter = ('is_active',)
    search_fields = ('eyebrow', 'title', 'subtitle')
    fieldsets = (
        ('Nội dung banner trang chủ', {
            'fields': ('eyebrow', 'title', 'subtitle', 'image'),
        }),
        ('Nút hành động', {
            'fields': ('button_text', 'button_url'),
        }),
        ('Hiển thị', {
            'fields': ('is_active', 'sort_order'),
        }),
    )
    list_editable = ('is_active', 'sort_order')

# Register your models here.
