from django.urls import path

from .views import AccountView, LoginView, activate, register

urlpatterns = [
    path('registration/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<str:uid>/<str:token>/', activate, name='activate'),
    path('account/', AccountView.as_view(), name='account'),
]
