from django.views.generic import DetailView, TemplateView

from .models import Product
from .selectors import (all_not_most_recent_categories_selector,
                        hot_deals_selector, most_products_categories_selector,
                        product_detail_selector)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'most_recent_categories': most_products_categories_selector(),
            'all_other_categories': all_not_most_recent_categories_selector(),
            'hot_deals': hot_deals_selector()
        }
        return context


class ProductDetailView(DetailView):
    template_name = 'product-details.html'
    model = Product
    queryset = product_detail_selector()
