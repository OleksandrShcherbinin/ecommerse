from .selectors import (all_not_most_recent_categories_selector,
                        most_products_categories_selector)


def all_categories(request):
    return {
        'most_recent_categories': most_products_categories_selector(),
        'all_other_categories': all_not_most_recent_categories_selector(),
    }
