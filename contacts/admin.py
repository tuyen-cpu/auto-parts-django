from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'message')
    readonly_fields = ('full_name', 'phone', 'email', 'message', 'created_at')
    list_editable = ('is_read',)

# Register your models here.
