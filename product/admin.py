"""Admin"""
from django.contrib import admin
from .models import Product, Variation


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    """Variation admin"""
    list_display = ['name', 'stock']


class VariationInline(admin.TabularInline):
    """Variation Inline"""
    model = Variation
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin"""
    list_display = ['name', 'short_description',
                    'get_price_formated', 'get_promotional_price_formated']
    inlines = [VariationInline]
