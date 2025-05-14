from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'availability', 'price', 'old_price', 'discount')
    search_fields = ('title', 'description')
