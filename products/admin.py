from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'sort_order')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'sort_order')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'sale_price', 'is_featured', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_featured', 'category', 'created_at')
    search_fields = ('name', 'sku', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_featured', 'is_active')
    date_hierarchy = 'created_at'

# Register your models here.
