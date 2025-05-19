from django.db.models import Count, QuerySet

from .models import Category, Product


def most_products_categories_selector() -> QuerySet[Category]:
    return Category.objects.annotate(
        products_count=Count('products')
    ).order_by('-products_count')[:7]


def all_not_most_recent_categories_selector() -> QuerySet[Category]:
    recent_categories = most_products_categories_selector()
    return Category.objects.exclude(id__in=recent_categories.values_list('id', flat=True))


def hot_deals_selector() -> QuerySet[Product]:
    return Product.objects.filter(discount__isnull=False).order_by('discount')[:3]


def best_sellers_selector() -> QuerySet[Product]:
    return Product.objects.order_by('price')[:8]


def related_products_selector(product: Product) -> QuerySet[Product]:
    return Product.objects.filter(
        categories__in=product.categories.all()
    ).exclude(id=product.id)


def product_detail_selector() -> QuerySet[Product]:
    return Product.objects.all()


def category_products_selector(category: Category) -> QuerySet[Product]:
    return Product.objects.filter(categories=category).order_by('-price')
