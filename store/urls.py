from django.urls import path

from .views import IndexView, ProductDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product'),

]
