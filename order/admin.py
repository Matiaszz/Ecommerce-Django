"""Admin Orders """

from django.contrib import admin
from .models import OrderedItem, Order


class OrderedItemsInline(admin.TabularInline):
    """Order Inline"""

    model = OrderedItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin"""

    inlines = [
        OrderedItemsInline
    ]


@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):
    """OrderedItem admin"""

    list_display = ['product']
