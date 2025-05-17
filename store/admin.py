from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Image, Product


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'size', 'picture')

    @staticmethod
    def picture(obj: Image) -> str:
        return format_html(
            f'<img src="{obj.image.url}" style="max-width: 100px">'
        )


class InlineImageAdmin(admin.TabularInline):
    model = Image
    extra = 0


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    list_display = ('title', 'availability', 'price', 'old_price', 'discount')
    search_fields = ('title', 'description')
    summernote_fields = ('description',)
    inlines = (InlineImageAdmin,)


class ProductInlineAdmin(admin.StackedInline):
    model = Category.products.through
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('slug',)
    inlines = (ProductInlineAdmin,)

    @staticmethod
    def total_products(obj: Category) -> str:
        count = obj.products.count()
        link = f'/admin/store/product/?categories__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products</a>')
