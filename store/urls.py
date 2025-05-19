from django.urls import path

from .views import IndexView, ProductDetailView, ProductListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/category/<slug:slug>/', ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product'),

]
