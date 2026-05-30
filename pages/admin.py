from django.contrib import admin

from .models import AboutPage


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    search_fields = ('title', 'content')
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        if AboutPage.objects.exists():
            return False
        return super().has_add_permission(request)

# Register your models here.
