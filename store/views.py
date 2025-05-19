from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, Product
from .selectors import (best_sellers_selector, category_products_selector,
                        hot_deals_selector, product_detail_selector,
                        related_products_selector)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'hot_deals': hot_deals_selector()
        }
        return context


class ProductDetailView(DetailView):
    template_name = 'product-details.html'
    model = Product
    queryset = product_detail_selector()

    def get_context_data(self, **kwargs):
        product = self.get_object()
        context = super().get_context_data(**kwargs)
        context |= {
            'best_sellers': best_sellers_selector(),
            'related_products': related_products_selector(product)[:6]
        }
        return context


class ProductListView(ListView):
    template_name = 'shop-list.html'
    model = Product
    category = None
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return category_products_selector(self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'category': self.category,
            'total_objects': self.get_queryset().count()
        }
        return context
