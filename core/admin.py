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
    list_display = ('site_name', 'hotline', 'email', 'address')
    search_fields = ('site_name', 'hotline', 'email', 'address')

    def has_add_permission(self, request):
        if SiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'sort_order')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    list_editable = ('is_active', 'sort_order')

# Register your models here.
